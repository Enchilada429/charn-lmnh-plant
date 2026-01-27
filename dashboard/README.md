# 🌱 LMNH Plant Monitoring Dashboard

## Files
- `load_data.py`: Loads the relevant data from the database.
- `charts.py`: Creates plots to be displayed on dashboard.
- `dashboard.py`: Main dashboard configuration.

## Quick Start

To run the dashboard, run the following command:

```
streamlit run dashboard.py
```

This will extract data from the plant API, clean the data, and upload the data to the RDS.


## Docker & Uploading Image to AWS ECR

If you want to upload a Docker image of this dashboard to your AWS ECR, run the following:

```
sh dockerise.sh
```

You will be given prompts to enter your `AWS_ACCOUNT_ID`, `AWS_REGION`, and `AWS_ECR_REPO` name. These can all be found on AWS.