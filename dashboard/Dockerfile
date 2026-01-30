FROM python:latest

RUN apt-get update && apt-get install -y curl unixodbc odbcinst
RUN curl -sSL -O https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb
RUN dpkg -i packages-microsoft-prod.deb
RUN rm packages-microsoft-prod.deb

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY load_data.py .

COPY load_s3_data.py .

COPY charts.py .

COPY classes.py .

COPY dashboard.py .

COPY pages/ pages/

CMD ["streamlit", "run", "dashboard.py"]