import sys
import os
from pathlib import Path

IS_EXE = False


if getattr(sys, "frozen", False):
    IS_EXE = True
    PATH = Path(sys._MEIPASS)
else:
    PATH = Path(os.path.dirname(os.path.abspath(__file__)))
    print(PATH)
