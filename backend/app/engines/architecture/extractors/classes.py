import ast
from .base import BaseExtractor

class ClassExtractor(BaseExtractor):
    def extract(self, node):
        found_classes=[]
        for child in ast.walk(node):
            if isinstance(child , ast.ClassDef):
                found_classes.append(child.name)
        return found_classes

