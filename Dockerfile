FROM python:2.7

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000 

COPY . .

CMD ["./entrypoint.sh"]