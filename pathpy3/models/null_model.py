""" Null Model class """

# !/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : null_models.py -- Null models for pathpy
# Author    : Jürgen Hackl <hackl@ifi.uzh.ch>
# Time-stamp: <Tue 2021-06-01 19:06 juergen>
#
# Copyright (c) 2016-2019 Pathpy Developers
# =============================================================================
from typing import Optional, Any
from collections import Counter
from singledispatchmethod import singledispatchmethod

from pathpy3 import logger, tqdm
from pathpy3.models.higher_order_network import HigherOrderNetwork
from pathpy3.core.path import PathCollection
from pathpy3.models.network import Network

# create logger
LOG = logger(__name__)


class NullModel(HigherOrderNetwork):
    """A null model for higher order networks."""

    def __init__(
        self, uid: Optional[str] = None, order: int = 2, **kwargs: Any
    ) -> None:
        """Initialize the null model"""

        # initialize the base class
        super().__init__(uid=uid, order=order, **kwargs)

    @singledispatchmethod
    def fit(self, data, order: Optional[int] = None, subpaths: bool = True) -> None:
        """Fit data to a HigherOrderNetwork"""
        raise NotImplementedError

    @fit.register(PathCollection)  # type: ignore
    def _(self, data: PathCollection, order: Optional[int] = None) -> None:

        # check order
        if order is not None:
            self._order = order

        # generate first order hon
        hon = HigherOrderNetwork.from_paths(data, order=1)

        # get node index and transition matrix
        idx = {node.relations[0]: i for i, node in enumerate(hon.nodes)}
        mat = hon.transition_matrix(count=True)

        # generate possible paths
        paths = self.possible_relations(data, self.order)

        subpaths: Counter = Counter()
        for path in tqdm(data, desc="calculate possible sub-paths"):
            for subpath in path.subpaths(
                min_length=self.order - 1,
                max_length=self.order - 1,
                include_self=True,
                paths=False,
            ):
                subpaths[subpath] += data.counter[path.uid]

        for path in paths:
            # get higher-oder nodes
            _v, _w = path[:-1], path[1:]
            if _v not in self.nodes:
                self.add_node(*_v, uid="-".join(_v), count=0)
            if _w not in self.nodes:
                self.add_node(*_w, uid="-".join(_w), count=0)
            node_v, node_w = self.nodes[_v], self.nodes[_w]

            frequency = subpaths[_v] * mat[idx[path[-2]], idx[path[-1]]]

            if (node_v, node_w) not in self.edges:
                self.add_edge(node_v, node_w, count=0)

            edge = self.edges[node_v, node_w]
            self.edges.counter[edge.uid] += frequency

    @fit.register(Network)  # type: ignore
    def _(
        self, data: Network, order: Optional[int] = None, subpaths: bool = True
    ) -> None:
        paths = PathCollection(directed=data.directed, multipaths=data.multiedges)
        for edge in data.edges:
            paths.add(*edge, count=data.edges.counter[edge.uid])

        self.fit(paths, order=order)

    def degrees_of_freedom(self, mode: str = "path") -> int:
        """Returns the degrees of freedom of the higher order network.

        Since probabilities must sum to one, the effective degree of freedom is
        one less than the number of nodes

        .. math::

           \\text{dof} = \\sum_{n \\in N} \\max(0,\\text{outdeg}(n)-1)

        """
        # initialize degree of freedom
        degrees_of_freedom: int = 0

        if self.order == 0:
            degrees_of_freedom = max(0, self.number_of_nodes() - 1)

        elif mode == "ngram":
            number_of_nodes = len(self.nodes.nodes)
            degrees_of_freedom = (number_of_nodes**self.order) * (number_of_nodes - 1)

        elif mode == "path":

            # iterate over all nodes and count outdegree
            for outdegree in self.outdegrees().values():
                degrees_of_freedom += max(0, int(outdegree) - 1)

        # return degree of freedom
        return degrees_of_freedom

    @classmethod
    def from_paths(cls, paths: PathCollection, **kwargs: Any):
        """Create higher oder network from paths."""

        order: int = kwargs.get("order", 2)

        null = cls(order=order)
        null.fit(paths)

        return null

    @classmethod
    def from_network(cls, network: Network, **kwargs: Any):
        """Create higher oder network from networks."""

        order: int = kwargs.get("order", 2)

        null = cls(order=order)
        null.fit(network)

        return null


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 79
# End:
