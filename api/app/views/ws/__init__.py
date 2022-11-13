from app.views.ws.quiz import multiplayer_session, single_player_session
from app.views.ws.user import notifications
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ws = FastAPI()

ws.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ws.add_api_websocket_route("/singleplayer", single_player_session, "single_player")

ws.add_api_websocket_route("/multiplayer", multiplayer_session, "multi_player")

ws.add_api_websocket_route("/notifications", notifications, "notifications")
