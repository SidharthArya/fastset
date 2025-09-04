from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime




Base = declarative_base()

class SoftDeleteMixin:
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

class DeclaredBase(Base, SoftDeleteMixin):
    __abstract__ = True 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow(), onupdate=datetime.utcnow())
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None, nullable=True)



