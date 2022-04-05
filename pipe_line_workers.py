import pandas as pd
import requests
import json

from sqlalchemy import create_engine

def get_data(url='https://randomuser.me/api/?results=300&nat=de,dk,fr,gb&inc=id,gender,name,location,email,dob,picture,nat&seed=flightright'):
    req = requests.request("GET", url)
    json_dict = json.loads(req.text)
    df = pd.json_normalize(json_dict, 'results', sep='_')

    return df

def transform_data(df):
    df['dob_date'] = pd.to_datetime(df['dob_date'])
    df['location_timezone_offset'] = pd.to_numeric(df['location_timezone_offset'].str[:-3])
    df['location_coordinates_latitude'] = pd.to_numeric(df['location_coordinates_latitude'])
    df['location_coordinates_longitude'] = pd.to_numeric(df['location_coordinates_longitude'])

    return df

def agregate_data(df):
    df_out = df.groupby(['location_country']).agg({'email': 'count',
                                               'dob_age': 'mean'}).reset_index()

    gender_table = pd.pivot_table(df, index='location_country', 
            columns='gender', 
            values='email', aggfunc='count'
            ).reset_index()

    df_out = df_out.join(gender_table.set_index('location_country'), on='location_country')
    df_out.columns = ['location_country', 'entries_count', 'avg_age', 'female_count', 'male_count']

    return df_out

df = get_data()
df_transformed = transform_data(df)
df_out = agregate_data(df_transformed)

df_transformed.to_csv('out.csv', sep=';', index=False)

engine = create_engine('postgresql://postgres:postgres@pgsql:5432/postgres')
try: df.to_sql('person', engine, if_exists='append', index=False)
except Exception as e: print(e) 

df_out.to_csv('statistics.csv', sep=';', index=False)