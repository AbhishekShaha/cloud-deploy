FROM python:3.6.1

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["./entrypoint.sh"]