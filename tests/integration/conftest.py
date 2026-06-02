import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_mock_settings = sys.modules["app.core.config"].settings
_mock_settings.database_url = "sqlite:///./test_integration.db"
_mock_settings.initial_cards_per_user = 6
_mock_settings.deck_size = 3
_mock_settings.battle_rounds = 3
_mock_settings.ranking_win_points = 25
_mock_settings.ranking_loss_points = 15
_mock_settings.ranking_draw_points = 0

SQLALCHEMY_TEST_URL = "sqlite:///./test_integration.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import app.infrastructure.db.session as _session_module  # noqa: E402

_session_module.engine = engine
_session_module.SessionLocal = TestingSessionLocal

import app.infrastructure.db.models.card_model  # noqa: F401, E402
import app.infrastructure.db.models.deck_model  # noqa: F401, E402
import app.infrastructure.db.models.user_model  # noqa: F401, E402
from app.infrastructure.db.base import Base  # noqa: E402
from app.infrastructure.db.session import get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="function")
def db():
    """Cria todas as tabelas antes de cada teste e derruba ao final."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """TestClient com get_db substituído pela sessão de teste."""

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
