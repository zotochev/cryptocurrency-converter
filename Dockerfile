FROM python:3.10

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY app/. /tmp/app
CMD ["python", "/tmp/app/main.py"]

