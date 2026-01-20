from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    jwt_secret: str = "change-me"
    database_url: str = "sqlite:///lab.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",  # sin prefijo
        extra="ignore",
    )


settings = Settings()
