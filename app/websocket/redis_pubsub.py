import json
import traceback

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

            raw_data = message["data"]

            # Decode bytes if Redis returns bytes
            if isinstance(raw_data, bytes):
                raw_data = raw_data.decode("utf-8")

            data = json.loads(raw_data)

            receiver_id = data.get("receiver_id")
            sender_id = data.get("sender_id")


            # Send to receiver
            if receiver_id:
                await manager.send_to_user(
                    receiver_id,
                    data,
                )

            # Send to sender
            if sender_id:

                await manager.send_to_user(
                    sender_id,
                    data,
                )


        except Exception:
            print("\n❌ REDIS SUBSCRIBER ERROR")
            traceback.print_exc()