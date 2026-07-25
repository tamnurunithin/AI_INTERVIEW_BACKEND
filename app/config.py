from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ===============================
    # App Configuration
    # ===============================

    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    # ===============================
    # Server Configuration
    # ===============================

    HOST: str
    PORT: int

    # ===============================
    # Frontend Configuration
    # ===============================

    FRONTEND_URL: str

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