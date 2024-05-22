from redis_lab.settings import redis_credentials
from redis_lab.services.database import RedisDB


redis_client: RedisDB = RedisDB(**redis_credentials)


# redis_client.create_user("Артём")

print(redis_client.get_user(user_id="user:cf1294ba-3b93-413d-94c5-fe9bda9819fe"))