import os
from app.services.db_service import save_analysis_results
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.repository import (
    RepositoryResponse, RepositoryFile, Dependency, Framework, SecurityFinding
)
from app.services.repository_service import RepositoryService
from app.services.analysis_service import AnalysisService
from app.engines.security.SecurityEngine import SecurityEngine
from app.engines.ai.AlEngine import AIEngine 

class AnalysisOrchestrator:
    def __init__(self):
        self.repo_service = RepositoryService()
        self.analysis_service = AnalysisService()
        self.security_engine = SecurityEngine()
        self.ai_engine = AIEngine()

    async def run_full_analysis(self, repo_url: str, db: AsyncSession) -> RepositoryResponse:
        temp_path = None
        try:
            temp_path = self.repo_service.clone_repository(repo_url)

            repo_info = {
                "url": repo_url,
                "name": repo_url.split("/")[-1].replace(".git", ""),
                "owner": repo_url.split("/")[-2] if "github.com" in repo_url else "Unknown"
            }

            base_analysis = await self.analysis_service.analyze_full_repository(
                repo_path=temp_path, repo_data=repo_info, db=db
            )
            
            analysis_dict = base_analysis if isinstance(base_analysis, dict) else (base_analysis.model_dump() if hasattr(base_analysis, 'model_dump') else dict(base_analysis))

            repository_files = []
            raw_vulnerabilities = []
            
            # Sadece .py değil, tüm kritik uzantılar hedefleniyor
            target_extensions = ('.py', '.env', '.json', '.yml', '.yaml', '.ini', '.txt')

            for root_dir, dirs, files in os.walk(temp_path):
                if '.git' in root_dir:
                    continue
                for file in files:
                    full_path = os.path.join(root_dir, file)
                    relative_path = full_path.replace(f"{temp_path}/", "").replace(f"{temp_path}\\", "")
                    repository_files.append(RepositoryFile(path=relative_path))

                    if file.endswith(target_extensions):
                        try:
                            with open(full_path, "r", encoding="utf-8") as f:
                                code_content = f.read()
                            
                            findings = []
                            # Python ise AST analizi, değilse Ham (Raw) Regex analizi çalışır
                            if file.endswith(".py"):
                                findings = self.security_engine.analyze_code(code_content)
                            else:
                                findings = self.security_engine.analyze_raw_secrets(code_content)
                                
                            for finding in findings:
                                raw_vulnerabilities.append({
                                    "type": finding.get("type", "Bilinmeyen"),
                                    "severity": finding.get("severity", "MEDIUM"),
                                    "description": finding.get("description", ""),
                                    "file_path": relative_path,
                                    "line_number": finding.get("line_number", 0)
                                })
                        except UnicodeDecodeError:
                            pass # Binary dosyaları sessizce atla
                        except Exception as e:
                            print(f"[!] Dosya okuma hatası ({relative_path}): {e}")

            dependencies_list = analysis_dict.get("dependencies", [])
            if dependencies_list:
                dep_findings = self.security_engine.analyze_dependencies(dependencies_list)
                raw_vulnerabilities.extend(dep_findings)

            final_vulnerabilities = []
            risk_score = 0

            if raw_vulnerabilities:
                ai_report = self.ai_engine.generate_remediation_report(raw_vulnerabilities)
                if ai_report and "findings" in ai_report:
                    risk_score = ai_report.get("risk_score", 0)
                    for ai_finding in ai_report["findings"]:
                        final_vulnerabilities.append(SecurityFinding(
                            type=ai_finding.get("title", "Zafiyet"),
                            severity=ai_finding.get("severity", "HIGH"),
                            description=ai_finding.get("explanation", ""),
                            file_path=ai_finding.get("file", "Belirtilmemiş"),
                            recommendation=ai_finding.get("recommendation", "")
                        ))
                else:
                    final_vulnerabilities = [SecurityFinding(**rv) for rv in raw_vulnerabilities]

            deps = [Dependency(**d) if isinstance(d, dict) else Dependency(name=getattr(d, 'name', str(d))) for d in dependencies_list]
            fws = [Framework(**f) if isinstance(f, dict) else Framework(name=getattr(f, 'name', str(f))) for f in analysis_dict.get("frameworks", [])]


            await save_analysis_results(
                db=db,
                repo_url=repo_url,
                risk_score=risk_score,
                dependencies=deps,
                frameworks=fws,
                analyzed_files=analysis_dict.get("files", []),
                security_findings=final_vulnerabilities
            )

            return RepositoryResponse(
                repository_url=repo_url,
                risk_score=risk_score,
                repository_files=repository_files,
                dependencies=deps,
                frameworks=fws,
                vulnerabilities=final_vulnerabilities
            )

        finally:
            if temp_path:
                self.repo_service.cleanup_repository(temp_path)