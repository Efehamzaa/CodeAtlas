import os
import uuid
import shutil
from git import Repo

def clone_and_map_repo(repo_url: str):
    # Her analiz için benzersiz, geçici bir klasör oluştur
    repo_id = str(uuid.uuid4())[:8]
    temp_dir = f"./temp_repos/{repo_id}"
    
    repository_files = []
    
    try:
        # 1. Aşama: Depoyu Klonla
        print(f"[*] {repo_url} klonlanıyor...")
        Repo.clone_from(repo_url, temp_dir)
        
        # 2. Aşama: Dosya Hiyerarşisini Çıkart (AST Ön Hazırlığı)
        for root, dirs, files in os.walk(temp_dir):
            # .git klasörünü analizden hariç tut
            if '.git' in root:
                continue
                
            for file in files:
                full_path = os.path.join(root, file)
                # Geçici klasör yolunu temizleyip sadece dosya adını al
                relative_path = full_path.replace(f"{temp_dir}/", "").replace(f"{temp_dir}\\", "")
                # Frontend'in beklediği JSON formatı: {"path": "klasor/dosya.py"}
                repository_files.append({"path": relative_path})
                
        return {"repository_files": repository_files, "temp_dir": temp_dir}
        
    except Exception as e:
        print(f"[!] Klonlama Hatası: {e}")
        return {"error": str(e), "repository_files": []}