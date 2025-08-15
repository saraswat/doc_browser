"""Comment management components for document feedback."""

import streamlit as st
from typing import List, Optional, Dict, Tuple
from datetime import datetime
from database.database import SessionLocal
from database.crud import (
    create_comment, get_comments_for_document, 
    get_user_comments_for_document, delete_comment,
    update_comment, resolve_comment, get_or_create_document
)
from auth.oauth import get_current_user


def render_comment_section(document_name: str, document_date: str, document_type: str):
    """Render the comment section for a document."""
    user = get_current_user()
    if not user:
        st.info("👤 Please log in to view and add comments.")
        return
    
    db = SessionLocal()
    try:
        # Get or create document record
        document = get_or_create_document(
            db=db,
            name=document_name,
            date=document_date,
            file_path=f"content/{document_name}_{document_date}.{document_type}",
            document_type=document_type
        )
        
        st.markdown("---")
        st.subheader("💬 Comments & Feedback")
        
        # Add new comment section
        with st.expander("➕ Add New Comment", expanded=False):
            render_add_comment_form(user, document.id)
        
        # Display existing comments
        comments = get_comments_for_document(db, document.id)
        
        if comments:
            st.markdown(f"**{len(comments)} comment(s)**")
            for comment in comments:
                render_comment(comment, user)
        else:
            st.info("💭 No comments yet. Be the first to add feedback!")
            
    finally:
        db.close()


def render_add_comment_form(user: Dict, document_id: int):
    """Render form to add new comments."""
    with st.form("add_comment_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            comment_text = st.text_area(
                "Your comment:",
                placeholder="Share your thoughts, questions, or feedback about this document...",
                height=100
            )
        
        with col2:
            st.markdown("**Comment Options:**")
            element_id = st.text_input(
                "Link to element (optional):",
                placeholder="e.g., section-1",
                help="Reference a specific section or element in the document"
            )
        
        col_submit, col_cancel = st.columns([1, 1])
        
        with col_submit:
            submitted = st.form_submit_button("💬 Post Comment", use_container_width=True)
        
        with col_cancel:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.experimental_rerun()
        
        if submitted and comment_text.strip():
            db = SessionLocal()
            try:
                comment = create_comment(
                    db=db,
                    user_id=user["id"],
                    document_id=document_id,
                    content=comment_text.strip(),
                    element_id=element_id.strip() if element_id.strip() else None
                )
                st.success("✅ Comment added successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Failed to add comment: {str(e)}")
            finally:
                db.close()
        elif submitted:
            st.warning("⚠️ Please enter a comment before posting.")


def render_comment(comment, current_user: Dict):
    """Render a single comment."""
    # Comment container
    with st.container():
        # Comment header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{comment.user.name}**")
            if comment.user.avatar_url:
                st.image(comment.user.avatar_url, width=30)
        
        with col2:
            time_ago = get_time_ago(comment.created_at)
            st.markdown(f"*{time_ago}*")
            
            if comment.element_id:
                st.markdown(f"🔗 *Linked to: {comment.element_id}*")
        
        with col3:
            if comment.is_resolved:
                st.markdown("✅ **Resolved**")
        
        # Comment content
        st.markdown(f"> {comment.content}")
        
        # Comment actions (only for comment owner)
        if current_user["id"] == comment.user_id:
            col_edit, col_delete, col_resolve = st.columns([1, 1, 1])
            
            with col_edit:
                if st.button("✏️ Edit", key=f"edit_comment_{comment.id}"):
                    render_edit_comment_form(comment)
            
            with col_delete:
                if st.button("🗑️ Delete", key=f"delete_comment_{comment.id}"):
                    if st.session_state.get(f"confirm_delete_{comment.id}"):
                        db = SessionLocal()
                        try:
                            if delete_comment(db, comment.id, current_user["id"]):
                                st.success("Comment deleted!")
                                st.experimental_rerun()
                            else:
                                st.error("Failed to delete comment")
                        finally:
                            db.close()
                    else:
                        st.session_state[f"confirm_delete_{comment.id}"] = True
                        st.warning("Click delete again to confirm")
            
            with col_resolve:
                if not comment.is_resolved:
                    if st.button("✅ Resolve", key=f"resolve_comment_{comment.id}"):
                        db = SessionLocal()
                        try:
                            if resolve_comment(db, comment.id):
                                st.success("Comment marked as resolved!")
                                st.experimental_rerun()
                            else:
                                st.error("Failed to resolve comment")
                        finally:
                            db.close()
        
        # Show update timestamp if different from creation
        if comment.updated_at and comment.updated_at != comment.created_at:
            st.markdown(f"*Updated: {get_time_ago(comment.updated_at)}*")
        
        st.markdown("---")


def render_edit_comment_form(comment):
    """Render form to edit an existing comment."""
    form_key = f"edit_comment_form_{comment.id}"
    
    with st.form(form_key):
        st.markdown("**Edit Comment:**")
        
        new_content = st.text_area(
            "Comment:",
            value=comment.content,
            height=100
        )
        
        col_save, col_cancel = st.columns([1, 1])
        
        with col_save:
            save_clicked = st.form_submit_button("💾 Save Changes")
        
        with col_cancel:
            cancel_clicked = st.form_submit_button("❌ Cancel")
        
        if save_clicked and new_content.strip():
            db = SessionLocal()
            try:
                updated_comment = update_comment(db, comment.id, new_content.strip())
                if updated_comment:
                    st.success("✅ Comment updated successfully!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Failed to update comment")
            finally:
                db.close()
        elif cancel_clicked:
            st.experimental_rerun()


def render_user_comments_sidebar(user: Dict):
    """Render user's recent comments in sidebar."""
    if not user:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Your Recent Comments")
    
    db = SessionLocal()
    try:
        # Get user's recent comments across all documents
        from sqlalchemy.orm import joinedload
        from database.models import Comment
        
        recent_comments = db.query(Comment).options(
            joinedload(Comment.document)
        ).filter(
            Comment.user_id == user["id"]
        ).order_by(Comment.created_at.desc()).limit(5).all()
        
        if recent_comments:
            for comment in recent_comments:
                with st.sidebar.container():
                    st.markdown(f"**{comment.document.name}**")
                    st.markdown(f"*{comment.document.date}*")
                    # Truncate long comments
                    content_preview = comment.content[:100] + "..." if len(comment.content) > 100 else comment.content
                    st.markdown(f"> {content_preview}")
                    st.markdown(f"*{get_time_ago(comment.created_at)}*")
                    
                    if comment.is_resolved:
                        st.markdown("✅ Resolved")
                    
                    st.markdown("---")
        else:
            st.sidebar.info("No comments yet.")
            
    finally:
        db.close()


def get_time_ago(timestamp: datetime) -> str:
    """Get human-readable time ago string."""
    now = datetime.utcnow()
    diff = now - timestamp.replace(tzinfo=None)
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"


def get_comment_statistics(document_name: str, document_date: str) -> Dict:
    """Get comment statistics for a document."""
    db = SessionLocal()
    try:
        from database.crud import get_document_by_name_date
        document = get_document_by_name_date(db, document_name, document_date)
        
        if not document:
            return {"total": 0, "resolved": 0, "unresolved": 0}
        
        comments = get_comments_for_document(db, document.id)
        resolved_count = sum(1 for c in comments if c.is_resolved)
        
        return {
            "total": len(comments),
            "resolved": resolved_count,
            "unresolved": len(comments) - resolved_count
        }
        
    finally:
        db.close()