from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # APP
    app_name: str
    app_env: str
    app_debug: bool

    # API
    api_host: str
    api_port: int

    # DB
    database_url: str

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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore",)


settings = Settings()
