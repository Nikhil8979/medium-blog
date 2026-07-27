from fastapi import APIRouter,Depends,status
from app.schemas.post import PostCreate,PostResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.deps import get_db
from app.services.post import PostService
from typing import Annotated
from app.utils.responses import api_success
router = APIRouter(prefix="/posts",tags=["Posts"])
DbSession = Annotated[AsyncSession,Depends(get_db)]
def get_post_service(db:DbSession)->PostService:
    return PostService(db)
    
PostServiceDeps = Annotated[PostService,Depends(get_post_service)]
@router.post("/")
async def create_post(data:PostCreate,service:PostServiceDeps):
    result = await service.create_post(data,1)
    return api_success(data=PostResponse.model_validate(result),message="Post Created Successfully",code=status.HTTP_201_CREATED)

@router.get("/{post_id}")
async def get_post(post_id:int,service:PostServiceDeps):
    result = await service.get_post(post_id,1)
    return api_success(data=PostResponse.model_validate(result),message="Post retrieved successfully",code=status.HTTP_200_OK)

@router.get("/")
async def get_posts(service:PostServiceDeps):
    result = await service.get_posts(1);
    return api_success(data=[PostResponse.model_validate(post) for post in result],message="Posts retrieved successfully",code=status.HTTP_200_OK)
    