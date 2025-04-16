from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    bin_id: str

    class Config:
        env_file = ".env"


settings = Settings()
