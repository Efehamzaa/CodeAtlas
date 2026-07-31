import ast
from .extractors.imports import ImportExtractor
from .extractors.classes import ClassExtractor
from .extractors.functions import FunctionExtractor

class ArchitectureEngine:
    def __init__(self):
        self.import_extractor=ImportExtractor()
        self.class_extractor=ClassExtractor()
        self.function_extractor=FunctionExtractor()

    def analyze_code(self , source_code:str)->dict:
        tree=ast.parse(source_code)
        import_result=self.import_extractor.extract(tree)
        class_result=self.class_extractor.extract(tree)
        function_result=self.function_extractor.extract(tree)
        return{
            "import" : import_result,
             "class" : class_result,
             "function":function_result
             
        }