import configparser
import json
import os
import sys

config = configparser.RawConfigParser()

config_dir = os.path.dirname(os.path.abspath(__file__))
print("Config directory:", config_dir)

config_dir_path = os.path.normpath(config_dir + os.sep + os.pardir)

# --- Read API properties ---
api_properties_path = os.path.join(config_dir_path, 'config', 'api_properties.properties')
print("API Properties Path:", api_properties_path)

config.read(api_properties_path)

coordinates_files_path = os.path.join(config_dir_path, 'config', 'cities_coordinates.json')

open_weather_api_key = config.get('open_weather_api_properties', 'open_weather_api_key')
open_weather_base_url = config.get('open_weather_api_properties', 'open_weather_base_url')

print("OpenWeather Base URL:", open_weather_base_url)
print("OpenWeather API Key:", open_weather_api_key)
print("Coordinates File Path:", coordinates_files_path)

# --- Read PostgreSQL DB properties ---
postgresql_files_path = os.path.join(config_dir_path, 'config', 'postgresql_db_properties.json')
print("PostgreSQL DB Properties Path:", postgresql_files_path)

# --- Local output path ---
write_local_files_path = os.path.join(config_dir_path, 'output', 'finalOpenWeatherData.csv')
print("Local Write Path:", write_local_files_path)

# --- Read AWS S3 properties ---
aws_s3_properties_path = os.path.join(config_dir_path, 'config', 'aws_s3.properties')
print("AWS S3 Properties Path:", aws_s3_properties_path)

aws_s3_config = configparser.RawConfigParser()
aws_s3_config.read(aws_s3_properties_path)

aws_access_key_id = aws_s3_config.get('AWS', 'AWS_ACCESS_KEY')
aws_secret_access_key = aws_s3_config.get('AWS', 'AWS_SECRET_KEY')
aws_region_name = aws_s3_config.get('AWS', 'AWS_REGION')

print("AWS S3 Config Loaded.")
