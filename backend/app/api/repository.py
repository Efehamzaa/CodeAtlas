from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.repository import RepositoryRequest, RepositoryResponse
from app.core.database import get_db


from app.services.orchestrator import AnalysisOrchestrator

router = APIRouter(prefix="/repositories", tags=["Repositories"])
orchestrator = AnalysisOrchestrator()

@router.post("/", response_model=RepositoryResponse)
async def analyze_repository(request: RepositoryRequest, db: AsyncSession = Depends(get_db)):
    try:
        
        return await orchestrator.run_full_analysis(request.url, db)
        
    except ValueError as e:
        # Geçersiz URL veya kullanıcı kaynaklı hatalar
        raise HTTPException(
            status_code=400, 
            detail={"code": "INVALID_INPUT", "message": str(e)}
        )
    except Exception as e:
        # Sunucu çökmeleri veya beklenmeyen hataların standart formatta loglanıp dönülmesi
        print(f"[!] ORCHESTRATOR HATASI: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail={"code": "ANALYSIS_FAILED", "message": "Analiz sırasında sunucu hatası oluştu."}
        )