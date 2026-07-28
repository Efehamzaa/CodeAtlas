from pydantic import BaseModel , field_validator
from urllib.parse import urlparse
from typing import List , Optional

class RepositoryRequest(BaseModel):
    url: str
    @field_validator("url")
    @classmethod
    def check_github_url(cls,value:str) -> str:
        value = value.strip()

        if not value.lower().startswith("https://github.com/"):
            raise ValueError("Lütfen geçerli bir GitHub repository URL'si girin.")

        parsed=urlparse(value)
        path_parts=[p for p in parsed.path.strip("/").split("/") if p]

        if path_parts and path_parts[-1].endswith(".git"):
            path_parts[-1]=path_parts[-1][:-4]

        if len(path_parts)<2:
            raise ValueError("Geçerli bir repository belirtmelisiniz (Örn: https://github.com/kullanici/repo).")
        return value

class Dependency(BaseModel):
    name:str
    ecosystem:str
    version:Optional[str] = None

class Framework(BaseModel):
    name:str
    ecosystem:str

class RepositoryResponse(BaseModel):
    dependencies : List[Dependency] = []
    frameworks : List[Framework] = []

