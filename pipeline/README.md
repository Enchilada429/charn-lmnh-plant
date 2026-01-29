# LMNH Plant ETL Pipeline

## Environment Variables

There must be a `.env` file in the `pipeline` directory with the following contents:

```
DB_HOST=XXXX
DB_PORT=1433
DB_USER=XXXX
DB_PASSWORD=XXXX
DB_NAME=XXXX
DB_SCHEMA=XXXX
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

## Potential issues

When running `sh dockerise.sh`, you may run into this error:
```
Your session has expired. Please reauthenticate using 'aws login'.error: cannot perform an interactive login from a non TTY device
```

To fix this, ensure you have the [aws command line](https://aws.amazon.com/cli/) installed on your local machine, and then run the command `aws login`.
This should open an AWS window on your default browser, and you should select the account to authenticate. After this you're prompted to leave the site and you should be able to run `sh dockerise.sh` again.