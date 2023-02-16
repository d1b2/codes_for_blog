import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi
import re

#Step 1: Create New API token of kaggle
#Step 2: Create folder named .kaggle and paste kaggle.json in it
#Step 3: Install Kaggle by running pip install kaggle

#Step 4: Getting URL

kaggle_url="https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database?select=diabetes.csv"

#Step 5: Get filename and dataset name from kaggle_url
def dataset_and_file_name(kaggle_url:str):
    kaggle_url = re.split(r'[/?=]', kaggle_url)
    file=kaggle_url[-1]
    dataset="/".join(kaggle_url[-4:-2])
    return dataset,file

#Step 6: Getting kaggle username and key from kaggle.json
def get_kaggle_username_key(kaggle_json_path:str):
    with open(kaggle_json_path) as user:
        user_info=json.load(user)
    return user_info['username'],user_info['key']

#Step6 Authenticate Kaggle API and download dataset at designated path
def download_kaggle_dataset(path:str):
    username,key=get_kaggle_username_key(".kaggle\kaggle.json") 
    os.environ['KAGGLE_USERNAME'] = username
    os.environ['KAGGLE_KEY'] = key    

    api = KaggleApi()
    api.authenticate()
    dataset,file=dataset_and_file_name(kaggle_url)
    api.dataset_download_file(dataset, file, path)
    
#Call to function
download_kaggle_dataset('data_ingestion/kaggle_artifacts')





