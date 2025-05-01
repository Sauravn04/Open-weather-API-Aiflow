# dags/src/coordinate_mapping.py

from utilites import json_reader
from utilites.upload_to_s3 import upload_file_to_s3
import psycopg2
import requests
import os
import json
from sqlalchemy import create_engine
import pandas as pd
from unicodedata import normalize

# Debugging: Check API Key and Base URL
print("OpenWeather API Key:", json_reader.open_weather_api_key)
print("OpenWeather Base URL:", json_reader.open_weather_base_url)

def df_map_base_url_with_coordinates():
    print("Fetching API responses...")
    with open(json_reader.coordinates_files_path, "r") as f:
        data = json.load(f)
    
    response_list = []

    for i in data:
        base_url = (
            json_reader.open_weather_base_url
            + "?"
            + "lat=" + str(i["Lat"])
            + "&lon=" + str(i["Long"])
            + "&appid=" + json_reader.open_weather_api_key
            + "&units=metric"
        )

        response = requests.get(base_url)
        
        if response.status_code == 200:
            response_list.append(response.json())
        else:
            print(f"Failed API call for {i['Lat']},{i['Long']}: {response.status_code} - {response.text}")

    if not response_list:
        raise Exception("No successful API responses received.")

    df = pd.json_normalize(
        response_list,
        "weather",
        [
            "base",
            "visibility",
            "dt",
            "timezone",
            "name",
            "cod",
            ["coord", "lon"],
            ["coord", "lat"],
            ["main", "temp"],
            ["main", "feels_like"],
            ["main", "temp_min"],
            ["main", "temp_max"],
            ["main", "pressure"],
            ["main", "humidity"],
            ["main", "sea_level"],
            ["main", "grnd_level"],
            ["wind", "speed"],
            ["wind", "deg"],
            ["wind", "gust"],
            ["clouds", "all"],
            ["sys", "country"],
            ["sys", "sunrise"],
            ["sys", "sunset"],
            ["sys", "type"],
            ["sys", "id"],
        ],
        errors="ignore",
    )

    print("API responses fetched and dataframe created.")
    return df

def data_cleansing(dataframe):
    print("Starting data cleansing...")

    # Replace NaN values
    def replace_nan(x):
        if pd.isna(x):
            if isinstance(x, str) or pd.api.types.is_object_dtype(type(x)):
                return "null"
            else:
                return 0
        return x

    dataframe = dataframe.applymap(replace_nan)

    # Decode city name to ASCII
    dataframe["name"] = dataframe["name"].apply(
        lambda x: normalize("NFD", x).encode("ascii", "ignore").decode("utf-8-sig")
    )

    # Convert timestamp to datetime
    dataframe["date_time"] = pd.to_datetime(dataframe["dt"], unit="s")

    # Rename columns: Replace dots with underscores
    dataframe.rename(columns=lambda x: x.replace(".", "_"), inplace=True)

    print("Data cleansing done.")
    return dataframe

def write_to_postgres_db(dataframe):
    print("Writing to Postgres Database...")

    with open(json_reader.postgresql_files_path, "r") as f:
        db_params = json.load(f)

    connection_string = (
        f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}"
        f"@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
    )

    print(f"Connecting to DB with: {connection_string}")

    engine = create_engine(connection_string)

    table_name = "open_weather_api_tbl"
    schema_name = "public"  # Schema should already exist

    dataframe.to_sql(
        table_name,
        engine,
        schema=schema_name,
        if_exists="append",
        index=False
    )

    print("Data inserted successfully into Postgres.")

def write_to_local(dataframe):
    print("Writing data locally...")
    dataframe.to_csv(json_reader.write_local_files_path, index=False)
    print("Data written to local CSV successfully.")

    # Upload to S3 after writing locally
    print("Uploading to S3...")
    bucket_name = 'Your_bucket-name'  # <-- Change this to your real bucket name
    file_path = json_reader.write_local_files_path
    s3_key = 'weather-data/finalOpenWeatherData.csv'

    upload_file_to_s3(file_path, bucket_name, s3_key)

    print("File uploaded to S3 successfully.")

# Main ETL execution
if __name__ == "__main__":
    try:
        df = df_map_base_url_with_coordinates()
        df_clean = data_cleansing(df)

        # Uncomment whatever you want to run
        write_to_postgres_db(df_clean)
        write_to_local(df_clean)

    except Exception as e:
        print("An error occurred:", e)
