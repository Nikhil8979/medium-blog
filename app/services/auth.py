from fastapi import  HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginRequest,RegisterRequest
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password,verify_password,create_access_token
class AuthService:
    def __init__(self,db:AsyncSession):
        self.db = db
    
    async def login(self,data:LoginRequest):
        stmt = select(User).where(User.email == data.email);
        user = await self.db.scalar(stmt)
        if not user:
            raise HTTPException(status_code=404,detail="Email or password is incorrect")
         
         
        if not verify_password(data.password,user.password):
            raise HTTPException(status_code=404,detail="Email or password is incorrect")
        
        payload = {
            "id":user.id,
            "name":user.name,
            "email":user.email
        }
        
        token = create_access_token(payload)
        payload["token"] = token
        return payload

    async def register(self,data:RegisterRequest):
        stmt = select(User).where(User.email == data.email)
        existing = await self.db.scalar(stmt)
        if existing:
            raise HTTPException(status_code=409,detail="Email already exists")
        user= User(
            name=data.full_name.strip(),
            email=data.email.lower(),
            password = hash_password(data.password)
            )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user