import redis
from uuid import UUID, uuid4
from redis_lab.services.logger import _LOGGER


class RedisDB:
    def __init__(self, host, port):
        self._db: redis.Redis = redis.Redis(
            host,
            port,
            decode_responses=True,
            charset='UTF-8'
        )

    # Генерация уникального ключа для нового пользователя
    def create_user(self, name) -> UUID:
        user_id = uuid4()
        self._db.set(str(user_id), name)
        _LOGGER.info(f"Создал пользователя с user_id: {user_id}")
        return user_id

    # Создание временного ключа
    def create_session(self, user_id):
        session_key = f"session:{user_id}:{session_id}"
        token = str(uuid.uuid4())
        self._db.setex(session_key, 3600, token)  # Время жизни 1 час (3600 секунд)
        return session_id, token

    # Генерация уникального ключа для нового пользователя
    def get_user(self, user_id):
        return self._db.get(user_id)
