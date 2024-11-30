"""
An OpenSource python package to analyze and
visualize time series data on complex networks.
"""

__author__ = """Ingo Scholtes"""
__email__ = "scholtes@ifi.uzh.ch"
__version__ = "2.2.0"

from .classes import *
import pathpy2.path_extraction
import pathpy2.visualisation
import pathpy2.algorithms.centralities
import pathpy2.algorithms.components
import pathpy2.algorithms.shortest_paths
import pathpy2.algorithms.centralities
import pathpy2.algorithms.random_walk
import pathpy2.algorithms.temporal_walk
import pathpy2.algorithms.spectral
import pathpy2.algorithms.path_measures
import pathpy2.algorithms.infomap
import pathpy2.algorithms.modularity
import pathpy2.algorithms.random_graphs
from .algorithms import statistics

import pathpy2.utils

global ENABLE_MULTICORE_SUPPORT
ENABLE_MULTICORE_SUPPORT = False
