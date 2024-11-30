"""Statistics module for pathpy"""

# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : __init__.py -- Initialize statistics methods for pathpy
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Sun 2021-05-02 03:13 ingo>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================
# flake8: noqa
# pylint: disable=unused-import

from pathpy3.statistics.degrees import (
    degree_sequence,
    degree_distribution,
    degree_assortativity,
    degree_central_moment,
    degree_raw_moment,
    degree_generating_function,
    mean_degree,
    mean_neighbor_degree,
    molloy_reed_fraction,
)

from pathpy3.statistics.clustering import (
    local_clustering_coefficient,
    avg_clustering_coefficient,
    closed_triads,
)

from pathpy3.statistics.modularity import (
    Q_modularity,
    Q_max_modularity,
    Q_assortativity_coefficient,
)

from pathpy3.statistics import likelihoods

from pathpy3.statistics.reciprocity import edge_reciprocity

# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
