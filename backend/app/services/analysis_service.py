import os
from app.services.scanner_service import ScannerService
from app.engines.architecture.engine import ArchitectureEngine
from app.schemas.repository import RepositoryResponse, AnalyzedFile, FileArchitecture
from app.engines.discovery.engine import DiscoveryEngine

class AnalysisService:
    def __init__(self):
        self.scanner = ScannerService()
        self.architecture = ArchitectureEngine()
        self.discovery = DiscoveryEngine()

    def analyze_full_repository(self, repo_path: str) -> RepositoryResponse:
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
                    
                    
                    arch_data = FileArchitecture(
                        functions=file_data.get("function", []),
                        classes=file_data.get("class", []),
                        imports=file_data.get("import", [])
                    )
                    
                    
                    analyzed_file = AnalyzedFile(
                        file_path=relative_path,
                        architecture=arch_data
                    )
                    analyzed_files_list.append(analyzed_file)
                    
                except Exception as e:
                    print(f"Uyarı: {relative_path} analiz edilemedi. Hata: {str(e)}")


        print("--- TEST BAŞLANGICI ---")
        print("BULUNAN CONFIG DOSYALARI:", config_files)

        for config_file in config_files:
            try:
                file_name = os.path.basename(config_file)
                print(f"> Şu an inceleniyor: {file_name}")
                with open(config_file, "r", encoding="utf-8") as f:
                    config_content = f.read()

                deps=self.discovery.analyze_requirements(config_content , file_name)
                print(f"> Motordan dönen sonuç: {deps}")
                if deps:
                    all_dependencies.extend(deps)
            except Exception as e:
                print(f"Uyarı: {config_file} analiz edilemedi. Hata: {str(e)}")

        return RepositoryResponse(
            files=analyzed_files_list, 
            frameworks=[], 
            dependencies=all_dependencies
        )