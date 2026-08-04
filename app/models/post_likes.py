from app.database.db import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,ForeignKey,DateTime,func,UniqueConstraint
from datetime import datetime
class PostLikes(Base):
    __tablename__ = "post_likes"
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_user_post_like"),
    )
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id",ondelete="CASCADE"),index=True)
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    user:Mapped["User"] = relationship("User",back_populates="liked_posts")
    post:Mapped["Post"] = relationship("Post",back_populates="likes")