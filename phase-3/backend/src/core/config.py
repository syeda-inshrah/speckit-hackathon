from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    DATABASE_URL: str

    # Authentication
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7

    # CORS
    FRONTEND_URL: str

    # LLM Provider Selection
    LLM_PROVIDER: str = "OPENROUTER"  # Options: OPENROUTER or GROQ

    # OpenRouter (OpenAI-compatible API)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"

    # Groq (OpenAI-compatible API)
    GROQ_API_KEY: str = ""
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # OpenAI Agents SDK
    AGENT_NAME: str = "TodoAssistant"
    AGENT_INSTRUCTIONS: str = "You are a helpful AI assistant for managing todo tasks."
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7

    # Validators to strip whitespace from all string fields
    @field_validator('*', mode='before')
    @classmethod
    def strip_whitespace(cls, v):
        """Strip leading/trailing whitespace from all string values"""
        if isinstance(v, str):
            return v.strip()
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
