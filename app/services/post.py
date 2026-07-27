from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostCreate,PostStatus
from app.models.post import Post
from datetime import datetime,timezone
from app.utils.post import slugify
from sqlalchemy import select
from fastapi import HTTPException
class PostService:
    def __init__(self,db:AsyncSession):
        self.db = db
    
    
    async def create_post(self,data:PostCreate,owner_id:int):
        post = Post(
            title=data.title,
            content=data.content,
            image_url=str(data.image_url) if data.image_url else None,
            status=data.status,
            owner_id=1,
            slug=slugify(data.title),
            published_at=datetime.now(timezone.utc) if data.status == PostStatus.PUBLISHED else None
        )
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post
    
    async def get_post(self,post_id:int,owner_id:int):
        stmt = select(Post).where(
            Post.id == post_id,
            owner_id == 1
            )
        result = await self.db.execute(stmt)
        post = result.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404,detail="Post not found with the given id")
        return post
    
    async def get_posts(self,owner_id:int):
        stmt = select(Post).where(Post.owner_id == 1)
        result = await self.db.execute(stmt)
        posts = result.scalars().all()
        return posts