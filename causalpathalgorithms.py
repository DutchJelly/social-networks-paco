from typing import Iterable
from pathpy import TemporalNetwork, Paths
from pathpy.Log import Log, Severity


def PaCo(sorted_edges, delta_time, max_path_length, verbose=False):
    counts = dict()
    window = list()
    for source, target, time in sorted_edges:
        time = time["Timestamp"]
        current_counts = dict()
        current_counts[(source, target)] = 1

        # remove items from the window that are too old (from looking at delta_time)
        window = [
            (source_window, target_window, time_window, dict_window)
            for source_window, target_window, time_window, dict_window in window
            if time_window >= time - delta_time
        ]
        for source_window, target_window, time_window, counts_window in window:
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
        for time_window, counts_window in previously_seen_connecting_edges:
            if time_window < time - delta_time:
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
    if not verbose:
        Log.setMinSeverity(Severity.ERROR)

    temporal_network = TemporalNetwork()
    for source, target, time in sorted_edges:
        time = time["Timestamp"]
        temporal_network.addEdge(source, target, time)

    causal_paths = Paths.fromTemporalNetwork(
        temporal_network, delta_time, max_path_length
    )
    # print(max_path_length)
    # for p, counts in causal_paths.paths[max_path_length - 1].items():
    #     print(f"{p} -> {counts[1]}")

    # for l in causal_paths.paths:
    #     for p in causal_paths.paths[l]:
    #         if causal_paths.paths[l][p][1] > 0:
    #             print("{0} -> {1}".format(p, causal_paths.paths[l][p][1]))

    return causal_paths
