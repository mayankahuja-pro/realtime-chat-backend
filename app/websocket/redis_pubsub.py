import json

from app.core.redis import redis_client
from app.websocket.manager import manager

CHANNEL = "chat"


async def publish(message: dict):
    await redis_client.publish(
        CHANNEL,
        json.dumps(message),
    )


async def subscribe():

    pubsub = redis_client.pubsub()

    await pubsub.subscribe(CHANNEL)

    async for message in pubsub.listen():

        if message["type"] != "message":
            continue

        try:

            data = json.loads(message["data"])

            receiver_id = data.get("receiver_id")

            if receiver_id:
                await manager.send_to_user(
                    receiver_id,
                    data,
                )

            sender_id = data.get("sender_id")

            if sender_id:
                await manager.send_to_user(
                    sender_id,
                    data,
                )

        except Exception as e:
            print(e)