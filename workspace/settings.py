import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEBUG = False
BASEDIR = Path(__file__).resolve().parent.parent
ENVDIR = BASEDIR / ".env"
