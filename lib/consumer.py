import pika
import asyncio
from lib.config import RetryService # Импортируй свой класс
import os

service = RetryService()
rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
params = pika.URLParameters(rabbitmq_url)
def callback(ch, method, properties, body):
    tx_id = body.decode()
    print(f" [x] Получена задача на оплату: {tx_id}")
    
    # Запускаем асинхронный процесс в синхронном воркере
    asyncio.run(service.process(tx_id))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(params))
channel = connection.channel()
channel.queue_declare(queue='payment_queue')
channel.basic_consume(queue='payment_queue', on_message_callback=callback)

print(' [*] Ожидание сообщений. Нажми CTRL+C для выхода')
channel.start_consuming()