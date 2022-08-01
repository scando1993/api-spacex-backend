import json

import time
import sys
import site
import datetime
import random
import pandas as pd
import ijson

import io
import requests
import urllib.parse as par

from datetime import datetime

# Class for Api Spacex, the default url for db is localhost
# When the class is created it checks connection to database
# The load method should be called only once but it depends on
# how the user would use the api

class ApiSpacex:
    def __init__(self, db_url='http://localhost:9000/', json_url=''):
        self.db_url = db_url
        self.db_name = ''
        self.json_url = json_url
        self.data = []
        self.success = 0
        self.fail = 0
        self.connect_db()
        self.df = {}

    def connect_db(self):
        r = requests.get(self.db_url)
        if r.status_code == 200:
            print('Connection Successfull')
        else:
            print('Database not connected')

    def create_db(self, name='starlink_historical'):
        ## create table query
        self.db_name = name
        q = f'create table {name} (CREATION_DATE timestamp, ID string, LATITUDE double, LONGITUDE double)'

        r = requests.get(self.db_url + 'exec?query=' + q)
        if r.status_code == 200:
            print('Database created successfully')
        else:
            print('Database already created')

    def load_from_json(self, path, local_store=True, db_store=True, df=True):
        with open(path, 'rb') as f:
            for record in ijson.items(f, 'item'):
                if local_store:
                    self.data.append(
                        {'creation_date': record['spaceTrack']['CREATION_DATE'],
                         'longitude': record['longitude'],
                         'latitude': record['latitude'],
                         'id': record['id']})
                if db_store:
                    self.add_position({
                        'creation_date': "'" + record['spaceTrack']['CREATION_DATE'] + "'",
                        'latitude': record['latitude'],
                        'longitude': record['longitude'],
                        'id': "'" + record['id'] + "'"
                    })
        if local_store and df:
            self.df = pd.DataFrame(self.data)
            self.df['creation_date'] = pd.to_datetime(self.df['creation_date'])

    def add_position(self, obj):
        query = f'insert into {self.db_name} ' \
                f'values({obj["creation_date"]}, {obj["id"]}, {obj["latitude"]}, {obj["longitude"]})'
        r = requests.get(self.db_url + "exec?query=" + query)
        if r.status_code == 200:
            self.success += 1
        else:
            self.fail += 1

    def query(self, query, parse_dates=True):
        req = requests.get(self.db_url + "exp?query=" + requests.utils.quote(query))
        rawData = req.text

        df = pd.read_csv(io.StringIO(rawData), parse_dates=['CREATION_DATE'])
        print(df.columns)
        return df

    def find_last_position(self, id, timestamp=None):
        if timestamp is not None:
            q = f"select * from {self.db_name} where ID='{id}' and CREATION_DATE='{timestamp}'"
        else:
            q = f"select * from {self.db_name} where ID='{id}'"

        return self.query(q)

    def find_last_position_between_dates(self, id, start_date, end_date):
        q = f"select * from {self.db_name} where ID='{id}' and CREATION_DATE >= '{start_date}' and CREATION_DATE < '{end_date}'"
        return self.query(q)

    def find_closest_satellite(self, latitude, longitude, timestamp):
        q = f"select * from {self.db_name} where CREATION_DATE={'timestamp'}"

        return self.query(q)


if __name__ == '__main__':
    cl = ApiSpacex()
    cl.create_db()
    cl.load_from_json('starlink_historical_data.json')
    print(cl.find_last_position('5eed7716096e5900069857b2', '2021-01-26T13:16:10.000000Z'))
    print(cl.find_last_position_between_dates('5eed7716096e5900069857b2',
                                              '2021-01-24T13:16:10.000000Z',
                                              '2021-01-28T13:16:10.000000Z'))
