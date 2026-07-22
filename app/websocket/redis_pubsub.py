import json
import traceback

from app.core.redis import redis_client
from app.websocket.manager import manager

CHANNEL = "chat"


async def publish(message: dict):
    print("\n" + "=" * 70)
    print("📤 PUBLISHING TO REDIS")
    print(json.dumps(message, indent=2))
    print("=" * 70 + "\n")

    await redis_client.publish(
        CHANNEL,
        json.dumps(message),
    )


async def subscribe():
    print("🚀 subscribe() called")

    pubsub = redis_client.pubsub()

    print("📡 PubSub object created")

    await pubsub.subscribe(CHANNEL)

    print("✅ Redis Subscriber Started")

    async for message in pubsub.listen():

        print("\n" + "-" * 70)
        print("📥 RAW REDIS MESSAGE")
        print(message)
        print("-" * 70)

        if message["type"] != "message":
            continue

        try:

            raw_data = message["data"]

            # Decode bytes if Redis returns bytes
            if isinstance(raw_data, bytes):
                raw_data = raw_data.decode("utf-8")

            print("\n📦 Raw Data")
            print(raw_data)

            data = json.loads(raw_data)

            print("\n✅ PARSED MESSAGE")
            print(json.dumps(data, indent=2))

            receiver_id = data.get("receiver_id")
            sender_id = data.get("sender_id")

            print(f"\n👤 Sender   : {sender_id}")
            print(f"👤 Receiver : {receiver_id}")

            print("\n🟢 Connected Users:")
            print(list(manager.active_connections.keys()))

            # Send to receiver
            if receiver_id:
                print(f"\n➡️ Sending to Receiver: {receiver_id}")

                await manager.send_to_user(
                    receiver_id,
                    data,
                )

            # Send to sender
            if sender_id:
                print(f"\n➡️ Sending to Sender: {sender_id}")

                await manager.send_to_user(
                    sender_id,
                    data,
                )

            print("\n✅ Message Processing Complete")

        except Exception:
            print("\n❌ REDIS SUBSCRIBER ERROR")
            traceback.print_exc()