import sys, os

# Step 1: Set project root path first
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Step 2: Now import modules
from src.coordinate_mapping import (
    df_map_base_url_with_coordinates,
    data_cleansing,
    write_to_postgres_db,
    write_to_local,
)

if __name__ == "__main__":

    try:
        print("Fetching data from OpenWeather API...")
        api_dataframe = df_map_base_url_with_coordinates()
        print("Data fetched successfully.")

        print("Starting data cleansing...")
        cleaned_dataframe = data_cleansing(dataframe=api_dataframe)
        print("Data cleansing completed.")

        print("Writing data to PostgreSQL database...")
        write_to_postgres_db(dataframe=cleaned_dataframe)
        print("Data written to database.")

        print("Saving data to local CSV and uploading to S3...")
        write_to_local(dataframe=cleaned_dataframe)
        print("Data saved locally and uploaded to S3.")

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        print("Job completed.")
