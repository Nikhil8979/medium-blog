from pydantic import BaseModel,Field,HttpUrl,field_validator,model_validator,ConfigDict
from app.models.post import PostStatus
from typing import Optional
from datetime import datetime
from pydantic_core import PydanticCustomError

class PostCreate(BaseModel):
    title:str = Field(...,min_length=3,max_length=220)
    content:str = Field(...,min_length=3,max_length=5000)
    status:PostStatus = PostStatus.DRAFT
    image_url:Optional[HttpUrl] = None
    tags:list[str] = Field(default_factory=list)
    
    @field_validator("tags")
    @classmethod
    def normalize_tags(cls,tags:list[str]) -> list[str]:
        cleaned = []
        seen = set()
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in seen:
                seen.add(tag)
                cleaned.append(tag)
        return cleaned        
class Author(BaseModel):
    id:int
    name:str
    model_config = ConfigDict(from_attributes=True)
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
    tags:list[str]
    author:Author | None
    model_config = ConfigDict(from_attributes=True)

    

class PostUpdate(BaseModel):
    title:Optional[str] = Field(None,min_length=3,max_length=220)
    content:Optional[str] = Field(None,min_length=3,max_length=5000)
    image_url:Optional[str] = None
    status:Optional[PostStatus] = None    
    tags:list[str] = Field(default_factory=list)
    
    @field_validator("tags")
    @classmethod
    def normalize_tags(cls,tags:list[str]) -> list[str]:
        cleaned = []
        seen = set()
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in seen:
                seen.add(tag)
                cleaned.append(tag)
        return cleaned  

class PostsQuery(BaseModel):
    search:Optional[str] = Field(None)
    status:Optional[PostStatus] = None
    tags:Optional[str] = None
    start_date:Optional[datetime] = None
    end_date:Optional[datetime] = None
    
    @model_validator(mode="after")
    def validate_date_range(self):  
        if(self.start_date and self.end_date and self.start_date > self.end_date):
            raise PydanticCustomError(
                "date_range_error",
                "start_date must be less than or equal to end_date",
            )

        return self
        