import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans 

#####################

def plot_variable_dist(df, figsize = (3,2)):
    '''
    This function is for exploring. Takes in a dataframe with variables you would like to see the distribution of.
    Input the dataframe (either fully, or using .drop) with ONLY the columns you want to see plotted. 
    Optional argument figsize. Default it's small. 
    BTW if you just put list(df) it pulls out only the column names
    '''
    # loop through columns and use seaborn to plot distributions
    for col in list(df):
            plt.figure(figsize=figsize)
            plt.hist(data = df, x = col)
            plt.title(f'Distribution of {col}')
            plt.show()
            print(f'Number of Nulls: {df[col].isnull().sum()}')


##################### plot boxplots

def plot_boxes(df, figsize = (4,2)):
    '''
    This function is for exploring. Takes in a dataframe with variables you would like to see the box plot of.
    Input the dataframe (either fully, or using .drop) with ONLY the columns you want to see plotted.
    Will skip over object columns automatically.
    Optional argument figsize. Default it's small.    
    '''
    # loop through the columns in the dataframe entered
    for col in list(df):
        # check to see if col is numeric
        if df[col].dtypes != object: 
            plt.figure(figsize=figsize)
            sns.boxplot(data = df, x = col)
            plt.title(f'Box Plot of {col}')
            plt.show()
        else:
            print(f'{col} is an object type')

##################### plot variables against a the target

def plot_against_target(df, target, var_list, figsize = (10,5), hue = None):
    '''
    Takes in dataframe, target and varialbe list, and plots against target. 
    '''
    for var in var_list:
        plt.figure(figsize = (figsize))
        sns.regplot(data = df, x = var, y = target, 
                    line_kws={'color': 'orange'})
        plt.show()

##################### A scaler for exploring


def scale_this(X_df, scalertype):
    '''
    X_df = dataframe with columns you need scaled
    scalertype = something like StandardScaler(), or MinMaxScaler()
    This function takes a dataframe (an X data), a scaler, and ouputs a new dataframe with those columns scaled. 
    And a scaler to inverse transforming
    '''
    scaler = scalertype.fit(X_df)

    X_scaled = pd.DataFrame(scaler.transform(X_df), columns = X_df.columns).set_index([X_df.index.values])
    
    return X_scaled, scaler



##################### A cluster function for exploring and when you need centroids

def makin_clusters(X_df, k, col_name = None ):
    '''
    Function takes in scaled dataframe, k number of clusters you want to make
    Optional arguemenet col_name, If none is entered column returned is {k}_k_clusters
    Returns dataframe with column attched and dataframe with centroids (scaled) in it
    Returns: X_df, centroids_scaled, kmeans
    Use for exploring and when you need centroids
    '''
    
    #make thing
    kmeans = KMeans(n_clusters=k, random_state=713)

    #Fit Thing
    kmeans.fit(X_df)
    
    # create clusters
    centroids_scaled = pd.DataFrame(kmeans.cluster_centers_, columns = list(X_df))
    
    if col_name == None:
        #clusters on dataframe 
        X_df['clusters'] = kmeans.predict(X_df)
    else:
        X_df[col_name] = kmeans.predict(X_df)
        
    
    return X_df, centroids_scaled, kmeans

##################### Plot clusters

def plot_clusters(x ,y, cluster_col_name, df , kmeans, scaler, centroids):
    
    """ Takes in x and y (variable names as strings, along with returned objects from previous
    function create_cluster and creates a plot"""
    # set palette to zillow colors
    zpalette = ['#1277e1', '#f3ad35', '#0b449c', '#5289e4', '#c3eafb']

    # set figsize
    plt.figure(figsize=(10, 6))
    
    # scatterplot the clusters 
    sns.scatterplot(x = x, y = y, data = df, hue = cluster_col_name, cmap = zpalette)
    
    # plot the centroids as Xs
    centroids.plot.scatter(y=y, x= x, ax=plt.gca(), alpha=.60, s=500, c='black', marker = 'x')


##################### Inertia plotter

def plot_inertia(X_df, k_range_start = 2, k_range_end = 10):
    '''
    This function takes in a dataframe (scaled)
    And plots the change in inertia 
    Optional argument to change the range
    '''
    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(9, 6))
        pd.Series({k: KMeans(k).fit(X_df).inertia_ for k in range(k_range_start, k_range_end)}).plot(marker='x')
        plt.xticks(range(k_range_start -1, k_range_end))
        plt.xlabel('k')
        plt.ylabel('inertia')
        plt.title('Change in inertia as k increases')

#####################

