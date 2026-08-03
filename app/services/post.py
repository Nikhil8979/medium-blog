from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostCreate,PostStatus,PostUpdate,PostsQuery
from app.models.post import Post
from datetime import datetime,timezone,time
from app.utils.post import slugify
from sqlalchemy import select,or_
from sqlalchemy.orm import selectinload
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
            published_at=datetime.now(timezone.utc) if data.status == PostStatus.PUBLISHED else None,
            tags=data.tags
        )
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post
    
    async def get_post(self,post_id:int,owner_id:int):
        stmt = select(Post).where(
            Post.id == post_id,
            Post.owner_id == owner_id
            ).options(selectinload(Post.author))
        result = await self.db.execute(stmt)
        post = result.scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404,detail="Post not found with the given id")
        return post
    
    async def get_posts(self,owner_id:int,postQuery:PostsQuery):
        stmt = select(Post).where(Post.owner_id == owner_id).options(selectinload(Post.author))
        if postQuery.search is not None:
            stmt = stmt.where(
                Post.title.ilike(f"%{postQuery.search}%")
                )
        if(postQuery.status is not None):
            stmt = stmt.where(
                Post.status == postQuery.status
            )    

        if postQuery.tags:
            tags_list = [t.strip().lower() for t in postQuery.tags.split(",") if t.strip()]
            stmt = stmt.where(
                or_(*[Post.tags.contains([tag]) for tag in tags_list])
            )
        if postQuery.start_date:
            start_date = datetime.combine(postQuery.start_date,time.min)
            stmt = stmt.where(Post.created_at >= start_date)
        if postQuery.end_date:
                    end_date = datetime.combine(postQuery.end_date,time.max)
                    stmt = stmt.where(Post.created_at <= end_date)    
        
        stmt = stmt.order_by(Post.created_at.desc())
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
        if "tags" in update_data["tags"]:
            post.tags = update_data["tags"]                        
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
        