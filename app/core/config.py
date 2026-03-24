from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # APP
    app_name: str
    app_env: str
    app_debug: bool

    # API
    api_host: str
    api_port: int

    # DB
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    # GAME
    initial_cards_per_user: int
    deck_size: int
    battle_rounds: int

    # RANKING
    ranking_win_points: int
    ranking_loss_points: int
    ranking_draw_points: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()