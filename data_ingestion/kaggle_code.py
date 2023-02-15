import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi
import re




kaggle_url="https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database?select=diabetes.csv"

def dataset_and_file_name(kaggle_url:str):
    kaggle_url = re.split(r'[/?=]', kaggle_url)
    file=kaggle_url[-1]
    dataset="/".join(kaggle_url[-4:-2])
    return dataset,file

def get_kaggle_username_key(kaggle_json_path:str):
    with open(kaggle_json_path) as user:
        user_info=json.load(user)
    return user_info['username'],user_info['key']

def download_kaggle_dataset(path:str):
    username,key=get_kaggle_username_key(".kaggle\kaggle.json") 
    os.environ['KAGGLE_USERNAME'] = username
    os.environ['KAGGLE_KEY'] = key    

    api = KaggleApi()
    api.authenticate()
    dataset,file=dataset_and_file_name(kaggle_url)
    api.dataset_download_file(dataset, file, path)
    

download_kaggle_dataset('data_ingestion/kaggle_artifacts')





