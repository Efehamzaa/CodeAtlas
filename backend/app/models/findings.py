from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    category = Column(String)  
    name = Column(String)      
    version = Column(String, nullable=True)
    confidence = Column(Float, default=1.0)

    
    analysis = relationship("Analysis", back_populates="technologies")

class ProjectStructure(Base):
    __tablename__ = "project_structures"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    entry_point = Column(String, nullable=True)
    
   
    reading_order = Column(JSON, default=list)
    dependency_graph = Column(JSON, default=dict)
    folder_graph = Column(JSON, default=dict)

    analysis = relationship("Analysis", back_populates="project_structures")

class SecurityFinding(Base):
    __tablename__ = "security_findings"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    severity = Column(String) 
    type = Column(String)     
    file_path = Column(String)
    line_number = Column(Integer, nullable=True)

    analysis = relationship("Analysis", back_populates="security_findings")