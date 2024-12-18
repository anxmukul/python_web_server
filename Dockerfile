FROM python:3.12-slim
LABEL authors="mukul"

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# install dependencies
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]
