import json

from app.core.redis import redis_client
from app.websocket.manager import manager


async def publish_group_message(
    group_id: str,
    message: dict,
):
    channel = f"group:{group_id}"

    await redis_client.publish(
        channel,
        json.dumps(message),
    )


async def subscribe_group(group_id: str):

    pubsub = redis_client.pubsub()

    channel = f"group:{group_id}"

    await pubsub.subscribe(channel)

    async for message in pubsub.listen():

        if message["type"] != "message":
            continue

        data = json.loads(message["data"])

        await manager.broadcast_to_group(
            group_id,
            data,
        )