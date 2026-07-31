from abc import ABC , abstractmethod
import ast

class BaseExtractor(ABC):
    """ 
     Tüm mimari çıkarıcıların uymak zorunda olduğu temel arayüz
     """

    @abstractmethod
    def extract(self , node:ast.AST):
        pass
    