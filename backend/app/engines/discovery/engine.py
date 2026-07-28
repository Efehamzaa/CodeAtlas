from .requirements_parser import parse_requirements

class DiscoveryEngine:
    def __init__(self):
        pass

    def analyze_requirements(self, file_content: str) -> list[dict]:
        """Ana sistemden gelen requirements.txt içeriğini parser'a iletir."""
        return parse_requirements(file_content)