from fastapi import APIRouter,Depends,status
from app.schemas.auth import LoginRequest,RegisterRequest,RegisterResponse,LoginResponse
from app.schemas.common import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.deps import get_db
from app.services.auth import AuthService
from app.utils.responses import api_success
router = APIRouter(prefix="/auth",tags=["Auth"])

def get_auth_service(db:AsyncSession = Depends(get_db))->AuthService:
    return AuthService(db)
    
@router.post("/login",status_code=status.HTTP_200_OK)
async def login(data:LoginRequest,service:AuthService = Depends(get_auth_service)):
    result = await service.login(data)
    return api_success(data=result,message="Login successful",code=status.HTTP_200_OK)

@router.post("/register",status_code=status.HTTP_200_OK)
async def register(data:RegisterRequest,service:AuthService = Depends(get_auth_service)):
    result = await service.register(data)
    return api_success(data=RegisterResponse.model_validate(result),message="User created successfully",code=status.HTTP_200_OK)
    