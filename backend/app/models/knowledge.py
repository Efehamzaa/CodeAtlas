from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))

    summary = Column(Text, nullable=True)
    tech_summary = Column(Text, nullable=True)
    architecture_summary = Column(Text, nullable=True)
    security_summary = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)

    analysis = relationship("Analysis", back_populates="knowledge")
    conversations = relationship("AIConversation", back_populates="knowledge")

class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge.id"))
    role = Column(String)  
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    knowledge = relationship("Knowledge", back_populates="conversations")