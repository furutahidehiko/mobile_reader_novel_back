from sqlalchemy import Column, Integer, Boolean, ForeignKey,String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from models.base import Base

class Book(Base):
    """小説情報のORM."""

    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ncode: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="小説コード")

