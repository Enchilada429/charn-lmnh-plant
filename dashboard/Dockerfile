FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY load_data.py .

COPY charts.py .

COPY pages/archive_page.py .

COPY dashboard.py .

CMD ["python", "dashboard.py"]