from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Book(Base):
    """小説情報のORM."""

    __tablename__ = "book"

    ncode: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="小説コード")

