from os import environ

from split_settings.tools import include
from split_settings.tools import optional


ENV = environ.get("DJANGO_ENV", "dev")

base_settings = [
    "env.py",
    "base.py",
    "database.py",
    "drf.py",
    f"environments/{ENV}.py",
]

include(*base_settings)
