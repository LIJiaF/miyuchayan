from redis import StrictRedis

redisConfig = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': ''
}

redis = StrictRedis(**redisConfig)
