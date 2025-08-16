"""
Database package for Multi-Agent AI Chat System.

This package provides database configuration, session management,
and utilities for working with the SQLite database.

Example:
    from app.db import get_db, init_database, DatabaseSession
    
    # Initialize database
    init_database()
    
    # Use in FastAPI dependency
    def get_conversations(db: Session = Depends(get_db)):
        return db.query(Conversation).all()
        
    # Use context manager
    with DatabaseSession() as db:
        conversation = db.query(Conversation).first()
"""

from .database import (
    DatabaseSession,
    create_tables,
    drop_tables,
    get_db,
    init_database,
    reset_database,
    engine,
    SessionLocal,
    DATABASE_URL,
)

__all__ = [
    "DatabaseSession",
    "create_tables", 
    "drop_tables",
    "get_db",
    "init_database",
    "reset_database",
    "engine",
    "SessionLocal", 
    "DATABASE_URL",
]
