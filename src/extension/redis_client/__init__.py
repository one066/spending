import redis

# 获取redis数据库连接
redis_client = redis.Redis(host="redis", port=6379, db=0)
