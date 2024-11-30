#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_null_model.py -- Test environment for null models
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Tue 2021-06-01 19:06 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================

import pytest

from pathpy3.models.network import Network
from pathpy3.core.path import PathCollection
from pathpy3.models.null_model import NullModel
from pathpy3.models.higher_order_network import HigherOrderNetwork


def test_basic():
    """Test basic functions"""

    paths = PathCollection()
    paths.add("a", "c", "d", uid="a-c-d", count=10)
    paths.add("b", "c", "e", uid="b-c-e", count=10)

    null = NullModel()
    null.fit(paths, order=2)

    # null = NullModel.from_paths(paths, order=2)

    assert null.number_of_edges() == 4
    assert null.number_of_nodes() == 4

    for e in null.edges.uids:
        assert null.edges.counter[e] == 5.0


def test_possible_paths():
    """Test to generate all possible paths."""
    paths = PathCollection()
    paths.add("a", "a", "b", "b", "a")

    null = NullModel()
    assert len(null.possible_relations(paths, length=3)) == 16


def test_from_network():

    net = Network()
    net.add_edge("a", "c", count=10)
    net.add_edge("c", "d", count=10)
    net.add_edge("b", "c", count=10)
    net.add_edge("c", "e", count=10)

    null = NullModel.from_network(net, order=2)

    assert null.number_of_edges() == 4
    assert null.number_of_nodes() == 4

    for e in null.edges.uids:
        assert null.edges.counter[e] == 5.0


def test_degrees_of_reedom():
    """Tets degrees of freedom"""
    paths = PathCollection()
    paths.add("a", "c", "d", frequency=2)
    paths.add("b", "c", "e", frequency=2)

    null = NullModel.from_paths(paths, order=0)
    assert null.degrees_of_freedom() == 4

    null = NullModel.from_paths(paths, order=1)
    assert null.degrees_of_freedom() == 1

    null = NullModel.from_paths(paths, order=2)
    assert null.degrees_of_freedom() == 2

    null = NullModel.from_paths(paths, order=3)
    assert null.degrees_of_freedom() == 0


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
