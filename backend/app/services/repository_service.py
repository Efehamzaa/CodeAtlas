import os
import tempfile
import shutil 
from git import Repo,GitCommandError

class RepositoryService:
    def clone_repository(self,repo_url:str)->str:
        try:
            temp_dir=tempfile.mkdtemp(prefix="codeatlas_")
            Repo.clone_from(repo_url , temp_dir)
            return temp_dir
        
        except GitCommandError as e:
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir , ignore_errors=True)
            raise ValueError(f"Repository klonlanamadı. Erişim yok veya link hatalı: {str(e)}")

        except Exception as e:
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir , ignore_errors=True)
            raise RuntimeError(f"Klonlama sırasında sistem hatası oluştu: {str(e)}")

    def cleanup_repository(self , temp_dir: str):
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir , ignore_errors=True)


    
