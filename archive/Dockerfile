# dockerfile to create the archive image
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip3 install -r requirements.txt

COPY archive.py . ${LAMBDA_TASK_ROOT}

CMD ["archive.handler"]

