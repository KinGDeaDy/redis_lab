from redis_lab.services.database import RedisDB
from redis_lab.settings import redis_credentials

if __name__ == '__main__':
    redis_client: RedisDB = RedisDB(**redis_credentials)
    user_id = redis_client.generate_user_id()
    full_name = "Иван Иванов"

    # Создаем карточку пользователя
    user_info = redis_client.create_user_card(user_id, full_name)

    # Создаем токен для действия пользователя
    action_token = redis_client.create_action_token(user_id)

    # Получаем информацию о пользователе
    retrieved_user_info = redis_client.get_user_info(user_id)
