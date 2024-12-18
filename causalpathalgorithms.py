from typing import Iterable
import pathpy1 as pp1
import pathpy2 as pp2
import pathpy3 as pp3
import pathpyG as ppg


def PaCo(sorted_edges, delta_time, max_path_length, verbose=False):
    counts = {}
    window = []
    for idx, (source, target, time) in enumerate(sorted_edges):
        time = time["Timestamp"]
        current_counts = dict()
        current_counts[(source, target)] = 1

        out_of_scope_count = 0
        for source_window, target_window, time_window, counts_window in window:
            if time_window < time - delta_time:
                out_of_scope_count += 1
                continue

            # skip if edge in window doesn't connect or is not formed after time
            if target_window != source or time <= time_window:
                continue

            # look through the window which paths can be exteded with current edge
            for path in counts_window.keys():
                # Check if the length of path is not too large to add a node to it given max_path_length
                if len(path) - 1 >= max_path_length:
                    continue
                # combine path in window with current edge, and count the path variations
                combined_path = (*path, target)
                current_counts[combined_path] = (
                    current_counts.get(combined_path, 0) + counts_window[path]
                )
        # remove items from the window that are too old (from looking at delta_time)
        if out_of_scope_count > 0:
            del window[:out_of_scope_count]

        if verbose:
            print("current counts", current_counts)

        # Add current_counts to counts
        for key in current_counts:
            counts[key] = counts.get(key, 0) + current_counts[key]

        # Increment window
        window.append((source, target, time, current_counts))
    return counts


def PaCo2(
    sorted_edges: Iterable[tuple[str, str, dict]],
    delta_time: int,
    max_path_length: int,
    verbose=False,
):
    counts = dict()
    window = dict()
    for source, target, time in sorted_edges:
        time = time["Timestamp"]
        current_counts = dict()
        current_counts[(source, target)] = 1

        previously_seen_connecting_edges = window.get(source, list())
        out_of_scope_count = 0
        for time_window, counts_window in previously_seen_connecting_edges:
            if time_window < time - delta_time:
                out_of_scope_count += 1
                continue

            for path in counts_window.keys():
                # Check if the length of path is not too large to add a node to it given max_path_length
                if len(path) - 1 >= max_path_length:
                    continue
                # combine path in window with current edge, and count the path variations
                combined_path = (*path, target)
                current_counts[combined_path] = (
                    current_counts.get(combined_path, 0) + counts_window[path]
                )
        if out_of_scope_count > 0:
            del previously_seen_connecting_edges[:out_of_scope_count]

        if verbose:
            print("current counts", current_counts)

        # Add current_counts to counts
        for key in current_counts:
            counts[key] = counts.get(key, 0) + current_counts[key]

        window[target] = window.get(target, list())
        window[target].append((time, current_counts))
    return counts


def pathpy_causal_paths(
    sorted_edges: Iterable[tuple[str, str, dict]],
    delta_time: int,
    max_path_length: int,
    verbose=False,
):
    temporal_network = pp1.TemporalNetwork()
    for source, target, time in sorted_edges:
        time = time["Timestamp"]
        temporal_network.addEdge(source, target, time)

    causal_paths = pp1.Paths.fromTemporalNetwork(
        temporal_network, delta_time, max_path_length
    )
    return causal_paths


# This version seems to ignore max path length
def pathpy2_causal_paths(
    sorted_edges: Iterable[tuple[str, str, dict]],
    delta_time: int,
    max_path_length: int,
    verbose=False,
):
    temporal_network = pp2.TemporalNetwork()
    for source, target, time in sorted_edges:
        time = time["Timestamp"]
        temporal_network.add_edge(source, target, time)

    causal_paths = pp2.path_extraction.paths_from_temporal_network_dag(
        temporal_network, delta=delta_time, max_subpath_length=max_path_length
    )

    for l in causal_paths.paths:
        for p in causal_paths.paths[l]:
            if causal_paths.paths[l][p][1] > 0:
                print("{0} -> {1}".format(p, causal_paths.paths[l][p][1]))

    return causal_paths


# Unfortunatly this seems to be broken
def pathpy3_causal_paths(
    sorted_edges: Iterable[tuple[str, str, dict]],
    delta_time: int,
    max_path_length: int,
    verbose=False,
):
    temporal_network = pp3.TemporalNetwork(directed=True, multiedges=True)
    for source, target, time in sorted_edges:
        time = time["Timestamp"]
        temporal_network.add_edge(source, target, timestamp=time)

    paths = pp3.algorithms.path_extraction.all_paths_from_temporal_network(
        temporal_network, delta_time, max_path_length
    )

    return paths


def pathpy_g_causal_paths(
    sorted_edges: Iterable[tuple[str, str, dict]],
    delta_time: int,
    max_path_length: int,
    verbose=False,
):
    sorted_edges = [
        (s, t, int(timestamp_dict["Timestamp"]))
        for (s, t, timestamp_dict) in sorted_edges
    ]
    temporal_network = ppg.TemporalGraph.from_edge_list(sorted_edges)
    causal_paths = ppg.MultiOrderModel.from_temporal_graph(
        temporal_network, delta_time, max_order=max_path_length
    )
    # ppg.algorithms.lift_order_temporal(temporal_network, delta_time)
    # e_i = ppg.algorithms.lift_order_temporal(t, delta=1)
    # dag = ppg.Graph.from_edge_index(e_i)
    # pp.plot(dag, node_label = [f'{v}-{w}-{time}' for v, w, time in t.temporal_edges]);
    # return paths
    return None
