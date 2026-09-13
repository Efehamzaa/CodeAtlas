from pydantic import BaseModel, Field
from typing import List, Optional


class RepositoryFile(BaseModel):
    path: str

class Dependency(BaseModel):
    name: str
    version: Optional[str] = "Bilinmiyor"

class Framework(BaseModel):
    name: str
    ecosystem: Optional[str] = "Sistem"

class SecurityFinding(BaseModel):
    type: str
    severity: str
    description: str
    file_path: str = "Belirtilmemiş"
    line_number: Optional[int] = 0
    recommendation: Optional[str] = None


class RepositoryRequest(BaseModel):
    url: str


class RepositoryResponse(BaseModel):
    repository_url: str
    risk_score: int = Field(default=0, ge=0, le=100)
    repository_files: List[RepositoryFile] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)
    frameworks: List[Framework] = Field(default_factory=list)
    vulnerabilities: List[SecurityFinding] = Field(default_factory=list)



