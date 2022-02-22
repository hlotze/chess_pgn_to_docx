# pylint: disable=wrong-import-position
# pylint: disable=unused-import
"""Helper for imports"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import chessboard
import eco
import pgn
