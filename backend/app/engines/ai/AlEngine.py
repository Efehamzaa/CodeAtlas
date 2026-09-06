import json
from google import genai
from google.genai import types
from app.core.config import settings
from app.engines.ai.schemas import SecurityAnalysis
from app.engines.ai.prompts import SECURITY_ANALYSIS_PROMPT

class AIEngine:
    def __init__(self):
        self.client=genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate_remediation_report(self , security_findings:list):
        if not security_findings:
            return None

        findings_json = json.dumps(security_findings, indent=2, ensure_ascii=False)
        formatted_prompt = SECURITY_ANALYSIS_PROMPT.format(findings_data=findings_json)


        try:
            print("--- AI Analizi Başladı (Structured Output) ---")
            

        
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=formatted_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SecurityAnalysis,
                    temperature=0.2 
                ),
            )

            print("--- AI Analizi Tamamlandı ---")
            return json.loads(response.text)

        except Exception as e:
            print(f"AI Analizi sırasında hata oluştu: {str(e)}")
            return None