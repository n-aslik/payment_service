from fastapi import HTTPException,status
from connections.dbconn import connection
from connections.DML import (create_transaction, 
                            update_success_status, 
                            update_status, 
                            update_balance, 
                            get_transaction_by_id, 
                            get_idempotency_key, 
                            create_user,
                            get_metrics,
                            delete_user,
                            select_user,
                            get_balance,
                            get_history)
import  lib.config as ACL
from ..models import models
import uuid
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

async def create_users(data: models.User):

    with connection() as cur:
        result = None
        cur.execute(create_user,(data.balance,))
        result = cur.fetchone()
        if not result:
            logger.error(f"Пользователь {result[0]} не найден для выполнения платежа")
            raise HTTPException(status_code=404, detail="Transaction not found")
        return {'id':result[0], "balance": result[1]}
    
async def delete_users(user_id: str):

    with connection() as cur:
        result = None
        cur.execute(delete_user,(user_id,))
        result = cur.fetchone()
        if not result:
            logger.error(f"Пользователь {user_id} не найден для выполнения платежа")
            raise HTTPException(status_code=404, detail="Transaction not found")
        return result
    

async def get_users():

    with connection() as cur:
        result = None
        cur.execute(select_user)
        result = cur.fetchall()
        if not result:
            logger.error(f"Пользователь {result[0]} не найден для выполнения платежа")
            raise HTTPException(status_code=404, detail="Transaction not found")
        return [{
            "id": r[0], 
            "balance": r[1]
        }for r in result
        ]

async def create_transactions(data: models.Transactions):

    with connection() as cur:
        result = None
        cur.execute(create_transaction,(data.id, data.user_id, data.amount, data.commission , data.status, data.idempotency_key))
        result = cur.fetchone()
        if not result:
            logger.error(f"Пользователь {data.user_id} не найден для выполнения платежа")
            raise HTTPException(status_code=404, detail="Transaction not found")
        return result
        

async def edit_balance(balance_value: float, user_id: str):
    """
    Обновляет баланс пользователя. 
    balance_value: положительное число для начисления, отрицательное для списания.
    """
    try:
        with connection() as cur:
            cur.execute(update_balance, (balance_value, user_id))
            
            result = cur.fetchone()
            # Фиксируем изменения в БД
            
            if not result:
                logger.error(f"Пользователь {user_id} не найден для обновления баланса")
                raise HTTPException(status_code=404, detail="User not found")
            
            return result
    except Exception as e:
        logger.error(f"Ошибка БД в edit_balance: {e}")
        raise HTTPException(status_code=500, detail="Database update balance error")

async def edit_status(tx_status: str, transaction_id: str):
    """Обновляет статус транзакции на произвольный"""
    try:
        with connection() as cur:
            # SQL: "UPDATE transactions SET status = %s WHERE id = %s RETURNING id, status"
            cur.execute(update_status, (tx_status, transaction_id))
            
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Transaction not found")
            
            return result
    except Exception as e:
        logger.error(f"Ошибка БД в edit_status: {e}")
        raise HTTPException(status_code=500, detail="Database update status error")

async def edit_success_status(transaction_id: str):
    """Специализированная функция для перевода в Success"""
    try:
        with connection() as cur:
            # SQL: "UPDATE transactions SET status = 'Success' WHERE id = %s RETURNING id, status"
            cur.execute(update_success_status, (transaction_id,))
            
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Transaction not found")
                
            return result
    except Exception as e:
        logger.error(f"Ошибка БД в edit_success_status: {e}")
        raise HTTPException(status_code=500, detail="Database update success status error")
    
async def get_transactions_by_id(transaction_id: str):
    result = None
    with connection() as cur:
        cur.execute(get_transaction_by_id, (transaction_id,))
        result = cur.fetchone()
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{result}")

async def get_payment_history():
    with connection() as cur:
        cur.execute(get_history)
        result = cur.fetchall()
        
        return [
            {
                "id": r[0], 
                "user_id": r[1], 
                "amount": round(float(r[2]),2), 
                "commission": float(r[3])
            } for r in result
        ]


async def get_idempotency_key_from_tx(key: str):
    result = None
    with connection() as cur:
        cur.execute(get_idempotency_key, (key,))
        result = cur.fetchone()
        print(result)
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{result}")

async def get_user_balance(user_id: str):
    result = None
    with connection() as cur:
        cur.execute(get_balance, (user_id,))
        result = cur.fetchone()
        return {"balance":result[0]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{result}")

async def get_metricks():
    result = None
    with connection() as cur:
        cur.execute(get_metrics)
        result = cur.fetchall()
        return [
            {
                "success_count": r[0], 
                "failed_count": r[1], 
            } for r in result
        ]

    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"{result}")




    
