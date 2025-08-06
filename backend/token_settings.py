from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class TokenSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    # Token settings
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(alias="ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database settings
    db_hostname: str = Field(alias="DB_HOSTNAME")
    db_port: int = Field(alias="DB_PORT")
    db_name: str = Field(alias="DB_NAME")
    db_username: str = Field(alias="DB_USERNAME")
    db_password: str = Field(alias="DB_PASSWORD")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+mysqldb://{self.db_username}:{self.db_password}@{self.db_hostname}:{self.db_port}/{self.db_name}"
