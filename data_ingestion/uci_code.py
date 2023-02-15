import os
import urllib.request as request
from pathlib import Path
from zipfile import ZipFile
import numpy as np
import pandas as pd



uci_url="https://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.zip"

def download_rawfile(path:str): 
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path,"data.zip").replace("\\","/")
    request.urlretrieve(uci_url,filename) 
    return filename


def unzip_raw(path:str,path_to_unzip:str):
    filename=download_rawfile(path)
    with ZipFile(file=filename, mode="r") as zf:
        zf.extractall(path_to_unzip)

def list_unzip_files(path_to_unzip:str):
    file_list=[]
    for f in os.listdir(path_to_unzip):
        file_list.append(os.path.join(path_to_unzip,f).replace("\\","/"))
    return file_list

    
def get_headers(path_to_header:str):
    file1 = open(path_to_header, 'r')
    Lines = file1.readlines()
    header=[]
    # Strips the newline character and splits with : charater and select the first part
    for i in range(34,90):
        header.append(Lines[i].strip().split(':')[0])
    header.append("Spam/No_Spam")
    return header


def saving_data(filelist:list,path_to_csv:str):
    header=get_headers(filelist[-1])
    clean_df=pd.read_csv(filelist[0],sep=",",names=header)
    if not os.path.exists(path_to_csv):
        os.makedirs(path_to_csv)
    csvfilepath = os.path.join(path_to_csv,"data.csv").replace("\\","/")
    clean_df.to_csv(csvfilepath,index=False)
    return csvfilepath

def train_test(csvfilepath:str,path_to_train_test:str):
    clean_dataframe=pd.read_csv(csvfilepath)
    if not os.path.exists(path_to_train_test):
        os.makedirs(path_to_train_test)
    
    train_dataframe,test_dataframe=clean_dataframe[:4000],clean_dataframe[4000:]
    train_filepath=os.path.join(path_to_train_test,"train.csv").replace("\\","/")
    test_fielpath=os.path.join(path_to_train_test,"test.csv").replace("\\","/")

    train_dataframe.to_csv(train_filepath,index=False)
    test_dataframe.to_csv(test_fielpath,index=False)

path='data_ingestion/uci_artifacts/raw_data'
path_to_unzip='data_ingestion/uci_artifacts/unzip_data'
path_to_csv='data_ingestion/uci_artifacts/clean_data'
path_to_train_test='data_ingestion/uci_artifacts/clean_data/train_test'

unzip_raw(path=path,path_to_unzip=path_to_unzip)
filelist=list_unzip_files(path_to_unzip=path_to_unzip)

csvfilepath=saving_data(filelist=filelist,path_to_csv=path_to_csv)
train_test(csvfilepath=csvfilepath,path_to_train_test=path_to_train_test)