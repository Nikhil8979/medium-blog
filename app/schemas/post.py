from pydantic import BaseModel,Field,HttpUrl
from app.models.post import PostStatus
from typing import Optional
from datetime import datetime
class PostCreate(BaseModel):
    title:str = Field(...,min_length=3,max_length=220)
    content:str = Field(...,min_length=3,max_length=5000)
    status:PostStatus = PostStatus.DRAFT
    image_url:Optional[HttpUrl] = None
    

class PostResponse(BaseModel):
    id:int
    title:str 
    content:str
    status:PostStatus
    slug:str
    image_url:Optional[str] = None
    owner_id: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}