# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_path.py -- Test environment for the Path class
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Thu 2021-06-10 14:38 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================

import pytest

from pathpy3 import Edge, Node, Path
from pathpy3.core.path import PathCollection


def test_path():
    """Test basic path"""
    a = Node("a")
    b = Node("b")
    c = Node("c")
    e = Edge(a, b)
    f = Edge(b, c)

    p = Path(e, f)


def test_PathCollection_add_path():
    """Add path to the path collection."""
    a = Node("a")
    b = Node("b")
    c = Node("c")
    e = Edge(a, b, uid="e")
    f = Edge(b, c, uid="f")

    p1 = Path(e, f, uid="p1")
    p2 = Path(e, uid="p2")
    p3 = Path(a, uid="p3")

    paths = PathCollection()
    paths.add(p1)

    paths.add(p1)
    assert paths.counter["p1"] == 2

    assert len(paths.nodes) == 2
    # assert len(paths.edges) == 2
    assert len(paths) == 1
    assert p1 in paths

    paths = PathCollection()
    paths.add(p1, p2)

    assert p1 in paths
    assert p2 in paths


def test_PathCollection_add_edges():
    """Add edge path to the path collection."""
    a = Node("a")
    b = Node("b")
    c = Node("c")
    e = Edge(a, b, uid="e")
    f = Edge(b, c, uid="f")

    paths = PathCollection()
    paths.add(e, f, uid="p1")

    assert len(paths.nodes) == 2
    #     assert len(paths.edges) == 2
    assert len(paths) == 1
    assert "p1" in paths

    paths.add(e, f, uid="p1")
    assert paths.counter["p1"] == 2

    paths.add(e, f)
    assert paths.counter["p1"] == 3

    with pytest.raises(Exception):
        paths.add(e, f, uid="p2")

    assert paths.counter["p1"] == 3


def test_PathCollection_add_nodes():
    """Add node path to the path collection."""
    a = Node("a")
    b = Node("b")
    c = Node("c")

    paths = PathCollection()
    paths.add(a, b, c, uid="p1")

    assert len(paths.nodes) == 3
    # assert len(paths.edges) == 2
    assert len(paths) == 1
    assert "p1" in paths

    paths.add(a, b, c, uid="p1")
    assert paths.counter["p1"] == 2

    paths.add(a, b, c)
    assert paths.counter["p1"] == 3


def test_PathCollection_add_str():
    """Add string path to the path collection."""

    paths = PathCollection()
    paths.add("a", "b", "c", uid="p1")

    assert len(paths.nodes) == 3
    # assert len(paths.edges) == 2
    assert len(paths) == 1
    assert "p1" in paths

    paths.add("a", "b", "c", uid="p1")
    assert paths.counter["p1"] == 2

    paths.add("a", "b", "c")
    assert paths.counter["p1"] == 3

    # paths = PathCollection()
    # paths.add('e1', 'e2', uid='p1', nodes=False)

    # assert len(paths) == 1
    # assert len(paths.edges) == 2
    # assert len(paths.nodes) == 3
    # assert 'p1' in paths
    # assert 'e1' and 'e2' in paths.edges


def test_PathCollection_add_tuple():
    """Add path tuple to the path collection."""

    paths = PathCollection()
    paths.add(("a", "b"), ("a", "b", "c"))

    assert len(paths.nodes) == 3
    # assert len(paths.edges) == 2
    assert len(paths) == 2

    paths.add("a", "b", "c")
    assert paths.counter[paths["a", "b", "c"].uid] == 2


def test_PathCollection_remove_path():
    """Remove path from the path collection."""
    a = Node("a")
    b = Node("b")
    c = Node("c")
    e = Edge(a, b, uid="e")
    f = Edge(b, c, uid="f")

    p1 = Path(e, f, uid="p1")
    p2 = Path(e, uid="p2")
    p3 = Path(a, uid="p3")

    paths = PathCollection()
    paths.add(p1)

    paths.remove(p1)

    assert len(paths.nodes) == 0
    # assert len(paths.edges) == 2
    assert len(paths) == 0
    assert p1 not in paths


def test_PathCollection_remove_edges():
    """Remove edge path from the path collection."""
    a = Node("a")
    b = Node("b")
    c = Node("c")
    e = Edge(a, b, uid="e")
    f = Edge(b, c, uid="f")

    paths = PathCollection()
    paths.add(e, f, uid="p1")

    paths.remove(e, f)
    assert len(paths) == 0
    assert "p1" not in paths

    paths.add(e, f, uid="p1")
    paths.remove("p1")
    assert len(paths) == 0

    paths.add(e, f, uid="p1")
    paths.remove(e, f)
    assert len(paths) == 0

    paths.add(e, f, uid="p1")
    paths.remove("e", "f")
    assert len(paths) == 0


def test_PathCollection():
    """Test the paths object"""
    a = Node("a")
    b = Node("b")
    c = Node("c")
    e = Edge(a, b, uid="e")
    f = Edge(b, c, uid="f")

    p1 = Path(e, f, uid="p1")
    p2 = Path(e, uid="p2")
    p3 = Path(a, uid="p3")

    paths = PathCollection()
    paths.add(p1)
    paths.add(p2)
    paths.add(p3)

    paths.add(p1)
    assert paths.counter["p1"] == 2

    assert len(paths.nodes) == 3
    # assert len(paths.edges) == 2
    assert len(paths) == 3
    assert p1 in paths
    assert p2 in paths
    assert p3 in paths

    assert "p1" in paths
    assert "p2" in paths
    assert "p3" in paths

    assert (e, f) in paths
    assert ("e", "f") in paths
    assert (e,) in paths
    assert ("e",) in paths
    assert (a,) in paths
    assert ("a",) in paths

    a = Node("a")
    b = Node("b")
    c = Node("c")

    p1 = Path(a, b, c, uid="p1")
    p2 = Path(a, b, uid="p2")
    p3 = Path(a, uid="p3")

    paths = PathCollection()
    paths.add(p1)
    paths.add(p2)
    paths.add(p3)

    assert (a, b, c) in paths
    assert ("a", "b", "c") in paths
    assert (a, b) in paths
    assert ("a", "b") in paths

    assert (a,) in paths
    assert ("a",) in paths
    # assert [a] in paths
    # assert ['a'] in paths

    assert paths["a", "b", "c"] == p1
    assert paths["a", "b"] == p2

    with pytest.raises(Exception):
        p = paths["x", "y"]

    p4 = Path(b, c, uid="p4")
    # with pytest.raises(Exception):
    paths.add(p4)
    assert paths.counter["p4"] == 1

    paths = PathCollection()
    paths.add(a, b)

    # with pytest.raises(Exception):
    paths.add(a, b)
    assert paths.counter[paths["a", "b"].uid] == 2

    paths = PathCollection()
    paths.add("a", "b", "c", uid="a-b-c")

    assert len(paths) == 1
    assert "a-b-c" in paths
    assert "a" and "b" and "c" in paths.nodes

    paths = PathCollection()
    paths.add(p1, p2)

    assert len(paths) == 2

    paths = PathCollection()
    paths.add(("a", "b", "c"), ("a", "b"))

    assert len(paths.nodes) == 3
    # assert len(paths.edges) == 2
    assert len(paths) == 2

    paths = PathCollection()
    paths.add(e, f, uid="p1")

    assert len(paths) == 1
    # assert len(paths.edges) == 2
    assert len(paths.nodes) == 2

    assert (e, f) in paths
    # assert ('a', 'b', 'c') in paths

    # with pytest.raises(Exception):
    paths.add(f, e, uid="p2")

    #     paths = PathCollection()
    #     paths.add('e1', uid='p1', nodes=False)

    #     assert len(paths) == 1
    #     assert len(paths.edges) == 1
    #     assert len(paths.nodes) == 2
    #     assert 'p1' in paths
    #     assert 'e1' in paths.edges

    #     paths = PathCollection()
    #     paths.add('e1', 'e2', uid='p1', nodes=False)

    #     assert len(paths) == 1
    #     assert len(paths.edges) == 2
    #     assert len(paths.nodes) == 3
    #     assert 'p1' in paths
    #     assert 'e1' and 'e2' in paths.edges

    #     assert paths.edges['e1'].w == paths.edges['e2'].v

    #     paths = PathCollection()
    #     paths.add(('e1', 'e2'), ('e3', 'e4'), nodes=False)

    #     assert len(paths.nodes) == 6
    #     assert len(paths.edges) == 4
    #     assert len(paths) == 2

    paths = PathCollection()
    paths.add(p1, p2, p3)

    assert len(paths.nodes) == 3
    assert len(paths) == 3

    paths.remove(p3)
    assert len(paths.nodes) == 3
    # assert len(paths.edges) == 2
    assert len(paths) == 2
    assert p3 not in paths

    paths.remove("p1")
    assert len(paths.nodes) == 2
    # assert len(paths.edges) == 2
    assert len(paths) == 1
    assert p1 not in paths

    paths = PathCollection()
    paths.add(("a", "b", "c"), ("a", "b"))

    assert len(paths) == 2

    paths.remove("a", "b")

    assert len(paths) == 1

    paths = PathCollection()
    paths.add(("a", "b"), ("b", "c"), ("c", "d"))
    paths.remove(("a", "b"), ("b", "c"))

    assert len(paths) == 1
    assert ("a", "b") not in paths
    assert ("b", "c") not in paths
    assert ("c", "d") in paths

    #     paths = PathCollection()
    #     paths.add(('e1', 'e2'), ('e2', 'e3'), ('e3', 'e4'), nodes=False)

    #     assert len(paths) == 3
    #     assert len(paths.edges) == 4

    #     paths.remove('e1', 'e2')
    #     assert len(paths) == 2

    #     paths.remove(('e2', 'e3'), ('e3', 'e4'))
    #     assert len(paths) == 0

    paths = PathCollection()
    paths.add("a", "b", uid="p1")
    paths.add("b", "c", uid="p2")
    paths.add("c", "d", uid="p3")
    paths.add("d", "e", uid="p4")

    assert len(paths) == 4

    paths.remove("p1")

    assert len(paths) == 3

    paths.remove(("p2", "p3"))

    # assert len(paths) == 1


def test_PathCollection_counter():
    """Test the counter of the path collection"""
    paths = PathCollection()
    paths.add("a", "b", count=5)
    paths.add("a", "b", count=7)
    assert paths.counter[paths["a", "b"].uid] == 12

    p1 = Path("a", "x", "c", uid="a-x-c")
    p2 = Path("b", "x", "d", uid="b-x-d")
    pc = PathCollection(multipaths=True)
    pc.add(p1)
    pc.add(p2)
    pc.add(p2)

    assert "a-x-c" and "b-x-d" in pc.counter

    p3 = Path("b", "x", "d", uid="b-x-d-2")
    pc.add(p3)

    assert "a-x-c" and "b-x-d" and "b-x-d-2" in pc.counter


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
