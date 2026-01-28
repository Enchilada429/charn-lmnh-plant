# dockerfile to create the archive image
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY archive.py .

CMD ["archive.handler"]

