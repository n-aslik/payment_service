import time
import httpx
from src.modules import payment
import aio_pika
import os
import json
import logging
from decimal import Decimal
from fastapi import HTTPException, status
import asyncio
from configparser import ConfigParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_rabbitmq_connection():
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    
    try:

        return await aio_pika.connect_robust(rabbitmq_url)
    except Exception as e:
        logger.error(f"Не удалось подключиться к RabbitMQ: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f"RabbitMQ error: {str(e)}"
        )

async def send_to_retry_queue(transaction_data: dict):
    try:
    
        connection = await get_rabbitmq_connection()
        
    
        async with connection:
    
            channel = await connection.channel()

    
            queue = await channel.declare_queue('retry_queue', durable=True)

            message_body = json.dumps(transaction_data).encode()
            
            message = aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT, # Это аналог delivery_mode=2
                content_type='application/json'
            )

            # 6. Публикуем через default_exchange (аналог exchange='')
            await channel.default_exchange.publish(
                message,
                routing_key='retry_queue'
            )
            
            logger.info(f" [x] Отправлено в очередь: {transaction_data}")
        
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения в очередь: {e}")
logger = logging.getLogger(__name__)
class RetryService:
    def __init__(self):
    
        self.PAYMENT_URL = os.getenv("PAYMENT_URL", "http://web:8000/pay")

    async def process(self, tx_id: str):
        
        result = await payment.get_transactions_by_id(tx_id)
        
        if not result:
            logger.error(f" [!] Транзакция {tx_id} не найдена в базе")
            return 
        

        amount, user_id, commission, idempotency_key = result

        async with httpx.AsyncClient() as client:
            for i in range(3): 
                try:
                    
                    headers = {
                        "X-Idempotency-Key": str(idempotency_key),
                    }
                    
                    
                    params = {
                        "amount": str(amount) 
                    }
                    
                    res = await client.post(
                        self.PAYMENT_URL, 
                        params=params, 
                        headers=headers,
                        timeout=10.0
                    )

                    if res.status_code == 200:
                        logger.info(f" [v] Платеж {tx_id} подтвержден (Attempt {i+1})")
                        
                        await self._success_logic(tx_id, user_id, amount, commission)
                        return
                    
                    elif res.status_code == 422:
                        logger.error(f" [!] Ошибка валидации (422). Ответ сервера: {res.json()}")
                        break 

                    else:
                        logger.warning(f" [!] Попытка {i+1}: Сервис вернул {res.status_code}: {res.text}")

                except Exception as e:
                    logger.error(f" [!] Попытка {i+1}: Ошибка связи: {e}")

            
                await asyncio.sleep(i + 1)

        
        logger.error(f" [X] Все попытки для TX {tx_id} исчерпаны. Статус -> Failed")
        await self._update_status(tx_id, "Failed")

    async def _success_logic(self, tx_id, user_id, amount, commission):
        
        total = amount + commission
        
        await payment.edit_balance(total, user_id)
        await payment.edit_success_status(tx_id)
        logger.info(f" [Success] Баланс пользователя {user_id} обновлен, статус TX {tx_id} -> Success")

    async def _update_status(self, tx_id, status):
        await payment.edit_status(status, tx_id)

def configdb(filename='lib/configs.env', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename, encoding='UTF-8')
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

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

