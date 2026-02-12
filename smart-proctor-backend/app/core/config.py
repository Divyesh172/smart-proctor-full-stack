import secrets
from typing import List, Union, Optional, Annotated
from pydantic import AnyHttpUrl, PostgresDsn, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    # --- Project Metadata ---
    PROJECT_NAME: str = "VerifAI"
    API_V1_STR: str = "/api/v1"

    # --- Security ---
    # In production, this MUST be loaded from .env.
    # If missing, Pydantic will raise an error (unless a default is provided).
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 7 days = 1 week token validity
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # --- CORS (Cross-Origin Resource Sharing) ---
    # This allows your Next.js frontend (Vercel) to talk to this Python backend.
    # It parses a comma-separated string from .env into a Python list.
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # --- Database (PostgreSQL) ---
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Auto-constructs the Postgres connection string from components.
        This is the 'Java-like' safety feature: we build the URL programmatically
        instead of trusting a raw string from the environment.
        """
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # --- Polyglot Service Integration ---
    # Where does the Python 'Brain' find the Go 'Bouncer'?
    GO_BOUNCER_URL: str = "http://localhost:8080"

    # --- AI & Anti-Cheating Config ---
    HONEYPOT_TRAP_WORD: str = "Cyberdyne"
    MAX_TYPING_DEVIATION_PERCENT: float = 40.0

    # --- Pydantic Config ---
    # Reads from .env file automatically.
    # 'case_sensitive' ensures OS compatibility.
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore" # Ignore extra fields in .env (like comments)
    )

# Instantiate the settings object to be imported elsewhere
settings = Settings()