from pydantic import BaseModel
from typing import List, Optional , Literal

class Finding(BaseModel):
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    category: str
    file: str
    line: Optional[int] = None
    title: str
    explanation: str
    recommendation: str
    confidence: float

class SecurityAnalysis(BaseModel):
    summary: str
    risk_score: int
    findings: List[Finding]