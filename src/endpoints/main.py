from fastapi import Depends,APIRouter, Response
from ..models import models
from typing import Any
from payment_service.src.modules import payment



router=APIRouter(prefix="/v1")

# region ADMINISTRATION

@router.post('/create-admin', tags=["ADMINISTRATION"])
async def create_admin(data: models.User):
    return await payment.create_admin(data)

@router.put("/update-admin", tags=["ADMINISTRATION"])
async def update_admin(user_id: str, data: models.User):
    return  await payment.update_admin(user_id,data)

@router.delete('/delete-admin', tags=["ADMINISTRATION"] )
async def delete_admin(user_id: str):
    return await payment.delete_admin(user_id)

@router.get('/get-admins', tags=["ADMINISTRATION"] )
async def get_admin():
    return await payment.get_admin()

@router.get('/get-admin', tags=["ADMINISTRATION"] )
async def get_admin_by_id():
    return await payment.get_admin_by_id()

# endregion

# region AUTHORIZATON

@router.post("/login", tags=["AUTHORIZATON"])
async def login(data: models.Login = Depends()):
    return await payment.login(data)

@router.post('/refresh/token', tags=["AUTHORIZATON"])
async def refresh_token(response: Response):
    return await payment.refresh_token()

@router.delete('/logout', tags=["AUTHORIZATON"])
async def logout():
    return await payment.logout()

# endregion
