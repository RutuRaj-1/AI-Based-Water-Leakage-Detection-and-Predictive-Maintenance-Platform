"""
SQLAlchemy declarative base and audit mixin classes.

This module provides:
- Base: Declarative base for all ORM models
- TimestampMixin: Adds created_at and updated_at columns
- AuditMixin: Extends TimestampMixin with created_by, updated_by, and is_deleted (soft delete)

Usage:
    from app.db.base import Base, AuditMixin
    from sqlalchemy import Column, String
    from uuid import UUID
    
    class MyModel(AuditMixin, Base):
        __tablename__ = "my_model"
        id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
        name: Mapped[str] = mapped_column(String(255))
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

# Declarative base for all ORM models
Base = declarative_base()


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AuditMixin(TimestampMixin):
    """
    Mixin that adds full audit trail and soft-delete support.
    Extends TimestampMixin with created_by, updated_by, and is_deleted.
    """

    created_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="User ID or system process that created the record",
    )
    updated_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="User ID or system process that last updated the record",
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,  # Index for filtering active records
        comment="Soft delete flag; True = logically deleted, preserved in DB",
    )
