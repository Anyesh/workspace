from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEBUG = False
BASEDIR = Path.home() / ".workspace"
BASEDIR.mkdir(exist_ok=True)
ENVDIR = BASEDIR / ".env"
