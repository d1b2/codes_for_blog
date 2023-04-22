import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi
import re
import pandas as pd
import shutil



kaggle_url="https://www.kaggle.com/datasets/parulpandey/palmer-archipelago-antarctica-penguin-data"


def get_dataset_name(kaggle_url:str):
    """function to get dataset name from kaggle_url

    Args:
        kaggle_url (str): kaggle url where dataset is present

    Returns:
        dataset_name (str): name of dataset
    """
    kaggle_url = re.split(r'[/]', kaggle_url)    
    dataset_name="/".join(kaggle_url[-2:])
    return dataset_name


def get_kaggle_username_key(kaggle_json_path:str):
    """function to get username and key of kaggle api 

    Args:
        kaggle_json_path (str): file path where kaggle.json is present

    Returns:
        user_info['username'] : username in kaggle api
        user_info['key']: key in kaggle api
    """
    with open(kaggle_json_path) as user:
        user_info=json.load(user)
    return user_info['username'],user_info['key']


def authenticate_download_kaggle_files(path:str):
    """function to authenticate kaggle api and download files

    Args:
        path (str): path of directory where downloaded files will be saved
    """
    #get username and key
    username,key=get_kaggle_username_key("data_ingestion\.kaggle\kaggle.json") 
    #setup environment variables
    os.environ['KAGGLE_USERNAME'] = username
    os.environ['KAGGLE_KEY'] = key    

    #instantiate to KaggleApi
    api = KaggleApi()
    #authenticate api instance
    api.authenticate()
    #get dataset name
    dataset_name=get_dataset_name(kaggle_url)
    #download and unzip all files present in dataset_name
    api.dataset_download_files(dataset_name,unzip=True,path=path)
    

def create_dataframes_remove_csv_files(path):
    """function to create dataframes and remove csv files

    Args:
        path (str): path of directory where csv files are present

    Returns:
        df1(pandas.DataFrame): dataframe generated from first csv file present at path
        df2(pandas.DataFrame): dataframe generated from second csv file present at path
    """
    # downloading csv files at path
    authenticate_download_kaggle_files(path)
    # getting list of files present in path
    file_list=os.listdir(path) 
    #creating path for dataframe   
    df1_path=os.path.join(path,file_list[0])
    #creating dataframe
    df1=pd.read_csv(df1_path)
    df2_path=os.path.join(path,file_list[1])
    df2=pd.read_csv(df2_path)
    #removing csv files and folder present at path
    shutil.rmtree(path, ignore_errors=False)
    
    return df1,df2

