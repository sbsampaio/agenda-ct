from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_hostname: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str
