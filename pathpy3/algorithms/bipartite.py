from pathpy3.models.hypergraph import HyperGraph
from pathpy3.models.network import Network
from pathpy3.models.temporal_network import TemporalNetwork

from itertools import combinations


def check_multi_partite(network, k=2, partition="partition"):
    """Checks whether a network fulfils the definition of a k-partite network, where the default value of k=2."""
    partitions = set()
    for e in network.edges:
        partitions.add(e.v[partition])
        partitions.add(e.w[partition])
        if e.v[partition] == e.w[partition]:
            return False
    return len(partitions) == k


def one_mode_projection(
    bipartite_net, partition="partition", projection=0, type="dyadic", temporal=False
):
    """Performs a one-mode or hypergraph projection of a bipartite network. It is assumed
    that nodes have an attribute partition that assumes values 0 and 1."""

    if projection == 0:
        other_partition = 1
    else:
        other_partition = 0
    if type == "dyadic":
        nodes = [v for v in bipartite_net.nodes if v[partition] == other_partition]
        # connect pairs of nodes in projected partition that have a common neighbour in other partition
        if temporal == False:
            n = Network(directed=False, multiedges=True)
        else:
            n = TemporalNetwork(directed=False, multiedges=True)
        for v in bipartite_net.nodes:
            if v[partition] == projection:
                n.add_node(v.uid, **v.attributes)
        for v in nodes:
            # connect pairs of nodes in projection partition that have common neighbour in other partition
            neighbors = set([x.uid for x in bipartite_net.predecessors[v.uid]])
            for i, j in combinations(neighbors, 2):
                n.add_edge(
                    i,
                    j,
                    uid="{0}-{1}[{2}]".format(i, j, v.uid),
                    node=v.uid,
                    **v.attributes
                )
    elif type == "hypergraph" or type == "polyadic":
        # collect nodes in other partition
        nodes = [v for v in bipartite_net.nodes if v[partition] == other_partition]
        n = HyperGraph()
        for v in nodes:
            # connect sets of nodes in projection partition that have common neighbour in other partition
            neighbors = [x.uid for x in bipartite_net.predecessors[v.uid]]
            n.add_edge(*neighbors, node=v.uid, **v.attributes)
    return n
