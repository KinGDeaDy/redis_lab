import hashlib
from uuid import uuid4

import redis
from rq import Queue

from redis_lab.services.logger import _LOGGER


class RedisDB:
    def __init__(self, host, port):
        self._db: redis.Redis = redis.Redis(
            host,
            port,
            decode_responses=True,
            charset='UTF-8'
        )
        self._queue: Queue = Queue(connection=redis.Redis())

    @staticmethod
    def generate_user_id() -> str:
        """
        Функция для генерации уникального ключа
        :return:
        """
        return str(uuid4())

    def create_user_session(self, user_id: str, session_expiry: int = 3600) -> str:
        """
        Функция для создания пользовательской сессии
        :param user_id: UUID пользователя
        :param session_expiry: TTL сессии в секундах
        :return: токен сессии
        """
        session_key = f"user:{user_id}:session"
        session_token = str(uuid4())
        self._db.setex(session_key, session_expiry, session_token)
        _LOGGER.info(f"Создал пользовательскую сессию {session_token=} {session_key=}")
        return session_token

    def create_action_token(self, user_id: str) -> str:
        """
        Функция для создания уникального токена для действия пользователя
        :param user_id: UUID пользователя
        :return: токен действия
        """
        action_token = hashlib.sha256(str(uuid4()).encode()).hexdigest()
        action_key = f"user:{user_id}:actions"
        self._db.lpush(action_key, action_token)
        _LOGGER.info(f"Создал уникальный токен {action_token} для действия пользователя")
        return action_token

    def create_user_card(self, user_id: str, full_name: str) -> dict[str, str]:
        """
        Функция для создания карточки пользователя
        :param user_id: UUID пользователя
        :param full_name: ФИО пользователя
        :return: карточка пользователя
        """
        user_key = f"user:{user_id}:info"
        session_token = self.create_user_session(user_id)
        user_info = {"full_name": full_name, "session_token": session_token}
        self._db.hmset(user_key, user_info)
        _LOGGER.info(f"Создал карточку пользователя {user_info} по ключу {user_key}")
        return user_info

    def get_user_info(self, user_id: str) -> dict[str, str]:
        """
        Функция для получения информации о пользователе
        :param user_id: UUID пользователя
        :return: информация о пользователе
        """
        user_key = f"user:{user_id}:info"
        retrieved_user_info = self._db.hgetall(user_key)
        _LOGGER.info(f"Информация о пользователе: {retrieved_user_info}")
        return retrieved_user_info
