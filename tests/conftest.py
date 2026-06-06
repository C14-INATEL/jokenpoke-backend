# tests/conftest.py
import sys
from unittest.mock import MagicMock

pytest_plugins = [
    "tests.fixtures.cards",
    "tests.fixtures.battles",
]

# para test_register_user.py
mock_settings = MagicMock()
mock_settings.jwt_secret_key = "test_secret"
mock_settings.jwt_algorithm = "HS256"
mock_settings.jwt_access_token_expire_minutes = 30

mock_config_module = MagicMock()
mock_config_module.settings = mock_settings

sys.modules["app.core.config"] = mock_config_module
