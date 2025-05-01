# dags/src/utilites/upload_to_s3.py
import boto3
import configparser
import os


def upload_file_to_s3(file_path, bucket_name, s3_key):
    # Read AWS credentials
    config = configparser.RawConfigParser()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.normpath(os.path.join(current_dir, "..", "config"))
    config_path = os.path.join(config_dir, "aws_s3.properties")

    config.read(config_path)

    aws_access_key_id = config.get("AWS", "AWS_ACCESS_KEY")
    aws_secret_access_key = config.get("AWS", "AWS_SECRET_KEY")
    region = config.get("AWS", "AWS_REGION")

    # Create S3 client
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region,
    )

    # Upload file
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Successfully uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise


if __name__ == "__main__":
    # Change these manually for testing
    bucket_name = "your_bucket"  # <- Change this
    file_path = "D:/openWeatherAPI-Airflow/dags/src/output/finalOpenWeatherData.csv"  # <- Change this
    s3_key = "weather-data/finalOpenWeatherData.csv"

    upload_file_to_s3(file_path, bucket_name, s3_key)
