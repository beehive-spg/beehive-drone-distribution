import asyncio
import aio_pika
import os, sys
import json
import time
from distribution.foundation.logger import Logger

logger = Logger(__name__)

def start_settings_queue(distribution_status, sending_connection):
    logger.info("started settings consumer")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(settings_queue(distribution_status, sending_connection, loop))
    loop.close()

async def settings_queue(distribution_status, sending_connection, loop):
    try:
        connection = await aio_pika.connect_robust(os.getenv('RABBITMQ_URL'), loop=loop)
        logger.info("01 - {}".format(connection))
        queue_name = os.getenv('SETTINGS_QUEUE')
        logger.info("02 - {}".format(queue_name))
        channel = await connection.channel()
        logger.info("03 - {}".format(channel))
        queue = await channel.declare_queue(queue_name, durable=True)
        logger.info("helloooooooooooooooooooo")

        async for message in queue:
            logger.info("step 01")
            with message.process():
                logger.info("step 02")
                try:
                    logger.info("step 03")
                    decoded_message = message.body.decode("utf-8")
                    loaded_message = json.loads(decoded_message)
                    logger.info("Received message: " + str(loaded_message))
                    distribution_status = int(loaded_message['value'])
                    logger.info(distribution_status)
                    sending_connection.send(distribution_status)
                except Exception as e:
                    logger.info(e)

                if queue.name in message.body.decode():
                    break
    except RuntimeError:
            logger.info("RabbitMQ - waiting for connection...")
            await asyncio.sleep(1)