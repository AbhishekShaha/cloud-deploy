FROM python:3.6.1

## this line not needed, 
## WORKDIR will create dir if it's not there
#RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

## no need to keep using full path when you've set workdir
## also, always use COPY unless you know *why* you need ADD
COPY ./requirements.txt .
RUN pip install -r requirements.txt

## no need for full path again, also changing ADD to COPY
COPY . .

## this line is redundant, it was already copied in last line
#COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

## this is oddly named. Entrypoints should use ENTRYPOINT not CMD
## recommend renaming this to make it clear what it's used for
## If it's a long running service, it shouldn't use a shell script
CMD ["./entrypoint.sh"]