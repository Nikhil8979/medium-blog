from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostCreate,PostStatus,PostUpdate
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
            owner_id=owner_id,
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
            Post.owner_id == owner_id
            )
        result = await self.db.execute(stmt)
        post = result.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404,detail="Post not found with the given id")
        return post
    
    async def get_posts(self,owner_id:int):
        stmt = select(Post).where(Post.owner_id == owner_id)
        result = await self.db.execute(stmt)
        posts = result.scalars().all()
        return posts
    
    async def update_post(self,post_id:int,data:PostUpdate,owner_id:int):
        stmt = select(Post).where(Post.id == post_id,owner_id ==owner_id)
        result = await self.db.execute(stmt)
        post = result.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=400,detail="Post not found with the given id")
        update_data = data.model_dump(exclude_unset=True)
        if "title" in update_data:
            post.title = update_data["title"]
            post.slug = slugify(update_data["title"])
        if "content" in update_data:
            post.content = update_data["content"]
        if "image_url" in update_data:
            post.image_url = update_data["image_url"]
        if "status" in update_data:
            status = update_data["status"]
            post.status = update_data["status"]
            if status == PostStatus.PUBLISHED and post.published_at is None:
                post.published_at = datetime.now(timezone.utc)
            if status != PostStatus.PUBLISHED:
                post.published_at = None
        await self.db.commit()
        await self.db.refresh(post)
        return post                    
    
    async def delete_post(self,post_id:int,owner_id:int):
        stmt = select(Post).where(Post.id == post_id,Post.owner_id == owner_id);
        result = await self.db.execute(stmt)
        post = result.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404,detail="Post not found with the given id")
        await self.db.delete(post)
        await self.db.commit()
        