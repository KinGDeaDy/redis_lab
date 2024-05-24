from typing import Final, TypedDict


class RedisCredentials(TypedDict):
    host: str
    port: int


REDIS_HOST: Final[str] = "localhost"
REDIS_PORT: Final[int] = 6379

redis_credentials = {
    "host": REDIS_HOST,
    "port": REDIS_PORT
}
