import asyncio
import aio_pika
import os

async def distribution_queue(loop):
    connection = await aio_pika.connect_robust(os.getenv('RABBITMQ_URL'), loop=loop)

    queue_name = os.getenv('DISTRIBUTIONQ')

    channel = await connection.channel()    # type: aio_pika.Channel

    queue = await channel.declare_queue(queue_name, durable=True)   # type: aio_pika.Queue

    async for message in queue:
        with message.process():
            try:
                print(message.body)
            except Exception as e:
                raise

            if queue.name in message.body.decode():
                break

async def settings_queue(loop):
    connection = await aio_pika.connect_robust(os.getenv('RABBITMQ_URL'), loop=loop)

    queue_name = os.getenv('SETTINGSQ')

    channel = await connection.channel()

    queue = await channel.declare_queue(queue_name, durable=True)

    async for message in queue:
        with message.process():
            print(message.body)

            if queue.name in message.body.decode():
                break

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(distribution_queue(loop), settings_queue(loop)))
    loop.close()