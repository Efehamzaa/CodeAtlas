from sqlalchemy import JSON, Column, Integer, String, Float, ForeignKey, DateTime, column
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class RepositoryFile(Base):
    __tablename__ = "repository_files"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    path = Column(String)
    extension = Column(String)
    language = Column(String)
    hash = Column(String , nullable=True)

    functions=Column(JSON, default=list)
    classes=Column(JSON, default=list)
    imports=Column(JSON, default=list)

    repository = relationship("Repository", backref="files")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    status = Column(String, default="started")
    confidence_score = Column(Float, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    repository = relationship("Repository", back_populates="analyses")

    technologies = relationship("Technology", back_populates="analysis")
    project_structures = relationship("ProjectStructure", back_populates="analysis")
    security_findings = relationship("SecurityFinding", back_populates="analysis")
    knowledge = relationship("Knowledge", back_populates="analysis", uselist=False)