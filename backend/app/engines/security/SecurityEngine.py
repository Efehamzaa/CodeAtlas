import ast
import re
import requests

class SecurityEngine:
    def __init__(self):
        self.dangerous_functions = ["eval", "exec", "system", "Popen"]
        self.secret_pattern = re.compile(r"(?i)(password|secret|api_key|token|auth_key)")

    def analyze_code(self, code):
        print(f"\n--- SECURITY ENGINE'E GELEN KOD --- \n{code}\n----------------------------------")
        try:
            tree = ast.parse(code)
            findings = []
            
            # 3 Kural motoru sırayla çalışıp sonuçları aynı havuza atıyor
            findings.extend(self._check_for_dangerous_calls(tree))
            findings.extend(self._check_for_hardcoded_secrets(tree))
            findings.extend(self._check_for_bola_vulnerabilities(tree))
            
            return findings
        except SyntaxError as e:
            print(f"SYNTAX HATASI YAKALANDI: {e}")
            return []
        except Exception as e:
            print(f"MOTOR İÇİNDE BEKLENMEYEN HATA: {e}")
            return []

    def _check_for_dangerous_calls(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in self.dangerous_functions:
                        findings.append({
                            "type": "Dangerous Function",
                            "severity": "High",
                            "description": f"Tehlikeli fonksiyon kullanımı: {func_name}",
                            "line_number": getattr(node, 'lineno', 0)
                        })
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                    if func_name in self.dangerous_functions:
                        findings.append({
                            "type": "Dangerous Module Call",
                            "severity": "High",
                            "description": f"Tehlikeli modül fonksiyon kullanımı: {func_name}",
                            "line_number": getattr(node, 'lineno', 0)
                        })
        return findings

    def _check_for_hardcoded_secrets(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        if hasattr(node, 'value') and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            assigned_value = node.value.value
                            if self.secret_pattern.search(var_name) and len(assigned_value) > 3:
                                findings.append({
                                    "type": "Hardcoded Secret",
                                    "severity": "Critical",
                                    "description": f"Koda gömülü kimlik bilgisi tespit edildi. Değişken: '{var_name}'",
                                    "line_number": getattr(node, 'lineno', 0)
                                })
        return findings

    def _check_for_bola_vulnerabilities(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                is_endpoint = False
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                        if decorator.func.attr in ["get", "post", "put", "delete", "patch"]:
                            is_endpoint = True
                            break
                
                if is_endpoint:
                    takes_id = False
                    has_auth_check = False
                    
                    for arg in node.args.args:
                        arg_name = arg.arg.lower()
                        if "id" in arg_name:
                            takes_id = True
                        if "user" in arg_name or "token" in arg_name or "auth" in arg_name:
                            has_auth_check = True
                            
                    if takes_id and not has_auth_check:
                        findings.append({
                            "type": "Potential BOLA/IDOR",
                            "severity": "High",
                            "description": f"Mantıksal Zafiyet (BOLA) Riski: '{node.name}' endpoint'i dışarıdan ID alıyor ancak yetki doğrulama parametresi içermiyor.",
                            "line_number": getattr(node, 'lineno', 0)
                        })
        return findings


    def analyze_dependencies(self, dependencies):
        findings = []
        osv_url="https://api.osv.dev/v1/query"

        for dep in dependencies:
            name=dep.get("name" , "").lower() if isinstance(dep,dict) else getattr(dep,"name","").lower()
            version=dep.get("version") if isinstance(dep,dict) else getattr(dep,"version",None)

            if not name or not version:
                continue

            payload={
                "version" : version,
                "package":{"name":name , "ecosystem":"PyPI"}
            }

            try:
                response=requests.post(osv_url,json=payload, timeout=5)

                if response.status_code==200:
                    data=response.json()

                    if "vulns" in data:
                        for vuln in data["vulns"]:

                            aliases=vuln.get("aliases",[])
                            cve_id=next((alias for alias in aliases if alias.startswith("CVE-")), vuln.get("id" , "Bilinmeyen ID"))

                            summary=vuln.get("summary" , "zafiyetin detaylı özeti bulunamadı.")

                            severity_level="Medium" #default severity level
                            if "severity" in vuln:
                                for sev in vuln["severity"]:
                                    if sev["type"]=="CVSS_V3":
                                        score=sev.get("score","")
                                        if "CRITICAL" in score or "HIGH" in score:
                                            severity_level="Critical" if "CRITICAL" in score else "High"

                            findings.append({
                                "type":f"Tedarik Zinciri Zafiyeti: ({cve_id})",
                                "severity":severity_level,
                                "description": f"Paket: {name} v{version} | Tehdit: {summary}",
                                "file_path": "requirements.txt",
                                "line_number":0
                            })

            except requests.exceptions.RequestException as e:
                print(f"OSV API Bağlantı Hatası ({name}): {e}")
        return findings
