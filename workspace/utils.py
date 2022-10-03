import os
import random
import string

from .settings import ENVDIR


def id_generator(size=6, chars=string.ascii_lowercase + string.digits) -> str:
    return "".join(random.choice(chars) for _ in range(size))


def parse_env() -> dict:
    envs = {}
    with open(ENVDIR, "r") as f:
        for line in f:
            key, value = line.split("=")
            envs[key] = value
    return envs


def write_env(key: str, value: str):
    with open(ENVDIR, "a+") as f:
        f.write(f"{key}={value}")


def get_or_create_env(key: str, value: str):
    if not os.path.exists(ENVDIR):
        write_env(key, value)
    envs = parse_env()
    if key not in envs:
        write_env(key, value)


def is_first_time_user():
    return not os.path.exists(ENVDIR)


def get_loggedin_user():
    try:
        return os.getlogin()
    except OSError:
        return "friend"
