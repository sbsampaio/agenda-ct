from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class TokenSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    # Token settings
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    # Database settings
    db_hostname: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+mysqldb://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_name}"
