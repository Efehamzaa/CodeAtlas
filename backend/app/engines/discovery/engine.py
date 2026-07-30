from .requirements_parser import parse_requirements
from .package_json import PackageJsonParser

class DiscoveryEngine:
    def __init__(self):
        self.nodejs_parser=PackageJsonParser()

    def analyze_requirements(self, file_content: str , file_name:str) -> list:
        """Ana sistemden gelen requirements.txt içeriğini parser'a iletir."""
        if file_name=="requirements.txt":
            return parse_requirements(file_content)
        elif file_name=="package.json":
            return self.nodejs_parser.parse(file_content)
        else:
            raise ValueError("Desteklenmeyen Dosya Yapısı Tespit Edildi.")
        