"""Pathpy"""

# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : __init__.py -- pathpy init file
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Fri 2021-05-28 13:04 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================
# flake8: noqa
# pylint: disable=unused-import

from .__about__ import (
    __title__,
    __version__,
    __author__,
    __email__,
    __copyright__,
    __license__,
    __maintainer__,
    __status__,
)

__version__ = "3.1.1"

# import os
import sys

# import utils
from pathpy3.utils.config import config  # noqa: F401
from pathpy3.utils.logger import logger  # noqa: F401
from pathpy3.utils.progress import tqdm  # noqa: F401
from pathpy3.utils.errors import FileFormatError, NetworkError, MissingModuleError


# import symbols into root namespace
from pathpy3.core.api import (
    Node,
    Edge,
    Path,
    HyperEdge,
    NodeCollection,
    EdgeCollection,
    PathCollection,
    HyperEdgeCollection,
)

# import models
from pathpy3.models.api import (
    Network,
    TemporalNetwork,
    DirectedAcyclicGraph,
    HigherOrderNetwork,
    HigherOrderNode,
    HigherOrderEdge,
    NullModel,
    MultiOrderModel,
    MOGen,
)

from pathpy3.visualisations.api import plot, layout

# import submodules
from pathpy3 import io
from pathpy3 import converters
from pathpy3 import algorithms
from pathpy3 import statistics
from pathpy3 import processes
from pathpy3 import generators


# add functions to Network class

# load external functions to the network
Network.adjacency_matrix = algorithms.adjacency_matrix  # type: ignore
Network.transition_matrix = algorithms.transition_matrix  # type: ignore
Network.distance_matrix = algorithms.distance_matrix  # type: ignore
Network.diameter = algorithms.diameter  # type: ignore
Network.avg_path_length = algorithms.avg_path_length

Network.betweenness_centrality = algorithms.betweenness_centrality  # type: ignore
Network.closeness_centrality = algorithms.closeness_centrality  # type: ignore

Network.find_connected_components = algorithms.find_connected_components  # type: ignore
Network.largest_connected_component = algorithms.largest_connected_component  # type: ignore
Network.largest_component_size = algorithms.largest_component_size  # type: ignore
Network.is_connected = algorithms.is_connected

Network.mean_degree = statistics.mean_degree
Network.mean_neighbor_degree = statistics.mean_neighbor_degree
Network.degree_sequence = statistics.degree_sequence
Network.degree_assortativity = statistics.degree_assortativity
Network.degree_central_moment = statistics.degree_central_moment
Network.degree_distribution = statistics.degree_distribution
Network.degree_generating_function = statistics.degree_generating_function
Network.degree_raw_moment = statistics.degree_raw_moment
Network.molloy_reed_fraction = statistics.molloy_reed_fraction

Network.avg_clustering_coefficient = statistics.avg_clustering_coefficient
Network.local_clustering_coefficient = statistics.local_clustering_coefficient

Network.plot = plot


# create logger for the the init file
LOG = logger(__name__)

# check in which environment pathpy is running
try:
    from IPython import get_ipython  # noqa: F401
except ModuleNotFoundError:
    config["environment"]["IDE"] = "console"
    config["environment"]["interactive"] = False
else:
    try:
        if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
            ImportError("console")
    except AttributeError:
        config["environment"]["IDE"] = "console"
        config["environment"]["interactive"] = False
    else:
        config["environment"]["interactive"] = True

    # NOTE: Currently this is not working
    # https://github.com/tqdm/tqdm/issues/747
    # https://github.com/microsoft/vscode-python/issues/3429
    # if 'VSCODE_PID' in os.environ:  # pragma: no cover
    #     config['environment']['IDE'] = 'vs code'
    #     LOG.debug('pathpy runs in vs code')
    # else:
    #     config['environment']['IDE'] = 'jupyter notebook'
    #     LOG.debug('pathpy runs in jupyter notebook')

LOG.debug("pathpy version %s", __version__)
LOG.debug("platform is %s", sys.platform)
LOG.debug("pathpy runs in a %s environment", config["environment"]["IDE"])

if config["environment"]["IDE"] == "vs code":
    _html = """
    <script charset="utf-8">
    // Load via requireJS if available (jupyter notebook environment)
    try {
    require.config({
    paths: {
    d3: "https://d3js.org/d3.v5.min.js".replace(".js", "")
    }
    });
    console.log("OKAY: requireJS was detected");
    }
    catch(err){
    console.log(err);
    console.log("ERROR: NO requireJS was detected");
    };
    require(['d3'], function(d3){
    console.log("OKAY: d3js was detected");
    });
    </script>
    """

    try:
        from IPython.display import display, HTML

        display(HTML(_html))
    except ImportError:
        pass
# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
