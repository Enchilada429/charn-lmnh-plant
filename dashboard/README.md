# 🌱 LMNH Plant Monitoring Dashboard

## Environment Variables

There must be a `.env` file in the `dashboard` directory with the following contents:

```
DB_HOST=XXXX
DB_PORT=1433
DB_USER=XXXX
DB_PASSWORD=XXXX
DB_NAME=XXXX
DB_SCHEMA=XXXX
```

## Files
- `load_data.py`: Loads the relevant data from the database.
- `charts.py`: Creates plots to be displayed on dashboard.
- `dashboard.py`: Main dashboard configuration.

## Quick Start

To run the dashboard, run the following command:

```
streamlit run dashboard.py
```


## Docker & Uploading Image to AWS ECR

If you want to upload a Docker image of this dashboard to your AWS ECR, run the following:

```
sh dockerise.sh
```

You will be given prompts to enter your `AWS_ACCOUNT_ID`, `AWS_REGION`, and `AWS_ECR_REPO` name. These can all be found on AWS.