import os
from pathlib import Path
from collections import Counter

class ScannerService:
    def __init__(self):
        # Tarama dışı bırakılacak klasörler
        self.IGNORE_DIRS = {
            ".git", ".venv", "venv", "__pycache__", "node_modules", 
            ".idea", ".vscode", "dist", "build"
        }
        # Tarama dışı bırakılacak özel dosyalar
        self.IGNORE_FILES = {
            ".DS_Store", ".env"
        }

    def should_ignore(self, path: Path) -> bool:
      
        if path.name in self.IGNORE_DIRS or path.name in self.IGNORE_FILES:
            return True
        return False

    def build_tree(self, repo_path: Path) -> list:
       
        tree = []
        for root, dirs, files in os.walk(repo_path):
            current_path = Path(root)
            

            dirs[:] = [d for d in dirs if not self.should_ignore(current_path / d)]
            
            for file in files:
                file_path = current_path / file
                if not self.should_ignore(file_path):
                    relative_path=file_path.relative_to(repo_path)
                    tree.append(str(relative_path))
                    
        return tree

    def count_languages(self, file_list: list) -> dict:
      
        extensions = []
        for file_path in file_list:
            ext = Path(file_path).suffix.lower()
            if ext: 
                extensions.append(ext)
        
        return dict(Counter(extensions))

    def scan_repository(self, repo_path_str: str) -> dict:
       
        repo_path = Path(repo_path_str)
        
        
        file_tree = self.build_tree(repo_path)
        
        
        language_stats = self.count_languages(file_tree)
        
    
        return {
            "total_files": len(file_tree),
            "language_distribution": language_stats,
            "tree": file_tree
        }
    