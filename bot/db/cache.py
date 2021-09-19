from redis.client import StrictRedis

import json


class CacheRedis():
    _cache = StrictRedis("localhost", 6379)

    def __init__(self):
        print("[*] Create cache object.")

    def create_dict(self, key: str, data):
        self._cache.set(key, json.dumps(data))

    def get_dict(self, key):
        self._cache.get(key)
