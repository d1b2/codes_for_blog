import os
from pathlib import Path
import pandas as pd
import yaml

#Step1 Get data 
def load_dataframes(path_to_df:Path):
    dataframe=pd.read_csv(path_to_df)
    #print('Data frame recieved')
    return dataframe  

#Step2 Create Schema and get contnets of schema.yaml
def read_yaml(path_to_yaml: Path) :  
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return content
    except yaml.YAMLError as exception:
        print(exception)

#Validation starts
#Step3 Validate Number of rows
def validate_rows(dataframe,schema,n,d,s,v):
    n.append('Number of Row')
    d.append(len(dataframe))
    s.append(schema['rows'])
    v.append(len(dataframe)==schema['rows'])
    #print(f"Number of rows Validated : {len(dataframe)==schema['rows']}")

#Step4 Validate Number of columns  
def validate_columns(dataframe,schema,n,d,s,v):
    n.append('Number of Column')
    d.append(len(dataframe.columns))
    s.append(len(schema['columns']))
    v.append(len(dataframe.columns)==len(schema['columns']))
    #print(f"Number of columns Validated : {len(dataframe.columns)==len(schema['columns'])}")  

#Step5 Validate datatypes of columns
def validate_dataype_columns(dataframe,schema,n,d,s,v):
    for i in dataframe.columns:
        n.append(f'Datatype of {i} column')
        d.append(dataframe.dtypes[i])
        s.append(schema['columns'][i])
        v.append(dataframe.dtypes[i]==schema['columns'][i])
        #print(f"{i} column datatype validated : {dataframe.dtypes[i]==schema['columns'][i]}")

#Step6 Validate minimum value of columns
def validate_min_columns(dataframe,schema,n,d,s,v):
    for i in ('Age','Outcome'):
        n.append(f'Minimum of {i} column')
        d.append(dataframe[i].min())
        s.append(schema['min_of_column'][i])
        v.append(dataframe[i].min()==schema['min_of_column'][i])
        #print(f"{i} column minimum value validated : {dataframe[i].min()==schema['min_of_column'][i]}") 

#Step7 Validate maximum value of columns
def validate_max_columns(dataframe,schema,n,d,s,v):
    for i in ('Age','Outcome'):
        n.append(f'Maximum of {i} column')
        d.append(dataframe[i].max())
        s.append(schema['max_of_column'][i])
        v.append(dataframe[i].max()==schema['max_of_column'][i])
        #print(f"{i} column maximum value validated : {dataframe[i].max()==schema['max_of_column'][i]}") 

#Step8 Generate Data Validation Report
def create_validation_report_df(path_dir,n,d,s,v):
    report = pd.DataFrame({
                'Validation' : n,    
                'Dataframe_Value' : d,
                'Schema_Value' : s,
                'Validation_Status' : v})
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)
            
    report_df_filepath = os.path.join(path_dir,"validation_report.csv")
    report_html_filepath=os.path.join(path_dir,"validation_report.html")

    report.to_csv(report_df_filepath,index=False)  # csv saved
    
     # styling of dataframe is optional
    df_html_styled = report.style.set_properties(
                **{"text-align": "left","border":"1px",
                'border-color':'blue',
                'border-width':'1px',
                'border-style':'solid',
                'padding-left': '20px',
                'padding-right': '10px',
                'padding-top': '2px',
                'padding-bottom': '2px'}
                ).hide(axis="index").set_caption('Data Validation Report')
    
    df_html_styled.to_html(report_html_filepath)


#initialize variables
n,d,s,v=[],[],[],[]
#call to functions
dataframe=load_dataframes('data_ingestion/kaggle_artifacts/diabetes.csv')
schema=read_yaml('data_validation/schema.yaml')
validate_rows(dataframe,schema,n,d,s,v)
validate_columns(dataframe,schema,n,d,s,v)
validate_dataype_columns(dataframe,schema,n,d,s,v)
validate_min_columns(dataframe,schema,n,d,s,v)
validate_max_columns(dataframe,schema,n,d,s,v)
create_validation_report_df("data_validation/validation_artifact",n,d,s,v)
