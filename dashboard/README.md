# 🌱 LMNH Plant Monitoring Dashboard 

This folder contains all necessary scripts and requirements to run a fully-functioning, real-time analytics dashboard for the plants in the LMNH garden. This dashboard may be ran in two ways via the CLI arguments.

## Files 📂🪷
- `load_data.py`: Loads the relevant data from the database.
- `charts.py`: Creates plots to be displayed on dashboard.
- `dashboard.py`: Main dashboard configuration.
- `archive.py`: The page where all downloadable links to past data will live.

## Running the Application 📈🌷

To run the dashboard, run the following command:

```
streamlit run dashboard.py --source [data_source]
```
- There are two options for the --source argument: 'csv' or 'db'
    - 'db': Connects to the AWS RDS for real-time streaming.
    - 'csv': This will plot the data from a CSV. The name of the CSV *must* be added as an argument when the data source is 'csv'.


## Docker & Uploading Image to AWS ECR 🐳🌾

If you want to upload a Docker image of this dashboard to your AWS ECR, run the following:

```
sh dockerise.sh
```

You will be given prompts to enter your `AWS_ACCOUNT_ID`, `AWS_REGION`. These can all be found on AWS.

### Environment Variables 🌎🌹

There must be a `.env` file in the `dashboard` directory with the following contents:

```
DB_HOST=XXXX
DB_PORT=1433
DB_USER=XXXX
DB_PASSWORD=XXXX
DB_NAME=XXXX
DB_SCHEMA=XXXX
DB_DRIVER=XXXX
```
These are necessary to connect to the RDS and thus display the data.

There must also be S3 bucket credentials for the `archive` page on the dashboard. This requires the additional credentials in the `.env`:

```
AWS_SECRET_KEY=XXXX
AWS_ACCESS_KEY=XXXX
S3_BUCKET=XXXX
```