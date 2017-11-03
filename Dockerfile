FROM python:3.6.1

# create working directory
RUN mkdir -p /usr/src/app

# set working work directory
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
ADD . /usr/src/app

# add entrypoint.sh
ADD ./entrypoint.sh /usr/src/app/entrypoint.sh

# run server
CMD ["sh entrypoint.sh"]