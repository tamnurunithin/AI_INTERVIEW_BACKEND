from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ===============================
    # App Configuration
    # ===============================

    APP_NAME: str = "AI Interview Coach"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ===============================
    # Server Configuration
    # ===============================

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ===============================
    # Frontend Configuration
    # ===============================

    FRONTEND_URL: str = "http://localhost:5173"

    # ===============================
    # Gemini API Configuration
    # ===============================

    GEMINI_API_KEY: str

    # ===============================
    # Groq API Configuration
    # ===============================

    GROQ_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()