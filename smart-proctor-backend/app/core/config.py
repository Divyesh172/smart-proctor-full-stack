import secrets
from typing import List, Union, Optional, Annotated
from pydantic import AnyHttpUrl, PostgresDsn, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    # ---------------------------------------------------------
    # PROJECT METADATA
    # ---------------------------------------------------------
    PROJECT_NAME: str = "VerifAI Enterprise"
    API_V1_STR: str = "/api/v1"

    # ---------------------------------------------------------
    # SECURITY (Required in Production)
    # ---------------------------------------------------------
    # If this is missing from .env, the app will CRASH immediately (Good!)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    # 7 Days Token Validity (Standard for student portals)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # ---------------------------------------------------------
    # CORS (Cross-Origin Resource Sharing)
    # ---------------------------------------------------------
    # Needs to handle a comma-separated string from .env
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # ---------------------------------------------------------
    # DATABASE (PostgreSQL)
    # ---------------------------------------------------------
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Auto-constructs the Postgres connection string.
        Handles special characters in passwords automatically.
        """
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # ---------------------------------------------------------
    # FEATURE FLAGS (Toggles)
    # ---------------------------------------------------------
    # Allows you to turn off signups during an exam period
    USERS_OPEN_REGISTRATION: bool = True

    # ---------------------------------------------------------
    # MICROSERVICES INTEGRATION
    # ---------------------------------------------------------
    GO_BOUNCER_URL: str = "http://localhost:8080"

    # ---------------------------------------------------------
    # AI & INTEGRITY CONFIG
    # ---------------------------------------------------------
    HONEYPOT_TRAP_WORD: str = "Cyberdyne"
    MAX_TYPING_DEVIATION_PERCENT: float = 40.0

    # ---------------------------------------------------------
    # PYDANTIC V2 CONFIG
    # ---------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore" # Ignore extra fields (like comments) in .env
    )

# Instantiate the global settings object
settings = Settings()