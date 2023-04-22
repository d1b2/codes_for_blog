import sqlite3
import pandas as pd
# importing everything from transform
from transform import *

#getting tranformed datasets from transform
df1,df2=initate_transformation()
#creating connection to sqlite database
conn=sqlite3.connect('basic_etl\penguin.db')
#writing data from dataframes to sqlite tables
df1.to_sql("penguin_study",conn,if_exists='replace',index=False)
df2.to_sql("penguin_size",conn,if_exists='replace',index=False)
#creating cursor object for query
cur=conn.cursor()
#querying all data from penguin_study table
for row in cur.execute("SELECT * FROM penguin_study LIMIT 5"):
    print(row)
#closing connection to sqlite database
conn.close()