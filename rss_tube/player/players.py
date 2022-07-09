from typing import Optional

from .mpv import MpvPlayerInstance
from .vlc import VlcPlayerInstance
from .generic import GenericPlayerInstance
from .base import BasePlayer


_player_instances = {
    "mpv": MpvPlayerInstance,
    "vlc": VlcPlayerInstance,
    "generic": GenericPlayerInstance,
}


def get_instance(player: str) -> Optional[BasePlayer]:
    return _player_instances.get(player)
