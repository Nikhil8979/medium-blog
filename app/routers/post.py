from fastapi import APIRouter,Depends,status
from app.schemas.post import PostCreate,PostResponse,PostUpdate,PostsQuery
from app.services.post import PostService
from typing import Annotated
from app.utils.responses import api_success
from app.core.security import get_current_user
from app.dependencies import DbSession,CurrentUser
router = APIRouter(prefix="/posts",tags=["Posts"])

def get_post_service(db:DbSession)->PostService:
    return PostService(db)
    
PostServiceDeps = Annotated[PostService,Depends(get_post_service)]
@router.post("/")
async def create_post(data:PostCreate,service:PostServiceDeps,current_user:CurrentUser):
    result = await service.create_post(data,current_user.id)
    return api_success(data=PostResponse.model_validate(result),message="Post Created Successfully",code=status.HTTP_201_CREATED)

@router.get("/{post_id}")
async def get_post(post_id:int,service:PostServiceDeps,current_user:CurrentUser):
    result = await service.get_post(post_id,current_user.id)
    return api_success(data=PostResponse.model_validate(result),message="Post retrieved successfully",code=status.HTTP_200_OK)

@router.get("/")
async def get_posts(postQuery:Annotated[PostsQuery,Depends()],service:Annotated[PostServiceDeps,Depends(get_post_service)],current_user:Annotated[CurrentUser,Depends(get_current_user)]):
    result = await service.get_posts(current_user.id,postQuery);
    return api_success(data=[PostResponse.model_validate(post) for post in result],message="Posts retrieved successfully",code=status.HTTP_200_OK)
    
@router.patch("/{post_id}")
async def update_posts(post_id:int, data:PostUpdate,service:PostServiceDeps,current_user:CurrentUser):
    result = await service.update_post(post_id,data,current_user.id)
    return api_success(data=PostResponse.model_validate(result),message="Post updated successfully",code=status.HTTP_200_OK)

@router.delete("/{post_id}")
async def delete_post(post_id:int,service:PostServiceDeps,current_user:CurrentUser):
    await service.delete_post(post_id=post_id,owner_id=current_user.id)
    return api_success(data=None,message="Post deleted successfully",code=status.HTTP_200_OK)
        