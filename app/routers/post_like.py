from fastapi import APIRouter,Depends
from app.schemas.post_like import LikeCreate,LikeResponse,UnlikePost
from typing import Annotated
from app.utils.responses import api_success
from app.dependencies import DbSession,CurrentUser
from app.services.post_like import PostLikeService
def get_post_like_service(db:DbSession)->PostLikeService:
    return PostLikeService(db=db)

PostLikeServiceDeps = Annotated[PostLikeService,Depends(get_post_like_service)]
router = APIRouter(prefix="/post",tags=["Post Likes"])

@router.post("/like")
async def like_post(data:LikeCreate,service:PostLikeServiceDeps,current_user:CurrentUser):
    result = await service.like_post(data,current_user.id)
    return api_success(LikeResponse.model_validate(result),"Post liked successfully",code=201)

@router.delete("/unlike")
async def unlike_post(data:UnlikePost,service:PostLikeServiceDeps,current_user:CurrentUser):
    await service.unlike_post(data=data,user_id=current_user.id)
    return api_success(data=None,message="Success",code=200)