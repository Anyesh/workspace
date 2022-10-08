import os
import random
import re
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
        f.write(f"{key}={value.strip('%')}\n")


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


def common_choice_helper(original_list: list, most_common: list) -> list:
    seen = set()
    valid_most_common = [x for x in most_common if x in original_list]
    seq = [*valid_most_common, *original_list]
    return [x for x in seq if x not in seen and not seen.add(x)]  # type: ignore


def validate_ticket_id(_, ticket_id: str) -> bool:
    return re.match(r"^[A-Za-z]+-\d+$", ticket_id) is not None
