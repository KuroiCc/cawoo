from datetime import time

from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENING_TIME = time(8, 0)
    WORKING_HOURS = 8
    LATE_NIGHT_TIME = time(22, 0)
    NOTION_API_KEY: str

    class Config:
        env_file = 'cawoo/.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()

if __name__ == "__main__":
    print(settings.dict())
