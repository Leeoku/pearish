FROM python:3.8.3-buster

WORKDIR /pearish

COPY requirements.txt ./

RUN pip install -r requirements.txt