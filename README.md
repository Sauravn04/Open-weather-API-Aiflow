# Open-weather-API-Aiflow
This is an automated weather ETL pipeline project
# 🌦️ OpenWeather API ETL Pipeline with Apache Airflow

This project is a data pipeline that extracts weather data from the [OpenWeather API](https://openweathermap.org/api), transforms it using Python scripts, loads it into a PostgreSQL database, and stores a backup in an AWS S3 bucket. The pipeline is orchestrated using Apache Airflow and containerized using Docker Compose.

---

## 🚀 Features

- ⛅ Fetches current weather data for specified cities from OpenWeather API
- 🧮 Stores structured weather data in PostgreSQL
- ☁️ Uploads processed weather files to AWS S3
- 📅 Scheduled and managed using Apache Airflow (via Docker)

---

## 🧰 Tech Stack

- **Python**
- **Apache Airflow**
- **Docker & Docker Compose**
- **PostgreSQL**
- **AWS S3**
- **OpenWeather API**

---

## 🗄️ Data Model

### Tables

#### `city`
| Column      | Type     | Description             |
|-------------|----------|-------------------------|
| city_id     | INT (PK) | Unique city identifier  |
| name        | VARCHAR  | City name               |
| country     | VARCHAR  | Country code (e.g., IN) |
| latitude    | FLOAT    | Latitude coordinate     |
| longitude   | FLOAT    | Longitude coordinate    |

#### `weather`
| Column              | Type     | Description                    |
|---------------------|----------|--------------------------------|
| weather_id          | SERIAL   | Primary key                    |
| city_id             | INT (FK) | Linked to `city` table         |
| datetime_utc        | TIMESTAMP | Timestamp of data             |
| temperature         | FLOAT    | Temperature in Celsius         |
| humidity            | INT      | Humidity percentage            |
| pressure            | INT      | Atmospheric pressure           |
| wind_speed          | FLOAT    | Wind speed in m/s              |
| wind_deg            | INT      | Wind direction in degrees      |
| weather_main        | VARCHAR  | Weather category (e.g. Clouds) |
| weather_description | TEXT     | Detailed weather description   |
| clouds              | INT      | Cloudiness percentage          |

#### `s3_uploads` (optional)
| Column     | Type     | Description              |
|------------|----------|--------------------------|
| upload_id  | SERIAL   | Primary key              |
| file_name  | VARCHAR  | Name of the file uploaded|
| upload_time| TIMESTAMP| Timestamp of upload      |
| status     | VARCHAR  | Upload status            |

---

## 🧑‍💻 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/openweather-etl-airflow.git
cd openweather-etl-airflow

