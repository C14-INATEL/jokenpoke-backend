from fastapi import APIRouter

from app.interfaces.api.routes import (
    auth_routes,
    card_routes,
    deck_routes,
    ranking_routes,
    user_routes,
)

router = APIRouter()

router.include_router(auth_routes.router)
# router.include_router(battle_routes.router)
router.include_router(card_routes.router)
router.include_router(deck_routes.router)
router.include_router(ranking_routes.router)
router.include_router(user_routes.router)
