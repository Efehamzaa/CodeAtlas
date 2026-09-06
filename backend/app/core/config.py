from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.6-flash"

    class Config:
        env_file = ".env"

settings = Settings()