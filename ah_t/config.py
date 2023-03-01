from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    DB_TEST_SUFFIX: str = "_test"

    class Config:
        env_file = ".env"

    @property
    def db_prod_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def db_test_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/"
            f"{self.POSTGRES_DB}{self.DB_TEST_SUFFIX}"
        )


settings = Settings()
