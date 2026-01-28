# 🌱 LMNH Plant Monitoring Archive script

## Files
- `archive.py`: Loads the relevant data from the database.

## Quick Start

To run the the archive script, run the following command:

```
python3 archive.py
```
## How it works

The script connects to the SQL Server database using environment variables for the connection details.

It queries the recording table for rows where recording_taken is older than 24 hours.

The results are written to a CSV file stored temporarily locally.

The CSV file is uploaded to an S3 bucket, using a date based filename.

Once the upload is successful, the archived rows are deleted from the database.

The database connection is then closed and the script exits.

## Docker & Uploading Image to AWS ECR

If you want to upload a Docker image of this archive to your AWS ECR, run the following:

```
sh dockerise.sh
```

You will be given prompts to enter your `AWS_ACCOUNT_ID`, `AWS_REGION`, and `AWS_ECR_REPO` name. These can all be found on AWS.