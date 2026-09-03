import ast

class SecurityEngine:
    def __init__(self):
        self.dangerous_functions=["eval", "exec", "system", "Popen"]

    def analyze_code(self, code):
        print(f"\n--- SECURITY ENGINE'E GELEN KOD --- \n{code}\n----------------------------------") # BURAYI EKLE
        try:
            tree = ast.parse(code)
            return self._check_for_dangerous_calls(tree)
        except SyntaxError as e:
            print(f"SYNTAX HATASI YAKALANDI: {e}") # HATA VARSA GÖRELİM
            return []

    def _check_for_dangerous_calls(self, tree):
        findings=[]
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):
                    func_name=node.func.id
                    if func_name in self.dangerous_functions:
                        findings.append({
                            "type": "Dangerous function",
                            "severity": "High",
                            "description": f"Tehlikeli fonksiyon kullanimi:{func_name}",
                            "line_number": getattr(node, 'lineno', 0)
                        })

                elif isinstance(node.func, ast.Attribute):
                    func_name=node.func.attr
                    if func_name in self.dangerous_functions:
                        findings.append({
                            "type": "Dangerous Module Call",
                            "severity": "High",
                            "description": f"Tehlikeli modül  fonksiyon kullanımı:{func_name}",
                            "line_number": getattr(node, 'lineno', 0)

                            })
        print(f"\n--- MOTORUN İÇİNDE YAKALANANLAR --- \n{findings}\n-----------------------------------")
        return findings