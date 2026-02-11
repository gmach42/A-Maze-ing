__authors__ = "Gildas", "Bruno"
__version__ = "0.0.1"

from .solver import Border
from .maze_manager import MazeManager
from .parser import parsing, EnvVariables

__all__ = ['Border', 'MazeManager', 'parsing', 'EnvVariables']
