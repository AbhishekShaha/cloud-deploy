#!/bin/bash

source /home/ubuntu/CA674-Cloud-Architecture//venv/bin/activate
source /home/ubuntu/CA674-Cloud-Architecture/.env
# /home/ubuntu/CA674-Cloud-Architecture/venv/bin/python /home/ubuntu/CA674-Cloud-Architecture/manage.py runserver


/home/ubuntu/CA674-Cloud-Architecture/venv/bin/gunicorn manage:app -b localhost:5000

