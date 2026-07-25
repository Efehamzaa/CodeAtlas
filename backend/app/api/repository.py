from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.repository import RepositoryRequest
from app.services.repository_service import RepositoryService
from app.services.scanner_service import ScannerService

router = APIRouter(prefix="/repositories", tags=["Repositories"])
repo_service = RepositoryService()
scanner_service=ScannerService()

@router.post("/")
async def analyze_repository(request: RepositoryRequest, background_tasks: BackgroundTasks):
    try:
    
        temp_path = repo_service.clone_repository(request.url)

        scan_results=scanner_service.scan_repository(temp_path)
        
        background_tasks.add_task(repo_service.cleanup_repository, temp_path)
        
        return {
            "status": "success",
            "message": "Repository başarıyla klonlandı ve analiz için hazırlandı.",
            "data": {
                "url": request.url,
                "analysis":scan_results
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="İşlem sırasında sunucu kaynaklı bir hata oluştu.")
    