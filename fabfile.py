import random
import os
from functools import wraps

import sys
from fabric.decorators import task
from django.utils.crypto import get_random_string

sys.path.append(os.path.dirname(__file__))

### helpers ###
_django_setup_run = False
def django_setup(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global _django_setup_run
        if not _django_setup_run:
            _django_setup_run = True

            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dostuff.settings')
            django.setup()

        return f(*args, **kwargs)
    return wrapper


### tasks ###

@task
@django_setup
def create_users(count=1):
    from django.contrib.auth.models import User

    adjectives = "adaptable	adventurous	affectionate	ambitious	amiable	compassionate	considerate	courageous courteous	diligent	empathetic	exuberant	frank	generous	gregarious	impartial	intuitive	inventive passionate	persistent	philosophical	practical	rational	reliable	resourceful	sensible	sincere sympathetic	unassuming	witty".split()
    animals = "Dog Cat Horse Chicken Fish Bear Bird Shark Snake Pig Lion Turkey Wolf Spider Duck Deer Cow  Monkey Lobster Ape Pony Eagle Dolphin Bison".split()

    for i in range(int(count)):
        username = ("%s %s" % (random.choice(adjectives), random.choice(animals))).title()
        user = User.objects.create_user(username=username, password=get_random_string(20))
        print(user.auth_token.key)
