from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    API_V1_STR: str = "/api/v1"

    DB_HOST: str
    LOCAL_DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.LOCAL_DB_PORT}/{self.DB_DATABASE}"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
