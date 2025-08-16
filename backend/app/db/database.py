"""
Database configuration and session management for Multi-Agent AI Chat System.

This module provides database connection, session management, and initialization
functionality using SQLAlchemy with SQLite.
"""
import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from ..models.base import Base


# Database configuration
def get_database_url() -> str:
    """
    Get database URL from environment or use default SQLite path.
    
    Returns:
        Database connection URL
    """
    # Get from environment or use default SQLite path
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    
    # Default SQLite database in data directory
    data_dir = Path(__file__).parent.parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    db_path = data_dir / "chatbot.db"
    
    return f"sqlite:///{db_path}"


# Create database engine
DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL,
    # SQLite specific configuration
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    # Echo SQL queries in development
    echo=os.getenv("DEBUG", "false").lower() == "true"
)


# Enable foreign key constraints for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key constraints for SQLite connections."""
    if "sqlite" in str(dbapi_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def create_tables() -> None:
    """
    Create all database tables.
    
    This function creates all tables defined in the models.
    Safe to call multiple times - will only create missing tables.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """
    Drop all database tables.
    
    WARNING: This will delete all data in the database.
    Use only for testing or development reset.
    """
    Base.metadata.drop_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection.
    
    This function provides a database session that automatically
    handles cleanup and error handling.
    
    Yields:
        Database session
        
    Example:
        from fastapi import Depends
        
        def get_conversations(db: Session = Depends(get_db)):
            return db.query(Conversation).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def init_database() -> None:
    """
    Initialize database with tables and any required data.
    
    This function should be called when the application starts
    to ensure the database is properly set up.
    """
    # Create tables
    create_tables()
    
    # Add any initial data here if needed
    # For example, default agent configurations could be stored
    # in the database if we decide to make them dynamic later
    
    print(f"Database initialized at: {DATABASE_URL}")


def reset_database() -> None:
    """
    Reset database by dropping and recreating all tables.
    
    WARNING: This will delete ALL data in the database.
    Use only for development or testing.
    """
    print("WARNING: Resetting database - all data will be lost!")
    drop_tables()
    create_tables()
    print("Database reset complete")


# Context manager for database sessions
class DatabaseSession:
    """
    Context manager for database sessions.
    
    Provides automatic session management with proper cleanup
    and error handling.
    
    Example:
        with DatabaseSession() as db:
            conversation = db.query(Conversation).first()
            print(conversation.goal_description)
    """
    
    def __init__(self):
        self.db = None
    
    def __enter__(self) -> Session:
        """Enter the context - create database session."""
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context - cleanup database session."""
        if exc_type is not None:
            # Exception occurred, rollback transaction
            self.db.rollback()
        else:
            # No exception, commit transaction
            self.db.commit()
        
        # Always close the session
        self.db.close()
        self.db = None
