from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post_like import LikeCreate,UnlikePost
from app.models.post_likes import PostLikes
from sqlalchemy import select
from fastapi import HTTPException
class PostLikeService:
    def __init__(self,db:AsyncSession):
        self.db = db
        
    async def like_post(self,data:LikeCreate,user_id:int):
        post_like = PostLikes(user_id=user_id,post_id=data.post_id)
        self.db.add(post_like)
        await self.db.commit()
        await self.db.refresh(post_like)
        return post_like
    
    async def unlike_post(self,data:UnlikePost,user_id:int):
        stmt = select(PostLikes).where(PostLikes.post_id == data.post_id,PostLikes.user_id == user_id)
        result = await self.db.execute(stmt)
        post = result.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404,detail="Post not found with the given id")
        await self.db.delete(post)
        await self.db.commit()