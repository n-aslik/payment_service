from fastapi import FastAPI, BackgroundTasks, APIRouter,Header, HTTPException
from src.modules import payment
from lib.config import send_to_retry_queue, RetryService
from src.models import models
import uuid
from decimal import Decimal
from typing import Optional
import random

router = APIRouter()
retry_service = RetryService()

@router.post("/create-user")
async def create_users(data: models.User):
    return await payment.create_users(data)

@router.delete("/delete-user")
async def delete_users(user_id: str):
    return await payment.delete_users(user_id)

@router.get("/get-users")
async def get_all_users():
    return await payment.get_users()

@router.get("/get-metrics")
async def get_all_metrics():
    return await payment.get_metricks()

@router.post("/create_payment")
async def create_payment(
    user_id: str, 
    amount: float,
    background_tasks: BackgroundTasks,
    x_idempotency_key: str = Header(random.choice([str(uuid.uuid4())]))
):
    existing_tx = await payment.get_idempotency_key_from_tx(x_idempotency_key)
    
    if existing_tx:
        return {
            "transaction_id": existing_tx[0], 
            "status": existing_tx[1], 
            "message": "Returned existing transaction"
        }
    
    if amount <= 0:
        current_status = 'Rejected'
    elif amount > 50000:
        current_status = 'Awaiting_Manual_Approval'
    else:
        current_status = "Pending"

    new_id = str(uuid.uuid4())
    data = models.Transactions(
        id=new_id,
        user_id=user_id,
        amount=amount,
        commission=amount * 0.02,
        status=current_status,
        idempotency_key=x_idempotency_key 
    )
    try:
        await payment.create_transactions(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB Error")

    if current_status == "Pending":
        await send_to_retry_queue(data.id)
        background_tasks.add_task(retry_service.process, new_id)
        return {"transaction_id": new_id, "status": "Processing"}
    
    return {"transaction_id": new_id, "status": current_status}

@router.get("/history")
async def get_payment_history():
    return await payment.get_payment_history()

@router.get("/balance")
async def get_balance(user_id: str):
    return await payment.get_user_balance(user_id)

@router.post("/pay")
async def mock_payment_gateway(
    amount: str, 
    x_idempotency_key: str = Header(None) 
):
    if not x_idempotency_key:
        raise HTTPException(status_code=400, detail="X-Idempotency-Key header is missing")

    existing_tx = await payment.get_idempotency_key_from_tx(x_idempotency_key)

    if existing_tx:
        status_tx, old_amount = existing_tx
        return {
            "status": "success", 
            "message": "Already processed (idempotent)",
            "original_status": status_tx,
            "amount": str(old_amount)
        }

    try:
        money = Decimal(amount)
        if money <= 0: raise ValueError()
    except:
        raise HTTPException(status_code=400, detail="Invalid amount format")
    
    print(f"Впервые обрабатываю платеж: {money} с ключом {x_idempotency_key}")
    
    return {
        "status": "success", 
        "amount": str(money),
        "idempotency_key": x_idempotency_key
            }