import pandas as pd
# importing everything from extract
from extract import *


def get_categotical_numerical_columns(dataframe):
    """
    function to get lists of categorical and numerical columns from dataframe

    Args:
        dataframe (pandas.DataFrame): dataframe 

    Returns:
       num_columns (list): list of numerical columns of input dataframe
       cat_columns (list): list of categorical columns of input dataframe
    """
    num_columns=[i for i in dataframe.columns if dataframe[i].dtype!='object']
    cat_columns=[i for i in dataframe.columns if dataframe[i].dtype=='object'] 
    return num_columns,cat_columns


def handle_null_values(dataframe):
    """
    function to replace null values in dataframe

    Args:
        dataframe (pandas.DataFrame): dataframe 

    Returns:
        dataframe (pandas.DataFrame): dataframe with no null values
    """
    #getting list of numerical and categorical columns
    num_columns,cat_columns=get_categotical_numerical_columns(dataframe)    
    #replace null vales in numerical columns with mean value of each column
    for i in num_columns:
        dataframe[i] = dataframe[i].fillna((dataframe[i].mean()))
     #replace null vales in categorical columns with mode value of each column
    for i in cat_columns:
        dataframe[i] = dataframe[i].fillna((dataframe[i].mode()[0]))   
    return dataframe
    


def correct_column_name(dataframe):
    """
    function to correct column names of dataframe

    Args:
        dataframe (pandas.DataFrame): dataframe 

    Returns:
        dataframe (pandas.DataFrame): dataframe with column names spaces replaced with _
    """    
    dataframe.columns = dataframe.columns.str.replace(' ', '_')
    return dataframe



def initate_transformation():
    """
    function to get transformed dataframes

    Returns:
        df1 (pandas.DataFrame): transformed dataframe with no null values 
                                and correct column name
        df2 (pandas.DataFrame): transformed dataframe with no null values 
                                and correct column name
    """
    #getting tranformed datasets from extract
    df1,df2=create_dataframes_remove_csv_files('basic_etl/artifacts')
    # call to handle_null_values function for both the dataframes
    df1=handle_null_values(df1)
    df2=handle_null_values(df2)
    # call to correct_column_name function for both the dataframes
    df1=correct_column_name(df1)
    df2=correct_column_name(df2)
    return df1,df2
