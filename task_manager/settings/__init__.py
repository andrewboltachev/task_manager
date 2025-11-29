from os import environ

from split_settings.tools import include

ENV = environ.get("DJANGO_ENV", "dev")

base_settings = [
    "env.py",
    "base.py",
    "database.py",
    "drf.py",
    f"environments/{ENV}.py",
]

include(*base_settings)
