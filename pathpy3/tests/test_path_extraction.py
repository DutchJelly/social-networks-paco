#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_path_extraction.py -- Test path extraction in temporal networks and DAGs
# Author    : Ingo Scholtes <scholtes@uni-wuppertal.de>
# Time-stamp: <Tue 2021-06-01 12:52 ingo>
#
# Copyright (c) 2016-2021 Pathpy Developers
# =============================================================================

import pytest
import pathpy3 as pp

from pathpy3 import TemporalNetwork
from pathpy3.algorithms.path_extraction import PaCo


from collections import Counter


@pytest.fixture
def tempnet():
    tn = pp.TemporalNetwork()
    tn.add_edge("a", "b", timestamp=1)
    tn.add_edge("b", "c", timestamp=2)
    tn.add_edge("b", "d", timestamp=5)
    tn.add_edge("c", "d", timestamp=5)
    return tn


@pytest.fixture
def tempnet2():
    tn = pp.TemporalNetwork(directed=False)
    tn.add_edge("a", "b", timestamp=1)
    tn.add_edge("b", "c", timestamp=2)
    tn.add_edge("a", "c", timestamp=3)
    tn.add_edge("b", "a", timestamp=3)
    return tn


@pytest.fixture
def dag():
    dag = pp.DirectedAcyclicGraph()
    dag.add_edge("a", "b")
    dag.add_edge("b", "c")
    dag.add_edge("b", "d")
    dag.add_edge("c", "e")
    return dag


pathdata = [
    (1, Counter({("a-b-c"): 1, ("b-d"): 1, ("c-d"): 1})),
    (2, Counter({("a-b-c"): 1, ("b-d"): 1, ("c-d"): 1})),
    (3, Counter({("a-b-c-d"): 1, ("b-d"): 1})),
    (4, Counter({("a-b-c-d"): 1, ("a-b-d"): 1})),
]

dagdata = [
    (1, [("a_1", "b_2"), ("b_2", "c_3"), ("b_5", "d_6"), ("c_5", "d_6")]),
    (
        2,
        [
            ("a_1", "b_2"),
            ("a_1", "b_3"),
            ("b_2", "c_3"),
            ("b_2", "c_4"),
            ("b_5", "d_6"),
            ("b_5", "d_7"),
            ("c_5", "d_6"),
            ("c_5", "d_7"),
        ],
    ),
    (
        3,
        [
            ("a_1", "b_2"),
            ("a_1", "b_3"),
            ("b_2", "c_3"),
            ("b_2", "c_4"),
            ("b_5", "d_6"),
            ("b_5", "d_7"),
            ("c_5", "d_6"),
            ("c_5", "d_7"),
            ("a_1", "b_4"),
        ],
    ),
    (
        4,
        [
            ("a_1", "b_2"),
            ("a_1", "b_3"),
            ("b_2", "c_3"),
            ("b_2", "c_4"),
            ("b_5", "d_6"),
            ("b_5", "d_7"),
            ("c_5", "d_6"),
            ("c_5", "d_7"),
            ("a_1", "b_4"),
            ("a_1", "b_5"),
        ],
    ),
]


@pytest.mark.parametrize("delta,path_counts", pathdata)
def test_path_extraction_temporal_network(tempnet, delta, path_counts):
    paths = pp.algorithms.path_extraction.all_paths_from_temporal_network(
        tempnet, delta=delta
    )
    assert paths.counter == path_counts


def test_path_extraction_temporal_network_undirected(tempnet2):
    paths = pp.algorithms.path_extraction.all_paths_from_temporal_network(
        tempnet2, delta=1
    )
    assert paths.counter == Counter(
        {("a-b-c-a"): 1, ("b-a"): 1, ("a-b"): 1, ("a-c"): 1, ("c-b-a"): 1}
    )


def test_path_extraction_dag(dag):
    paths = pp.algorithms.path_extraction.all_paths_from_dag(dag)
    assert paths.counter == Counter({("a-b-c-e"): 1, ("a-b-d"): 1})


@pytest.mark.parametrize("delta,expected_edges", dagdata)
def test_temporal_net_to_dag(tempnet, delta, expected_edges):
    dag = pp.DirectedAcyclicGraph.from_temporal_network(tempnet, delta=delta)
    for e in expected_edges:
        assert e in dag.edges


def tn1():
    """Temporal test Network 1"""
    tn1 = TemporalNetwork(directed=True)
    tn1.add_edge("a", "b", timestamp=1)  # 0
    tn1.add_edge("a", "b", timestamp=2)  # 1
    tn1.add_edge("b", "a", timestamp=3)  # 2
    tn1.add_edge("b", "c", timestamp=3)  # 3
    tn1.add_edge("d", "c", timestamp=3)  # 4
    tn1.add_edge("d", "c", timestamp=4)  # 5
    tn1.add_edge("c", "d", timestamp=5)  # 6
    tn1.add_edge("c", "b", timestamp=6)  # 7
    tn1.add_edge("b", "c", timestamp=7)  # 8
    return tn1


def tn2():
    """Temporal test Network 2"""
    tn2 = TemporalNetwork(directed=True)
    tn2.add_edge("a", "b", timestamp=1)  # 0
    tn2.add_edge("a", "c", timestamp=2)  # 1
    tn2.add_edge("b", "c", timestamp=2)  # 2
    tn2.add_edge("c", "d", timestamp=3)  # 3
    tn2.add_edge("b", "d", timestamp=4)  # 4
    tn2.add_edge("d", "c", timestamp=4)  # 5
    tn2.add_edge("d", "c", timestamp=5)  # 6
    tn2.add_edge("d", "a", timestamp=5)  # 7
    tn2.add_edge("c", "b", timestamp=6)  # 8
    return tn2


def tn1_delta2():
    """Correct solution"""
    return Counter(
        {
            ("a-b"): 2,
            ("b-a"): 1,
            ("b-c"): 2,
            ("c-b"): 1,
            ("c-d"): 1,
            ("d-c"): 2,
            ("a-b-a"): 2,
            ("a-b-c"): 2,
            ("b-c-d"): 1,
            ("c-b-c"): 1,
            ("d-c-b"): 1,
            ("d-c-d"): 2,
            ("a-b-c-d"): 2,
            ("d-c-b-c"): 1,
        }
    )


def tn1_delta3():
    """Correct solution"""
    return Counter(
        {
            ("a-b"): 2,
            ("b-a"): 1,
            ("b-c"): 2,
            ("c-b"): 1,
            ("c-d"): 1,
            ("d-c"): 2,
            ("a-b-a"): 2,
            ("a-b-c"): 2,
            ("b-c-b"): 1,
            ("b-c-d"): 1,
            ("c-b-c"): 1,
            ("d-c-b"): 2,
            ("d-c-d"): 2,
            ("a-b-c-b"): 2,
            ("a-b-c-d"): 2,
            ("b-c-b-c"): 1,
            ("d-c-b-c"): 2,
            ("a-b-c-b-c"): 2,
        }
    )


def tn2_delta1():
    """Correct solution"""
    return Counter(
        {
            ("a-b"): 1,
            ("a-c"): 1,
            ("b-c"): 1,
            ("b-d"): 1,
            ("c-b"): 1,
            ("c-d"): 1,
            ("d-a"): 1,
            ("d-c"): 2,
            ("a-b-c"): 1,
            ("a-c-d"): 1,
            ("b-c-d"): 1,
            ("b-d-a"): 1,
            ("b-d-c"): 1,
            ("c-d-c"): 1,
            ("d-c-b"): 1,
            ("a-b-c-d"): 1,
            ("a-c-d-c"): 1,
            ("b-c-d-c"): 1,
            ("b-d-c-b"): 1,
            ("a-b-c-d-c"): 1,
        }
    )


def tn2_delta2():
    """Correct solution"""
    return Counter(
        {
            ("a-b"): 1,
            ("a-c"): 1,
            ("b-c"): 1,
            ("b-d"): 1,
            ("c-b"): 1,
            ("c-d"): 1,
            ("d-a"): 1,
            ("d-c"): 2,
            ("a-b-c"): 1,
            ("a-c-d"): 1,
            ("b-c-d"): 1,
            ("c-d-c"): 2,
            ("b-d-c"): 1,
            ("c-d-a"): 1,
            ("b-d-a"): 1,
            ("d-c-b"): 2,
            ("a-b-c-d"): 1,
            ("a-c-d-c"): 2,
            ("b-c-d-c"): 2,
            ("b-d-c-b"): 1,
            ("a-c-d-a"): 1,
            ("b-c-d-a"): 1,
            ("c-d-c-b"): 2,
            ("a-b-c-d-a"): 1,
            ("a-c-d-c-b"): 2,
            ("b-c-d-c-b"): 2,
            ("a-b-c-d-c"): 2,
            ("a-b-c-d-c-b"): 2,
        }
    )


paco_paths = [
    (tn1(), 2, tn1_delta2()),
    (tn1(), 3, tn1_delta3()),
    (tn2(), 1, tn2_delta1()),
    (tn2(), 2, tn2_delta2()),
]


@pytest.mark.parametrize("tn,delta,expected_paths", paco_paths)
def test_PaCo(tn, delta, expected_paths):
    """
    Test the PaCo algorithm
    """

    PaCo_paths = PaCo(tn, delta, skip_first=0, up_to_k=10)
    assert PaCo_paths.counter == expected_paths


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
