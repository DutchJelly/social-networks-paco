# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_edge.py -- Test environment for the Edge class
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Fri 2021-06-04 10:40 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================

import pytest

from pathpy3 import Edge, Node
from pathpy3.core.edge import EdgeCollection


@pytest.fixture(params=[True, False])
def nodes(request):
    """Generate node objects."""
    v = Node("v")
    w = Node("w")
    return v, w


def test_hash():
    """Test the hash of an edge"""
    a = Node("a")
    b = Node("b")
    c = Node("c")

    e1 = Edge(a, b)
    e2 = Edge(b, c)
    e3 = Edge(a, b)

    # different objects
    assert e1.__hash__() != e2.__hash__()

    # different objects but same uid
    assert e1.__hash__() != e3.__hash__()


def test_uid():
    """Test the uid assignment."""

    a = Node("a")
    b = Node("b")

    e = Edge(a, b, uid="e")

    assert isinstance(e, Edge)
    assert isinstance(e.uid, str)
    assert e.uid == "e"

    a = Node("a")
    b = Node("b")

    e = Edge(a, b, "e")

    assert isinstance(e, Edge)
    assert isinstance(e.uid, str)
    assert e.uid == "e"

    a = Node()
    b = Node()

    e = Edge(a, b)

    assert isinstance(e, Edge)
    assert isinstance(e.uid, str)
    assert e.uid == hex(id(e))


def test_setitem(nodes):
    """Test the assignment of attributes."""

    v, w = nodes

    vw = Edge(v, w)
    vw["capacity"] = 5.5

    assert vw["capacity"] == 5.5


def test_getitem(nodes):
    """Test the extraction of attributes."""

    v, w = nodes

    vw = Edge(v, w, length=10)

    assert vw["length"] == 10
    assert vw["attribute not in dict"] is None


def test_repr(nodes):
    """Test printing the node."""

    v, w = nodes

    vw = Edge(v, w, "vw")

    assert vw.__repr__() == "Edge vw"


def test_update(nodes):
    """Test update node attributes."""
    v, w = nodes
    vw = Edge(v, w, length=5)

    assert vw["length"] == 5

    vw.update(length=10, capacity=6)

    assert vw["length"] == 10
    assert vw["capacity"] == 6


def test_copy(nodes):
    """Test to make a copy of a node."""

    v, w = nodes
    vw = Edge(v, w, "vw")
    ab = vw.copy()

    assert ab.uid == vw.uid == "vw"

    # different objects
    assert ab != vw


def test_weight(nodes):
    """Test the weight assigment."""

    v, w = nodes

    vw = Edge(v, w)

    assert vw.weight() == 1.0

    vw["weight"] = 4

    assert vw.weight() == 4.0
    assert vw.weight(weight=None) == 1.0
    assert vw.weight(weight=False) == 1.0

    vw["length"] = 5
    assert vw.weight("length") == 5.0


def test_self_loop():
    """Test self loop as an edge."""
    v = Node()

    vv = Edge(v, v)
    assert len(vv.nodes) == 1


def test_multiple_nodes():
    """Test edge creation with mutliple nodes"""
    e = Edge("a", "b", 1)
    assert "a" and "b" in e.nodes
    assert e.uid == 1


def test_errors():
    """Test some errors user can make"""
    # This is now possible and recomende
    # with pytest.raises(Exception):
    #     e = Edge('a', 'b')
    pass


def test_EdgeCollection():
    """Test the EdgeCollection"""
    edges = EdgeCollection(color="green")

    assert len(edges) == 0

    a = Node("a")
    b = Node("b")
    ab = Edge(a, b, uid="a-b")

    edges.add(ab)

    # with pytest.raises(Exception):
    #     edges.add(ab)

    assert len(edges) == 1
    assert edges["a-b"] == ab
    assert edges[ab] == ab
    assert "a-b" in edges
    assert ab in edges
    assert "a-b" in edges.uids
    assert "a-b" in edges.keys()
    assert ab in edges.values()
    assert ("a-b", ab) in edges.items()

    assert len(edges.nodes) == 2
    assert edges.nodes["a"] == a
    assert edges.nodes[a.uid] == a
    assert "a" in edges.nodes
    assert a in edges.nodes.values()
    # assert 'a' in edges.nodes.uids
    assert "a" in edges.nodes.keys()
    assert a in edges.nodes.values()
    # assert ('a', a) in edges.nodes.items()

    # with pytest.raises(Exception):
    #     edges.add((a))

    c = Node("c")
    d = Node("d")

    edges.add(c, d, uid="c-d")

    assert len(edges) == 2
    assert edges["c-d"].v.uid == "c"

    edges.add("e", "f", uid="e-f")

    assert len(edges) == 3
    assert "e" and "f" in edges.nodes

    for _e in [("f", "g"), ("g", "h")]:
        edges.add(_e)

    assert len(edges) == 5

    # edges.add('e', nodes=False)

    #     assert len(edges) == 6
    #     assert 'e' in edges
    #     assert isinstance(edges['e'].v, Node)
    #     assert isinstance(edges['e'].w, Node)
    #     assert len(edges.nodes) == 10

    #     _v = edges['e'].v.uid
    #     _w = edges['e'].w.uid

    #     edges.remove('e')
    #     assert len(edges) == 5
    #     assert 'e' not in edges

    #     # edges._remove_node(_v)
    #     # edges._remove_node(_w)
    #     # assert len(edges.nodes) == 8

    edges.remove("g", "h")
    edges.remove(("f", "g"))

    assert len(edges) == 3

    edges.remove(ab)
    edges.remove("c-d")
    assert len(edges) == 1
    # assert len(edges.nodes) == 10

    edges = EdgeCollection()
    edges.add("a", "b")

    # with pytest.raises(Exception):
    #     edges.add('a', 'b')

    edges = EdgeCollection()
    edges.add("a", "b", uid="e1")
    edges.add("b", "c", uid="e2")
    edges.add("c", "d", uid="e3")
    edges.add("d", "e", uid="e4")

    assert len(edges) == 4

    edges.remove("e1")
    assert len(edges) == 3

    for _e in ["e2", "e3"]:
        edges.remove(_e)

    assert len(edges) == 1


def test_EdgeCollection_multiedges():
    """Test the EdgeCollection"""
    edges = EdgeCollection(multiedges=True)

    assert len(edges) == 0

    a = Node("a")
    b = Node("b")
    ab = Edge(a, b, uid="a-b")

    edges.add(ab)
    edges.add(a, b, uid="new")

    assert len(edges) == 2
    assert edges["a-b"] == ab
    assert len(edges["a", "b"]) == 2
    assert len(edges[a, b]) == 2
    # assert edges[a, 'b'][-1].uid == 'new'
    # assert edges[a, 'b']['new'].uid == 'new'


def test_multiedges():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")

    e1 = Edge(a, b, uid="a-b")
    e2 = Edge(a, b, uid="e2")
    e3 = Edge(c, d, uid="a-b")

    edges = EdgeCollection()
    edges.add(e1)

    # with pytest.raises(Exception):
    #     edges.add(e2)
    # with pytest.raises(Exception):
    #     edges.add(e3)

    edges = EdgeCollection(multiedges=True)
    edges.add(e1)
    edges.add(e2)

    # with pytest.raises(Exception):
    #     edges.add(e3)


def test_EdgeCollection_undirected():
    """Test undirected edge collection"""

    edges = EdgeCollection(directed=False)
    edges.add("a", "b")
    edges.add("b", "a")
    assert len(edges) == 1

    assert edges["a", "b"].directed == False
    assert ("a", "b") in edges
    assert ("b", "a") in edges


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
