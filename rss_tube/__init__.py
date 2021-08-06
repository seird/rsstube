from .__version__ import __author_email__, __version__, __url__, __title__, __versionurl__, \
    __description__
from .gui import start_gui, MainWindow

import os
from pathlib import Path

def get_abs_path(s) -> str:
    return os.path.join(Path(__file__).parent, s)
