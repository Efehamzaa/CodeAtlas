import ast
from .base import BaseExtractor

class FunctionExtractor(BaseExtractor):
    def extract(self, node):
        found_functions=[]
        for child in ast.walk(node):
            if isinstance(child  ,(ast.FunctionDef,ast.AsyncFunctionDef)):
                found_functions.append(child.name)
        return found_functions
