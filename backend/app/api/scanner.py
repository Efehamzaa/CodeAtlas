from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from app.engines.discovery.engine import DiscoveryEngine

router = APIRouter(prefix="/api/v1/scan" , tags=["Scanner"])
engine = DiscoveryEngine()

class RequirementsRequest(BaseModel):
    file_name:str
    file_content:str

@router.post("/requirements")
async def scan_requirements(payload:RequirementsRequest):
    try:
        result= engine.analyze_requirements(payload.file_content,payload.file_name)
        return {"filename": payload.file_name , "dependencies":result}
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))
    