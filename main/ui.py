"""Public UI exports for other modules."""

from game import play
from menu import main_menu, rules

# Re-export the main UI entrypoints.
__all__ = ["play", "main_menu", "rules"]
