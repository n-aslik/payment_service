import asyncio
import aio_pika
import os
import logging
import json
from lib.config import RetryService

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_message(message: aio_pika.IncomingMessage):
    """
    Функция-обработчик входящего сообщения
    """
    async with message.process(): 
        try:
            
            body = message.body.decode()
            data = json.loads(body)
            tx_id = data.get("transaction_id")
            
            logger.info(f" [x] Получена задача на оплату TX: {tx_id}")

        
            service = RetryService()
        
            await service.process(tx_id)
            
            logger.info(f" [v] Обработка TX {tx_id} завершена успешно")
            
        except Exception as e:
            logger.error(f" [!] Ошибка при обработке сообщения: {e}")
        

async def main():

    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    
    connection = await aio_pika.connect_robust(rabbitmq_url)
    
    async with connection:

        channel = await connection.channel()
        
        
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue('retry_queue', durable=True)

        logger.info(' [*] Ожидание сообщений. Нажми CTRL+C для выхода')

    
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await process_message(message)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Воркер остановлен пользователем")