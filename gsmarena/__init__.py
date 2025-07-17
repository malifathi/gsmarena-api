"""
GSMArena API - Python version

GSMArena phone specification and finder. This is a Python port of the original Node.js library.
The API reads from GSMArena website and returns JSON data.
"""

from .catalog import catalog
from .deals import deals
from .glossary import glossary
from .search import search
from .top import top

__version__ = "1.0.0"
__author__ = "Python Port"

__all__ = ["catalog", "deals", "glossary", "search", "top"]