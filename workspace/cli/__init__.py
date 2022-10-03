from rich import pretty, traceback

from . import cli

pretty.install()
traceback.install(show_locals=False)

__all__ = ["cli"]
