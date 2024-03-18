"""
context module to enable running tests in directory tests/
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lfsr_library import Analyser, LFSR, MultiLFSR, Validator, ItValidator