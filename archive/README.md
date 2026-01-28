# 🌱 LMNH Plant Monitoring Archive script

## Files
- `archive.py`: Loads the relevant data from the database.

## Quick Start

To run the the archive script, run the following command:

```
python3 archive.py
```
## Environment Variables

# Database connection
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_HOST=your-db-hostname
DB_PORT=1433
DB_NAME=your-database-name
DB_USERNAME=your-username
DB_PASSWORD=your-password

# S3 configuration
S3_BUCKET=c21-charn-archive-bucket
S3_PREFIX=archive/

## How it works

The script connects to the SQL Server database using environment variables for the connection details.

It queries the recording table for rows where recording_taken is older than 24 hours.

The results are written to a CSV file stored temporarily locally.

The CSV file is uploaded to an S3 bucket, using a date based filename.

Once the upload is successful, the archived rows are deleted from the database.

The database connection is then closed and the script exits.

