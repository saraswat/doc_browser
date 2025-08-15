"""CRUD operations for database models."""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime, timedelta
from .models import User, Document, Comment, Session as DBSession
import secrets


def get_or_create_user(db: Session, email: str, name: str, oauth_provider: str, 
                      oauth_id: str, avatar_url: Optional[str] = None) -> User:
    """Get existing user or create new one."""
    user = db.query(User).filter(
        and_(User.email == email, User.oauth_provider == oauth_provider)
    ).first()
    
    if not user:
        user = User(
            email=email,
            name=name,
            avatar_url=avatar_url,
            oauth_provider=oauth_provider,
            oauth_id=oauth_id,
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update user info in case it changed
        user.name = name
        user.avatar_url = avatar_url
        user.last_login = datetime.utcnow()
        db.commit()
    
    return user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def create_session(db: Session, user_id: int, expires_hours: int = 24) -> str:
    """Create a new user session."""
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
    
    db_session = DBSession(
        session_token=session_token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(db_session)
    db.commit()
    
    return session_token


def get_user_by_session(db: Session, session_token: str) -> Optional[User]:
    """Get user by session token."""
    session = db.query(DBSession).filter(
        and_(
            DBSession.session_token == session_token,
            DBSession.is_active == True,
            DBSession.expires_at > datetime.utcnow()
        )
    ).first()
    
    if session:
        return session.user
    return None


def invalidate_session(db: Session, session_token: str) -> bool:
    """Invalidate a user session."""
    session = db.query(DBSession).filter(
        DBSession.session_token == session_token
    ).first()
    
    if session:
        session.is_active = False
        db.commit()
        return True
    return False


def get_or_create_document(db: Session, name: str, date: str, 
                          file_path: str, document_type: str, 
                          description: Optional[str] = None) -> Document:
    """Get existing document or create new one."""
    document = db.query(Document).filter(
        and_(Document.name == name, Document.date == date)
    ).first()
    
    if not document:
        document = Document(
            name=name,
            date=date,
            file_path=file_path,
            document_type=document_type,
            description=description
        )
        db.add(document)
        db.commit()
        db.refresh(document)
    
    return document


def get_document_by_name_date(db: Session, name: str, date: str) -> Optional[Document]:
    """Get document by name and date."""
    return db.query(Document).filter(
        and_(Document.name == name, Document.date == date)
    ).first()


def create_comment(db: Session, user_id: int, document_id: int, 
                  content: str, element_id: Optional[str] = None) -> Comment:
    """Create a new comment."""
    comment = Comment(
        user_id=user_id,
        document_id=document_id,
        content=content,
        element_id=element_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments_for_document(db: Session, document_id: int) -> List[Comment]:
    """Get all comments for a document."""
    return db.query(Comment).filter(
        Comment.document_id == document_id
    ).order_by(Comment.created_at.desc()).all()


def get_user_comments_for_document(db: Session, user_id: int, 
                                 document_id: int) -> List[Comment]:
    """Get user's comments for a specific document."""
    return db.query(Comment).filter(
        and_(Comment.user_id == user_id, Comment.document_id == document_id)
    ).order_by(Comment.created_at.desc()).all()


def update_comment(db: Session, comment_id: int, content: str) -> Optional[Comment]:
    """Update a comment's content."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        comment.content = content
        comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(comment)
    return comment


def delete_comment(db: Session, comment_id: int, user_id: int) -> bool:
    """Delete a comment (only by the user who created it)."""
    comment = db.query(Comment).filter(
        and_(Comment.id == comment_id, Comment.user_id == user_id)
    ).first()
    
    if comment:
        db.delete(comment)
        db.commit()
        return True
    return False


def resolve_comment(db: Session, comment_id: int) -> bool:
    """Mark a comment as resolved."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        comment.is_resolved = True
        db.commit()
        return True
    return False