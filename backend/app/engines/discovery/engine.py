import json
import re  # Performans için döngü içinden alınıp en başa taşındı
from .requirements_parser import parse_requirements
from .package_json import PackageJsonParser

try:
    import tomllib
except ImportError:
    import toml as tomllib

class DiscoveryEngine:
    
    def analyze_requirements(self, content: str, file_name: str) -> list:
        """
        Dosya adına göre ilgili ayrıştırma metodunu tetikler.
        """
        if file_name == "requirements.txt":
            return self._parse_requirements_txt(content)
        elif file_name == "package.json":
            return self._parse_package_json(content)
        elif file_name == "pyproject.toml":
            return self._parse_pyproject_toml(content)
        else:
            raise ValueError(f"Desteklenmeyen dosya yapısı: {file_name}")

    def _parse_pyproject_toml(self, content: str) -> list:
        """
        Modern Python projelerindeki (PEP 621 ve Poetry) bağımlılıkları çıkarır.
        """
        dependencies = []
        try:
            parsed_data = tomllib.loads(content)
            
            # 1. Standart (PEP 621) Yapısı: project.dependencies
            project_deps = parsed_data.get("project", {}).get("dependencies", [])
            for dep in project_deps:
                name = re.split(r'[>=<~]', dep)[0].strip()
                
                dependencies.append({
                    "name": name,
                    "ecosystem": "pip",
                    "version": None  
                })
            
            # 2. Poetry Yapısı: tool.poetry.dependencies
            poetry_deps = parsed_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            for name, version_info in poetry_deps.items():
                if name.lower() == "python":
                    continue  # Python'un kendi sürüm gereksinimini paket olarak alma
                    
                dependencies.append({
                    "name": name,
                    "ecosystem": "pip",
                    "version": str(version_info) if isinstance(version_info, (str, int, float)) else None
                })
                
        except Exception as e:
            print(f"pyproject.toml ayrıştırılırken hata oluştu: {str(e)}")
            
        return dependencies

    def _parse_requirements_txt(self, content: str) -> list:
        # İçe aktarılan modülü doğrudan çalıştırıyoruz
        return parse_requirements(content)

    def _parse_package_json(self, content: str) -> list:
        # Sınıf örneği oluşturulup ayrıştırma metodu çağrılıyor
        parser = PackageJsonParser()
        return parser.parse(content)