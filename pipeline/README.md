# LMNH Plant ETL Pipeline

## Environment Variables

There must be a `.env` file in the `pipeline` directory with the following contents:

```
DB_HOST=XXXX
DB_PORT=1433
DB_USERNAME=XXXX
DB_PASSWORD=XXXX
DB_NAME=XXXX
DB_SCHEMA=XXXX
DB_DRIVER=ODBC Driver 18 for SQL Server

AWS_ACCOUNT_ID = XXXX
AWS_REPO_NAME  = XXXX
AWS_REGION          = XXXX
```

## Quick Start

To run the entire ETL pipeline from start to finish, run the following:

```
python pipeline.py
```

This will extract data from the plant API, clean the data, and upload the data to the RDS.


## Docker & Uploading Image to AWS ECR

If you want to upload a Docker image of this pipeline to your AWS ECR, run the following:

```
sh dockerise.sh
```
