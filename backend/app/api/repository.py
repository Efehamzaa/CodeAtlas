from fastapi import APIRouter, HTTPException
from app.schemas.repository import RepositoryRequest, RepositoryResponse
from app.services.repository_service import RepositoryService
from app.services.analysis_service import AnalysisService   

router = APIRouter(prefix="/repositories", tags=["Repositories"])
repo_service = RepositoryService()
analysis_service = AnalysisService()

@router.post("/" , response_model=RepositoryResponse)
async def analyze_repository(request: RepositoryRequest):
    try:
        
        temp_path = repo_service.clone_repository(request.url)

        
        response_data = analysis_service.analyze_full_repository(temp_path)
        
        
        if hasattr(response_data, 'repository_url'):
            response_data.repository_url = request.url

        
        return response_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        
        print(f"Hata detayı: {str(e)}") 
        raise HTTPException(status_code=500, detail="İşlem sırasında sunucu kaynaklı bir hata oluştu.")

    finally:
    
        if 'temp_path' in locals():
            repo_service.cleanup_repository(temp_path)