#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    # use the argpare module to parse command-line arguments
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # execute a wget command to download the CSV file from URL
    os.system(f"wget {url} -O {csv_name}")

    # create a PostgreSQL database connection using the create_engine function from sqlalchemy library
    # connection parameters are taken from the command-line arguments
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # use pandas to read the CSV file in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # use first chunk to get the data types of the columns
    df = next(df_iter)

    # convert two columns to datetime format
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # creates an empty table in the PostgreSQL database with the specified name (table_name) and replaces it if it already exists.
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    # append the first chunk to the PostgreSQL table
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # continue loading subsequent chunks into the PostgreSQL table
    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            # print a message when the data ingestion process is complete
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':
    # set up command-line argument parser
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # define required command-line arguments
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    # Psparse command-line arguments
    args = parser.parse_args()

    # call the main function with the parsed arguments
    main(args)
