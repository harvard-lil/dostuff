# dostuff

This is an interactive API for educational demonstrations, using [Django Channels](https://channels.readthedocs.io/en/stable/) and [Django REST framework](https://www.django-rest-framework.org/).

Run:

    docker compose up -d --build
    docker compose exec web poetry run ./manage.py migrate
    docker compose exec web poetry run ./manage.py collectstatic
    docker compose exec web poetry run ./manage.py createsuperuser
    docker compose exec web poetry run ./manage.py runserver 0.0.0.0:8000
    
Log in as the new superuser at [localhost:5000/admin](http://localhost:5000/admin). Identify or create a token, then go to [localhost:5000/rooms/test](http://localhost:5000/rooms/test) and run, e.g.

    curl -H "Content-Type: application/json" -X POST http://localhost:5000/new_event -H 'Authorization: Token <token>' -d '{"message": "hello world!", "room_name":"test"}'
    curl -H "Content-Type: application/json" -X POST http://localhost:5000/new_event -H 'Authorization: Token <token>' -d '{"color": "blue", "room_name":"test"}'
    
Hit `Ctrl-C` to stop the server, then stop the containers by running

    docker compose down

You can also run the service with daphne directly, as in the `Procfile`:

```
docker compose exec web poetry run daphne -p 5000 dostuff.asgi:application --bind 0.0.0.0 -v2
```

When managing dependencies with Poetry, keep `requirements.txt` up to date by running `docker compose exec web poetry export -o requirements.txt`.
