import redis
from backend.core.config import settings
import json

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_redis():
    return redis_client

class RedisBus:
    def __init__(self, client):
        self.client = client
        
    def publish(self, channel: str, message: dict):
        self.client.publish(channel, json.dumps(message))
        
    def subscribe(self, channel: str):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        return pubsub

redis_bus = RedisBus(redis_client)
