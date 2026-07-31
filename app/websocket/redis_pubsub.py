import asyncio
import json

from app.core.redis import redis_client
from app.websocket.manager import manager

CHANNEL = "chat"


async def publish(message: dict, exclude_user_id: str = None):
    """Publish a message to the Redis pub/sub channel."""
    payload = json.dumps({
        "message": message,
        "exclude_user_id": exclude_user_id,
    })
    await redis_client.publish(
        CHANNEL,
        payload,
    )


async def subscribe():

    pubsub = redis_client.pubsub()

    await pubsub.subscribe(CHANNEL)

    async for message in pubsub.listen():

        if message["type"] != "message":
            continue

        data = json.loads(message["data"])
        await manager.broadcast(
            data["message"],
            exclude_user_id=data.get("exclude_user_id"),
        )