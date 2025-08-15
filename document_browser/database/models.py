"""Database models for the document browser application."""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authenticated users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    avatar_url = Column(String(500))
    oauth_provider = Column(String(50), nullable=False)  # e.g., 'google', 'microsoft'
    oauth_id = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    """Document model to track available documents."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    date = Column(String(20), nullable=False)  # Storing as string to match existing format
    file_path = Column(String(500), nullable=False)
    document_type = Column(String(10), nullable=False)  # 'html' or 'pdf'
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    comments = relationship("Comment", back_populates="document", cascade="all, delete-orphan")
    
    # Composite unique constraint for name + date
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )


class Comment(Base):
    """Comment model for user feedback on documents."""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    element_id = Column(String(255))  # For anchoring comments to specific document elements
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_resolved = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="comments")
    document = relationship("Document", back_populates="comments")


class Session(Base):
    """Session model to track user sessions."""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User")