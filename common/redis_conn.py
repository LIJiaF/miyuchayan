from redis import StrictRedis

from config import redisConfig

redis = StrictRedis(**redisConfig)
