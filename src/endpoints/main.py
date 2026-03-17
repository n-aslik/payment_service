from fastapi import Depends,APIRouter, Response
from ..models import models
from typing import Any
from src.modules import auth_module
import lib.acl as ACL



router=APIRouter(prefix="/v1")

# region ADMINISTRATION

@router.post('/create-admin', tags=["ADMINISTRATION"])
async def create_admin(data: models.User, payload:dict = Depends(ACL.access_token) ):
    return await auth_module.create_admin(data)

@router.put("/update-admin", tags=["ADMINISTRATION"])
async def update_admin(user_id: str, data: models.User, payload:dict = Depends(ACL.access_token)):
    return  await auth_module.update_admin(user_id,data)

@router.delete('/delete-admin', tags=["ADMINISTRATION"] )
async def delete_admin(user_id: str, payload: dict = Depends(ACL.access_token)):
    return await auth_module.delete_admin(user_id)

@router.get('/get-admins', tags=["ADMINISTRATION"] )
async def get_admin(payload: dict = Depends(ACL.access_token)):
    return await auth_module.get_admin()

@router.get('/get-admin', tags=["ADMINISTRATION"] )
async def get_admin_by_id(user_id: str, payload: dict = Depends(ACL.access_token)):
    return await auth_module.get_admin_by_id(user_id)

# endregion

# region AUTHORIZATON

@router.post("/login", tags=["AUTHORIZATON"])
async def login(data: models.Login = Depends()):
    return await auth_module.login(data)

@router.post('/refresh/token', tags=["AUTHORIZATON"])
async def refresh_token(response: Response, payload: dict = Depends(ACL.refresh_token)):
    return await auth_module.refresh_token(payload)

@router.delete('/logout', tags=["AUTHORIZATON"])
async def logout(payload: dict = Depends(ACL.access_token)):
    return await auth_module.logout(payload['user_id'])

# endregion
