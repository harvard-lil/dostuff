from channels import route
from main import consumers

channel_routing = [
    route("websocket.connect", consumers.ws_connect, path=r"^/rooms/(?P<room_name>[a-zA-Z0-9_]+)$"),
    route("websocket.disconnect", consumers.ws_disconnect),
]