# 🌱 Liverpool Museum of Natural History Plant Monitoring 
A fully-functioning, end-to-end ETL pipeline and dashboard which cleans, transforms, and analyses real-time recordings of the moisture and temperature levels of the plants in the Liverpool Museum of Natural History (LMNH).

## Introduction 🌷
The gardeners at the LMNH want to be able to monitor the health of their plants over time. This project provides a solution to this by building an ETL pipeline that takes in the readings from the temperature and moisture sensors within the garden and analyses these recordings for all the plants. 

## Project Structure 📂🪷

```text
├── pipeline/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
└── dashboard/
    ├── load_data.py
    ├── charts.py
    ├── dashboard.py
    └── pages/
        └── archive_page.py
├── archive/
│   ├── 
```

## Architecture Diagram & ERD 🧩🪷

![Architecture Diagram](Charn_LMNH_Plant_Architecture_Diagram.png)

![ERD Diagram](erd_ver6.png)


## Data Source 📊🌱
The data source from which this pipeline extracts recordings is this [API](https://tools.sigmalabs.co.uk/api/plants/8)

Ⓒ Charn Group (Basil, Fariha, Omar Y, Sam)