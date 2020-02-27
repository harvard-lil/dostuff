# dostuff

Run:

    docker-compose up -d --build
    docker-compose exec web pipenv run ./manage.py migrate
    docker-compose exec web pipenv run ./manage.py collectstatic
    docker-compose exec web pipenv run ./manage.py createsuperuser
    docker-compose exec web pipenv run ./manage.py runserver 0.0.0.0:5000
    
Log in as the new superuser at [localhost:5000/admin](http://localhost:5000/admin). Identify or create a token, then go to [localhost:5000/rooms/test](http://localhost:5000/rooms/test) and run, e.g.

    curl -H "Content-Type: application/json" -X POST http://localhost:5000/new_event -H 'Authorization: Token <token>' -d '{"message": "hello world!", "room_name":"test"}'
    curl -H "Content-Type: application/json" -X POST http://localhost:5000/new_event -H 'Authorization: Token <token>' -d '{"color": "blue", "room_name":"test"}'
    
Hit `Ctrl-C` to stop the server, then stop the container by running

    docker-compose down
