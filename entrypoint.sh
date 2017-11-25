#!/bin/sh

# echo "Waiting for postgres..."

# while ! nc -z users-db 5432; do
#   sleep 0.1
# done

# echo "PostgreSQL started"

python manage.py recreate_db
python manage.py seed_db

mkdir -p /code/logs
touch /code/logs/gunicorn.log
touch /code/logs/gunicorn-access.log
tail -n 0 -f /code/logs/gunicorn*.log &

gunicorn -b 0.0.0.0:5000 manage:app --log-level=info \
                                    --log-file=/code/logs/gunicorn.log \
                                    --access-logfile=/code/logs/gunicorn-access.log \
                                    --graceful-timeout 75 \
                                    --timeout 75