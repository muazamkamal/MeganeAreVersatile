FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./run.sh

ENTRYPOINT ["./run.sh"]