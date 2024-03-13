"""
context module to enable running of tests in directory
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfsr import LFSR, LinSolve, IterSolve, MultiLFSR