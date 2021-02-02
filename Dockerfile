FROM python:3.7.9

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY run.py .

CMD [ "python", "./run.py" ]
