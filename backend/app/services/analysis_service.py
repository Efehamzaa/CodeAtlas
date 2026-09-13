import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.scanner_service import ScannerService
from app.engines.architecture.engine import ArchitectureEngine
from app.engines.discovery.engine import DiscoveryEngine

class AnalysisService:
    def __init__(self):
        self.scanner = ScannerService()
        self.architecture = ArchitectureEngine()
        self.discovery = DiscoveryEngine()
        

    async def analyze_full_repository(self, repo_path: str, repo_data: dict, db: AsyncSession) -> dict:
        scan_results = self.scanner.scan_repository(repo_path)
        file_tree = scan_results.get("tree", [])
        config_files = scan_results.get("config_files", [])
        
        analyzed_files_list = []
        all_dependencies = []
        
        
        for relative_path in file_tree:
            if relative_path.endswith('.py'):
                absolute_path = os.path.join(repo_path, relative_path)
                try:
                    with open(absolute_path, "r", encoding="utf-8") as f:
                        source_content = f.read()
                    
                    file_data = self.architecture.analyze_code(source_content)
                    
                    analyzed_files_list.append({
                        "file_path": relative_path,
                        "architecture": {
                            "functions": file_data.get("function", []),
                            "classes": file_data.get("class", []),
                            "imports": file_data.get("import", [])
                        }
                    })
                except Exception as e:
                    print(f"[!] {relative_path} analiz edilemedi: {str(e)}")

        
        for config_file in config_files:
            try:
                file_name = os.path.basename(config_file)
                with open(config_file, "rb") as f:
                    raw_data = f.read()
                
                if raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
                    config_content = raw_data.decode("utf-16", errors="ignore")
                elif raw_data.startswith(b'\xef\xbb\xbf'):
                    config_content = raw_data.decode("utf-8-sig", errors="ignore")
                else:
                    try:
                        config_content = raw_data.decode("utf-8")
                    except UnicodeDecodeError:
                        config_content = raw_data.decode("latin-1")

                deps = self.discovery.analyze_requirements(config_content, file_name)
                if deps:
                    all_dependencies.extend(deps)
            except Exception as e:
                print(f"[!] {config_file} okuma hatası: {str(e)}")

        detected_frameworks = self.discovery.detect_frameworks(all_dependencies)

        
        return {
            "dependencies": all_dependencies,
            "frameworks": detected_frameworks,
            "files": analyzed_files_list
        }