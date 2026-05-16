from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import Config
import logging

logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(Config.DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True)
    platform = Column(String(50))  # whatsapp, instagram, messenger
    name = Column(String(255))
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Message(Base):
    """Message model for storing conversation history"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    platform = Column(String(50))  # whatsapp, instagram, messenger
    message_text = Column(Text)
    reply_text = Column(Text)
    message_type = Column(String(50))  # incoming, outgoing
    timestamp = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)

class Conversation(Base):
    """Conversation model for managing chat sessions"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    platform = Column(String(50))
    conversation_summary = Column(Text, nullable=True)
    total_messages = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
