# Wrangle module for Zillow Clustering Project
#------- by Heather McMillan
# Here are all the wrangle functions for recreating my project 
# You will need your own env.py file with your own credentials 
import pandas as pd
import numpy as np

# Vis tools
import matplotlib.pyplot as plt
import seaborn as sns

import scipy.stats as stats
from sklearn.model_selection import train_test_split

# defining some functions to make it easier. will go in Wrangle function
from env import host, password, user
import os

###################### Getting database Url ################
def get_db_url(db_name, user=user, host=host, password=password):
    """
        This helper function takes as default the user host and password from the env file.
        You must input the database name. It returns the appropriate URL to use in connecting to a database.
    """
    url = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
    return url

######################### get generic data #########################
def get_any_data(database, sql_query):
    '''
    put in the query and the database and get the data you need in a dataframe
    '''

    return pd.read_sql(sql_query, get_db_url(database))

######################### get Zillow Data #########################
def get_zillow_data():
    '''
    This function reads in Zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    sql_query = """
                SELECT parcelid, airconditioningtypeid, airconditioningdesc, architecturalstyletypeid, architecturalstyledesc,
                bathroomcnt, bedroomcnt, buildingclasstypeid, buildingclassdesc, buildingqualitytypeid,
                decktypeid, calculatedfinishedsquarefeet, fips, fireplacecnt, fireplaceflag, garagecarcnt, garagetotalsqft,
                hashottuborspa, latitude, longitude, lotsizesquarefeet, poolcnt, poolsizesum, propertycountylandusecode,
                propertylandusetypeid, propertylandusedesc, propertyzoningdesc, rawcensustractandblock, 
                regionidcity, regionidcounty, regionidneighborhood, roomcnt, threequarterbathnbr, typeconstructiontypeid, typeconstructiondesc, unitcnt, yearbuilt, numberofstories, structuretaxvaluedollarcnt, taxvaluedollarcnt, assessmentyear, 
                landtaxvaluedollarcnt, taxamount, censustractandblock, logerror, transactiondate 
                FROM properties_2017 AS p
                JOIN predictions_2017 USING (parcelid)
                INNER JOIN (SELECT parcelid, MAX(transactiondate) AS transactiondate
                FROM predictions_2017
                GROUP BY parcelid) 
                AS t USING (parcelid, transactiondate)
                LEFT JOIN airconditioningtype USING (airconditioningtypeid)
                LEFT JOIN architecturalstyletype USING (architecturalstyletypeid)
                LEFT JOIN buildingclasstype USING (buildingclasstypeid)
                LEFT JOIN heatingorsystemtype USING (heatingorsystemtypeid)
                LEFT JOIN propertylandusetype USING (propertylandusetypeid)
                LEFT JOIN storytype USING (storytypeid)
                LEFT JOIN typeconstructiontype USING (typeconstructiontypeid)
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL 
                AND transactiondate LIKE "2017%%";
                """
    if os.path.isfile('zillow_data.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('zillow_data.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = pd.read_sql(sql_query, get_db_url('zillow'))
        
        # Cache data
        df.to_csv('zillow_data.csv')

    return df

######################### Overview #########################
def overview(df, thresh = 10):
    '''
    This function takes in a dataframe and prints out useful things about each column.
    Unique values, value counts for columns less than 10 (can be adjusted with optional arguement thresh)
    Whether or not the row has nulls
    '''
    # create list of columns
    col_list = df.columns
    
    # loop through column list
    for col in col_list:
        # seperator using column name
        print(f'============== {col} ==============')
        
        # print out unique values for each column
        print(f'# Unique Vals: {df[col].nunique()}')
        
        # if number of things is under or equal to the threshold  print a value counts
        if df[col].nunique() <= thresh:
            print(df[col].value_counts(dropna = False).sort_index(ascending = True))
            
        # if the number is less than 150 and not an object, bin it and do value counts
        elif (df[col].nunique() < 150) and df[col].dtype != 'object' :
            print(df[col].value_counts(bins = 10, dropna=False).sort_index(ascending = True))
        
        # Space for readability 
        print('')
       

#########################

def missing_values_table(df):
    '''
    this function takes a dataframe as input and will output metrics for missing values, 
    and the percent of that column that has missing values
    '''
    # Total missing values
    mis_val = df.isnull().sum()
    
    # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    
    # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    
    # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(
    columns = {0 : 'Missing Values', 1 : '% of Total Values'})
    
    # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
    '% of Total Values', ascending=False).round(1)
    
    # Print some summary information
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
        "There are " + str(mis_val_table_ren_columns.shape[0]) +
        " columns that have missing values.")
        
        # Return the dataframe with missing information
    return mis_val_table_ren_columns

#########################

def nulls_by_row(df):
    '''
    This function takes in a dataframe and returns a dataframe with an overview of how many rows have missing values
    '''
    num_missing = df.isnull().sum(axis=1)
    prcnt_miss = round(num_missing / df.shape[1] * 100, 2)
    rows_missing = pd.DataFrame({'num_cols_missing': num_missing, 'percent_cols_missing': prcnt_miss})\
    .reset_index()\
    .groupby(['num_cols_missing', 'percent_cols_missing']).count()\
    .rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing

#########################

def single_homes(df):
    '''
    Function takes in zillow dataframe and outputs dataframe with only data for single unit homes.
    Single unit home defined as any of the following 
    'Single Family Residential', 'Townhouse', 'Manufactured, Modular, Prefabricated Homes', 'Mobile Home'
    Home must also have unit count of 1 or NaN
    '''
    # define single home descriptions
    single_homes = ['Single Family Residential', 'Townhouse', 'Manufactured, Modular, Prefabricated Homes', 'Mobile Home']
    
    # If the property land use description is the in the single homes list keep it
    df = df[df['propertylandusedesc'].isin(single_homes)]
    
    # create mask if unit count is 1 or NaN
    unitcnt_mask = (df['unitcnt'] == 1) | (df['unitcnt'].isnull())
    
    # apply mask to dataframe
    df = df[unitcnt_mask]
    
    return df

#########################

def drop_missing(df, min_col_percent= 0.65, min_row_percent = 0.85):
    '''
    This columns takes in a dataframe and outputs one with nulls dropped
    The minimum col percent is how many null values you would like to have in your columns for them to stay
    min_row_percent will be how many values must be not null in order to keep that row
    '''
    # calculate columns threshold (any columsn that have more nulls than this, dropped)
    col_thresh = int(round(min_col_percent*df.shape[0]))
    
    # drop coulmns 
    df = df.dropna(axis=1, thresh=col_thresh)
    
    # calculate row threshold 
    row_thresh = int(round(min_row_percent * df.shape[1]))
    
    # drop rows
    
    df = df.dropna(axis=0, thresh=row_thresh)
    
    return df

#########################

def get_house_age(df):
    '''
    This function takes in the Zillow dataframe, and uses the yearbuilt column
    to create new column called 'age'. 
    Outputs dataframe with new 'age' column attched.
    '''
     
    df['age'] = 2017 - df['yearbuilt']
    
    return df


#########################


def yearbuilt_bins(df):
    '''
    Function takes in a dataframe, uses the 'yearbuilt' column to create age bins
    pre 1978, 1978-2000, and post 2000 
    '''
    # set bin sizes
    year_bins = [df['yearbuilt'].min(), 1978, 2000,df['yearbuilt'].max()]
    
    # use cut to assign bins using yearbuilt column
    df['yearbuilt_bins'] = pd.cut(df['yearbuilt'], year_bins)
    
    return df

#########################

def ppsqft(df):
    '''
    This function takes in a dataframe and uses the 'calculatedfinishedsquarefeet' and 'taxvaluedollarcnt' columns
    to create new ppsqft column
    '''
    # create new column and do math
    df['ppsqft'] = round(df['taxvaluedollarcnt'] / df['calculatedfinishedsquarefeet'], 2)
    
    return df


#########################

def cali_counties(df):
    '''
    This function takes in the zillow dataframe, uses the fips column and a dictionary of counties
    and adds a column called county with where the house is located
    returns a dataframe with the column attached 
    '''
    # make dictionary with fips values and county names
    counties = {6037: 'LA', 6059: 'Orange', 6111: 'Ventura'}

    # use .replace to create an new column called county
    df['county'] = df.fips.replace(counties)

    return df


#########################

def get_tax_rate(df):
    '''
    Function takes in dataframe and returns with tax_rate column attched
    '''
    df['tax_rate'] = round(df['taxamount'] / df['taxvaluedollarcnt'] * 100, 2)
    
    return df


#########################

def remove_outliers(df, k, col_list):
    '''
    This function takes in a dataframe, k value, and column list and 
    k = number times interquartile range you would like to remove
    col_list = names of columns you want outliers removed from
    removes outliers from a list of columns in a dataframe 
    and return that dataframe
    '''
    
    for col in col_list:

        q1, q3 = df[f'{col}'].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[f'{col}'] > lower_bound) & (df[f'{col}'] < upper_bound)]
        
    return df


#########################

def drop_zillow_outliers(df):
    '''
    '''
    
    return df[((df.bathroomcnt <= 6) & (df.bathroomcnt > 0) & 
        (df.bedroomcnt <= 7) & (df.bedroomcnt > 0) & 
        (df.tax_rate < 15))]

#########################

def drop_unneeded_cols(df, unneeded_cols = ['lotsizesquarefeet', 'regionidcity', 'regionidcounty', 'assessmentyear']):
    '''
    This function takes in a dataframe and a list of unneeded columns (default is for zillow data)
    Returns dataframe with those columns dropped
    '''
    df = df.drop(columns = unneeded_cols)
    
    return df

#########################

def drop_rows_low_percent(df):
    '''
    Finds columns with missing values less than 1 percent. Drops all rows with missing values in those rows.
    '''
    
    has_percent_below_one = ((df.isnull().sum() / df.shape[0]) < .01)
    
    one_percenters = list(has_percent_below_one[has_percent_below_one == True].index)
    
    df = df.dropna(axis=0, subset=one_percenters)
    
    return df

#########################


def banana_split(df):
    '''
    args: df
    This function take in the telco_churn data data acquired by aquire.py, get_telco_data(),
    performs a split.
    Returns train, validate, and test dfs.
    '''
    train_validate, test = train_test_split(df, test_size=.2, 
                                        random_state=713)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=713)
    print(f'train --> {train.shape}')
    print(f'validate --> {validate.shape}')
    print(f'test --> {test.shape}')
    return train, validate, test

    


#########################

def wrangle_zillow():

    df = get_zillow_data()

    df = single_homes(df)

    df = drop_missing(df)

    df = get_house_age(df)

    df = yearbuilt_bins(df)

    df = get_tax_rate(df)

    df = ppsqft(df)

    df = cali_counties(df)

    df = drop_zillow_outliers(df)

    df = remove_outliers(df, 3, col_list = ['lotsizesquarefeet', 'regionidcity'])

    df = drop_unneeded_cols(df)

    df = drop_rows_low_percent(df)

    return df
#########################