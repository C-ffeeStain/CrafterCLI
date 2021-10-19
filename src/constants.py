import sys
import os
from pathlib import Path
from platformdirs import user_data_dir


IS_EXE = False
DATA_DIR = Path(user_data_dir("Crafter", "C_ffeeStain"))


if getattr(sys, "frozen", False):
    IS_EXE = True
    PATH = Path(sys._MEIPASS)
else:
    PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent
    print(PATH)
