#web: gunicorn dostuff.wsgi
web: daphne dostuff.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2 --threads ${WORKER_THREADS:=4}
release: python manage.py migrate --noinput