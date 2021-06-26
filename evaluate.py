import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import SelectKBest, f_regression, RFE


################################################################################################

def select_kbest(X, y, k, score_func=f_regression):
    '''
    takes in the predictors (X), the target (y), and the number of features to select (k) 
    and returns the names (in a list) of the top k selected features based on the SelectKBest class
    Optional arg: score_func. Default is f_regression. other options ex: f_classif 
    '''
    # create selector
    f_selector = SelectKBest(score_func=score_func, k=k)
    
    #fit to X and y
    f_selector.fit(X, y)
    
    # return the list of the column names that are the top k selected features
    return list(X.columns[f_selector.get_support()])


################################################################################################

def rfe(X, y, n, estimator=LinearRegression()):
    '''
    takes in the predictors (X), the target (y), and the number of features to select (n) 
    and returns the names (in a list) of the top k selected features based on the Recursive Feature Elimination class
    Optional arg: estimator. Default is LinearRegression()
    '''
    # use the estimator model to create estimator
    est = estimator
    
    # set up with estimator and n_features
    rfe = RFE(estimator=est, n_features_to_select=n)
    
    # fit to X and y
    rfe.fit(X, y)
    
    # return the list of the columns 
    
    return list(X.columns[rfe.support_])

################################################################################################

# create basline 
def get_mean_baseline(train, validate, test):
    '''
    function takes in train validate test.
    Adds column with the baseline predictions based on the mean of train to each dataframe.
    returns train, validate, test
    '''
    train['baseline'] = train.abs_logerror.mean()
    validate['baseline'] = train.abs_logerror.mean()
    test['baseline'] = train.abs_logerror.mean()
    
    return train, validate, test

################################################################################################

def compare_rmse(df_pred_actuals):
    '''
    This function takes in a list of tuples ex 
    [('df_name', df.pred1, df.actuals), 
    ('df_name2', df.pred2, y_validate)]
    unpacks the tuple, and prints out the Root Mean Squared Error for each
    First arguement of the tuple should be the dataframe name i.e. train or validate AS A STRING
    '''
    for df_name, prediction, actual in df_pred_actuals:
        
        rmse = mean_squared_error(prediction, actual, squared = False)
               
        print(f'{df_name} RMSE for {prediction.name}: {rmse} ')


################################################################################################

# this function has some issues 
def regression_modeler_for_validating(X_cols, cols, train, validate, model= LinearRegression(), model_name = 'model'):
    '''
    This function creates regression model 
    Takes in X_train, y_train, the model with the parameters you want (default is LinearRegression())
    The name of your model as a string (for naming your column)
    '''
    
    #fit model
    model.fit(train[X_cols], train[y_col])
    
    #put predictions in train dataframe
    train[model_name] = model.predict(train[X_cols])
    
    #put predictions in validate dataframe
    validate[model_name] = model.predict(validate[X_cols])
    
    #print confirmation instead of returning something
    print(f'{model_name} has been created and added to train and validate dataframes\n')
    
    # compare the RMSEs (this function prints out RMSE comparisons 
    compare_rmse([('train', train[model_name], train[y_col]), ('validate', validate[model_name], validate[y_col])])
    
################################################################################################
    
def compare_to_basline(df, actuals, model_name, baseline = 'baseline'):
    '''
    this function takes in a dataframe (i.e. train)
    the actuals (i.e. y_train)
    the name of the column where your model's predictions are in the dataframe
    baseline = name of the column where your baseline predictions are stored, 
    default is 'baseline'
    function prints out the RMSE for the df predictions, baseline, and whether or not 
    it is better than the baseline
    '''
    # get name of dataframe entered
    name =[x for x in globals() if globals()[x] is df][0]
    
    # calculate model RMSE
    rmse = mean_squared_error(df[model_name], actuals, squared = False)
    
    # calculate baseline RMSE 
    rmse_b = mean_squared_error(df[baseline], actuals, squared = False)
    
    # print it all out
    print(f'''------- {name} ---------\n
RMSE for {model_name}: {rmse}\n
RMSE for baseline: {rmse_b}\n
Better than baseline?: {rmse < rmse_b}
        ''')
################################################################################################

# Create function to do seperate dataframes for old and new
def old_new(df):
    '''
    '''
    # old
    df_old = df[df['built_before_1978'] == 1]
    
    # new
    df_new = df[df['built_before_1978'] == 0]
    
    return df_old, df_new

################################################################################################

# maybe in the future add creating the preditions and the residuals if none were entered 
# have to import sklearn stuff

def plot_the_dots(actuals, predictions, residuals):
    '''
    This function takes in the actuals (i.e. df.actuals), predictions, and residuals and outputs two graphs.
    One to see the regression line and the actuals/predictions
    One to see the actuals vs the residuals.
    '''
    
    r_sq = r2_score(actuals, predictions)
    rmse = mean_squared_error(actuals, predictions, squared = False)
    
    text_loc = actuals.max() - 2
    
    # plots actual vs predicted
    plt.figure(figsize=(16, 7))
    ax = plt.subplot(1, 2, 1)
    ax.scatter(actuals, predictions, label='predicted')
    ax.set(title='Actual vs Predicted Value', ylabel='Prediction', xlabel='Actual')
    ax.plot(actuals, actuals, ls=':', c='gray')
    ax.text(text_loc, 1, f'R^2: {r_sq:.2f}', fontsize='large')
    
    #put r^2 value on graph
    # and rmse and rmse of baseline
    
    ax = plt.subplot(1, 2, 2)
    ax.scatter(actuals, residuals)
    ax.set(title = 'Actual vs Residual',ylabel='Residual', xlabel='Actual')
    ax.hlines(0, *ax.get_xlim(), ls=':', color='gray')
    ax.text(text_loc, -3, f'RMSE: {rmse:.2f}')


################################################################################################

def plot_residuals(df, x_list, palette = "tab10"):
    '''
    This function takes in a dataframe and a list of all the risiduals you would like to plot (that means the names of the columns)
    '''
    color_list= list(sns.color_palette(palette))
    fig, ax = plt.subplots(figsize=(10, 5))
    for x, c in zip(x_list, color_list):
        sns.histplot(x = x, data = df, kde=True, ax = ax, alpha = 0.5, color = c, legend=True, lw = .1)
    
    plt.legend(x_list)  
    plt.show()

#####################################Compare RMSE function##########################################

def compare_rmse(pred_actuals):
    '''
    This function takes in a list of tuples ex [(df.pred1, df.actuals), (df.pred2, y_validate)]
    unpacks the tuple, and prints out the Root Mean Squared Error for each 
    '''
    for prediction, actual in pred_actuals:
        rmse = mean_squared_error(prediction, actual, squared = False)
        print(f'RMSE for {prediction.name}: {rmse} ')