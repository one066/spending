import redis

from extension.project_config import get_config

redis_host = get_config().REDIS_HOST
redis_password = get_config().REDIS_PASSWORD
redis_client = redis.Redis(host=redis_host, port=6379, db=0, password=redis_password,)
