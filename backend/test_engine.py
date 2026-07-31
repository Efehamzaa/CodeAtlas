from app.engines.architecture.engine import ArchitectureEngine

# Motorumuzu çalıştıracak sahte bir kod metni
ornek_kod = """
import os
import sys
from datetime import datetime
from pydantic import BaseModel

class Test:
    pass
    
class MyTestClass:pass

def my_func():pass

async def my_async_func():pass
"""

# Yöneticimizi çağıralım
engine = ArchitectureEngine()

# Analizi başlatalım
sonuc = engine.analyze_code(ornek_kod)

# Çıkan sonucu ekranda görelim
print("Bulunan Importlar:", sonuc)