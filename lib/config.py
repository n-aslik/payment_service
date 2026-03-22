import time
import httpx
from src.modules import payment
import aio_pika
import os
import json
import logging
from fastapi import HTTPException, status
import asyncio

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
    async def process(self, tx_id: str):
        
        result = await payment.get_transactions_by_id(tx_id)
        if not result:
            logger.error(f"Транзакция {tx_id} не найдена")
            return 
        amount, user_id, commission, idempotency_key = result
        


        PAYMENT_URL = "http://web:8000/pay" 

        async with httpx.AsyncClient() as client:
            for i in range(3): 
                try:
                
                    headers = {
                        "X-Idempotency-Key": str(idempotency_key),
                        "Content-Type": "application/json"
                    }
                    

                    res = await client.post(
                        PAYMENT_URL, 
                        content=str(amount),
                        headers=headers,
                        timeout=10.0
                    )

                    if res.status_code == 200:
                        logger.info(f"Платеж {tx_id} успешно обработан")
                        await self._success_logic(tx_id, user_id, amount, commission)
                        return
                    else:
                        logger.warning(f"Попытка {i+1}: Сервис вернул {res.status_code}")

                except Exception as e:
                    logger.error(f"Попытка {i+1}: Ошибка связи: {e}")

                
                await asyncio.sleep(i + 1)

        await self._update_status(tx_id, "Failed")

    async def _success_logic(self, tx_id, user_id, amount, commission):
        total = (amount + commission)
    
        await payment.edit_balance(total, user_id)

        await payment.edit_success_status(tx_id)

        logger.info(f"Баланс пользователя {user_id} обновлен, статус TX {tx_id} -> Success")

    async def _update_status(self, tx_id, status):
        await payment.edit_status(status, tx_id)