from app.database.db import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,ForeignKey,Enum as SqlEnum,DateTime,func,Text
from enum import Enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
class PostStatus(str,Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    
class Post(Base):
    __tablename__ = "posts"
    
    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title:Mapped[str] = mapped_column(String(220),nullable=False)
    content:Mapped[str] = mapped_column(Text,nullable=False)
    image_url:Mapped[str | None] = mapped_column(String,nullable=True)
    owner_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    slug:Mapped[str] = mapped_column(String(220),unique=True,nullable=False,index=True)
    status: Mapped[PostStatus] = mapped_column(
    SqlEnum(
        PostStatus,
        name="post_status",
        values_callable=lambda enum_cls: [e.value for e in enum_cls], 
    ),
    nullable=False,
    default=PostStatus.DRAFT,
    server_default="draft",
    index=True,
    )
    author:Mapped["User"] = relationship("User",back_populates="posts")
    published_at:Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    tags:Mapped[list[str]] = mapped_column(JSONB,nullable=False,default=[])
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
   