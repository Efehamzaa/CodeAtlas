from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.repository import RepositoryRequest, RepositoryResponse
from app.services.repository_service import RepositoryService
from app.services.analysis_service import AnalysisService   
from app.core.database import get_db
from app.services.db_service import save_analysis_results # Yazdığımız kayıt servisi

router = APIRouter(prefix="/repositories", tags=["Repositories"])
repo_service = RepositoryService()
analysis_service = AnalysisService()

@router.post("/", response_model=RepositoryResponse)
async def analyze_repository(request: RepositoryRequest, db: AsyncSession = Depends(get_db)):
    try:
        temp_path = repo_service.clone_repository(request.url)
        
        # 1. Mevcut analiz motoru çalışıyor
        response_data = analysis_service.analyze_full_repository(temp_path)
        
        if hasattr(response_data, 'repository_url'):
            response_data.repository_url = request.url

        # 2. Veritabanına kaydetme işlemi için veriyi hazırlama
        repo_info = {
            "url": request.url,
            "name": request.url.split("/")[-1].replace(".git", ""),
            "owner": request.url.split("/")[-2] if "github.com" in request.url else "Unknown"
        }
        
        # Pydantic objelerini dict yapısına çeviriyoruz
        dependencies_list = [
            dep.model_dump() if hasattr(dep, "model_dump") else (dep.dict() if hasattr(dep, "dict") else dep) 
            for dep in getattr(response_data, 'dependencies', [])
        ]
        
        # 3. Veritabanına yazma işlemini tetikleme
        await save_analysis_results(
            db=db, 
            repo_data={"url": request.url, "name": repo_info["name"], "owner": repo_info["owner"]}, 
            parsed_dependencies=dependencies_list,
            analyzed_files=getattr(response_data, 'files', [])
        )
        
        return response_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Hata detayı: {str(e)}") 
        raise HTTPException(status_code=500, detail="İşlem sırasında sunucu kaynaklı bir hata oluştu.")

    finally:
        if 'temp_path' in locals():
            repo_service.cleanup_repository(temp_path)