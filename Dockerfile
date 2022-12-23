FROM python:3.10.6
WORKDIR /price_checker
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./* .
CMD ["python","app/."]