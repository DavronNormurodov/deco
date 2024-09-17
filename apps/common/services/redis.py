from typing import Union

import redis
from core.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_CONNECTION_TIMEOUT

redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0,
                             socket_timeout=REDIS_CONNECTION_TIMEOUT,
                             socket_connect_timeout=REDIS_CONNECTION_TIMEOUT)


def write_to_redis(key: Union[str, int], value: Union[str, int], exp: int) -> None:
    redis_db.set(name=str(key), value=str(value), ex=exp)


def get_from_redis_by_key(key: str, contains: bool = False) -> str:
    return redis_db.keys(key) if not contains else redis_db.keys(f'*{key}*')


def get_value_from_redis(key: str) -> str:
    try:
        if data := redis_db.get(str(key)):
            return data.decode('utf-8')
        else:
            return None
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
        return None


def set_key_string_refresh(*args) -> str:
    return ":".join(args)
