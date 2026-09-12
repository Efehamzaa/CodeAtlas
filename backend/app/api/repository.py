from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import os
from app.schemas.repository import RepositoryRequest
from app.services.repository_service import RepositoryService
from app.services.analysis_service import AnalysisService   
from app.core.database import get_db

from app.engines.security.SecurityEngine import SecurityEngine
# Kendi dosya yolunuza göre içe aktarın (Dosyanızın adı AlEngine.py ise ona göre yazın)
from app.engines.ai.AlEngine import AIEngine 

router = APIRouter(prefix="/repositories", tags=["Repositories"])
repo_service = RepositoryService()
analysis_service = AnalysisService()
security_engine = SecurityEngine()
ai_engine = AIEngine()

@router.post("/")
async def analyze_repository(request: RepositoryRequest, db: AsyncSession = Depends(get_db)):
    try:
        temp_path = repo_service.clone_repository(request.url)
        
        repo_info = {
            "url": request.url,
            "name": request.url.split("/")[-1].replace(".git", ""),
            "owner": request.url.split("/")[-2] if "github.com" in request.url else "Unknown"
        }
        
        response_data = await analysis_service.analyze_full_repository(
            repo_path=temp_path,
            repo_data=repo_info,
            db=db
        )
        
        if hasattr(response_data, 'model_dump'):
            response_dict = response_data.model_dump()
        elif hasattr(response_data, 'dict'):
            response_dict = response_data.dict()
        else:
            response_dict = dict(response_data)
            
        response_dict["repository_url"] = request.url

        repository_files = []
        raw_vulnerabilities = []

        # 1. Statik Kod Analizi (SAST)
        for root_dir, dirs, files in os.walk(temp_path):
            if '.git' in root_dir:
                continue
            for file in files:
                full_path = os.path.join(root_dir, file)
                relative_path = full_path.replace(f"{temp_path}/", "").replace(f"{temp_path}\\", "")
                repository_files.append({"path": relative_path})
                
                if file.endswith(".py"):
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            code_content = f.read()
                        
                        findings = security_engine.analyze_code(code_content)
                        for finding in findings:
                            finding["file_path"] = relative_path
                            raw_vulnerabilities.append(finding)
                    except Exception as e:
                        print(f"[!] Dosya okuma hatası ({relative_path}): {e}")

        if "dependencies" in response_dict and response_dict["dependencies"]:
            dep_findings = security_engine.analyze_dependencies(response_dict["dependencies"])
            raw_vulnerabilities.extend(dep_findings)

        # 2. YAPAY ZEKA (LLM) ENTEGRASYONU
        final_vulnerabilities = []
        risk_score = 0
        
        if raw_vulnerabilities:
            ai_report = ai_engine.generate_remediation_report(raw_vulnerabilities)
            
            # AI başarılı çalıştıysa veriyi Frontend modeline haritala
            if ai_report and "findings" in ai_report:
                risk_score = ai_report.get("risk_score", 0)
                for ai_finding in ai_report["findings"]:
                    final_vulnerabilities.append({
                        "type": ai_finding.get("title", "Zafiyet"),
                        "severity": ai_finding.get("severity", "HIGH"),
                        "description": ai_finding.get("explanation", ""),
                        "file_path": ai_finding.get("file", "Belirtilmemiş"),
                        "recommendation": ai_finding.get("recommendation", "")
                    })
            else:
                # AI'dan yanıt gelmezse orjinal SAST verilerini kullan
                final_vulnerabilities = raw_vulnerabilities

        response_dict["repository_files"] = repository_files
        response_dict["vulnerabilities"] = final_vulnerabilities
        response_dict["risk_score"] = risk_score
        
        return response_dict
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Hata detayı: {str(e)}") 
        raise HTTPException(status_code=500, detail="İşlem sırasında sunucu kaynaklı bir hata oluştu.")

    finally:
        if 'temp_path' in locals():
            repo_service.cleanup_repository(temp_path)