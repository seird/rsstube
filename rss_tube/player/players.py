from typing import Optional

from .mpv import MpvPlayerInstance
from .vlc import VlcPlayerInstance
from .base import BasePlayer


_player_instances = {
    "mpv": MpvPlayerInstance,
    "vlc": VlcPlayerInstance
}


def get_instance(player: str) -> Optional[BasePlayer]:
    return _player_instances.get(player)
