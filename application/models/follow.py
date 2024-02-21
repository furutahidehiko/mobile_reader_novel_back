from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from pydantic import BaseModel,Field

from models.base import Base



class Follow(Base):
    """お気に入りテーブルのORM."""

    __tablename__ = "follow"

    read_history_id = Column(Integer, ForeignKey('read_history.id'), nullable=False)
    is_follow = Column(Boolean, default=False, nullable=False)

class FollowResponse(BaseModel):
    is_success: bool = Field(..., title="お気に入り登録してるかどうか")

    class Config:
        json_schema_extra = {
            "example": {
                "is_success": True
            }
        }