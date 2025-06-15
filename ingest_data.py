

import argparse
import os 
import pandas as pd 
from sqlalchemy import create_engine
from time import time


def main(params):

    user = params.user 
    password = params.password 
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name 
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else: 
        csv_name = 'output.csv'


    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    



    df_iter = pd.read_csv(f'{csv_name}', iterator=True, chunksize=100000)

    df = next(df_iter)

    # Convert the datetime to date formats. To make the db clean
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    # In[62]:


    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    df.head(n=0).to_sql(name = table_name, con = engine, if_exists = 'replace')

    t_start = time()
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    t_end = time()
    print('Inserted first chunk..., took %.3f seconds' % (t_end - t_start))


    for df in df_iter:
        t_start = time()
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        df.to_sql(name = table_name, con = engine, if_exists = 'append', index = False)

        t_end = time()

        print('Inserted another chunk..., took %.3f seconds' % (t_end - t_start))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Ingest csv data to postgres')


    parser.add_argument('--user', help = 'File path to the csv file')
    parser.add_argument('--password', help = 'Password for the postgres user')
    parser.add_argument('--host', help = 'Host for the postgres server')    
    parser.add_argument('--port', help = 'Port for the postgres server')
    parser.add_argument('--db', help = 'Name of the postgres database')
    parser.add_argument('--table_name', help = 'Name of the table to ingest data into')
    parser.add_argument('--url', help = 'url of the csv file')

    args = parser.parse_args()

    main(args)

