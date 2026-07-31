from .base import BaseExtractor
import ast

class ImportExtractor(BaseExtractor):
    def extract(self , node:ast.AST)->list:
        found_imports=[]
        for child in ast.walk(node):
            if isinstance(child , (ast.Import , ast.ImportFrom)):

                for alias in child.names:
                    found_imports.append(alias.name)

        return found_imports
    