from pydantic_settings import SettingsConfigDict,BaseSettings


class Settings(BaseSettings):
    PG_CONNECTION: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config : SettingsConfigDict = SettingsConfigDict(env_file='.env',extra="ignore")

Config = Settings()
