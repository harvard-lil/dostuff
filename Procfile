web: daphne -p $PORT dostuff.asgi:application --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2 --threads ${WORKER_THREADS:=4}
release: python manage.py migrate --noinput