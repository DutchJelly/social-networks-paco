import networkx as nx
from typing import Iterable, Literal
import pandas as pd


def read_time_stamped_csv(
    uri: str,
    format: Literal["datetime", "numeric"] = "numeric",
    columns=("Source", "Target", "Timestamp"),
) -> tuple[nx.MultiDiGraph, Iterable[tuple[str, str, dict]]]:
    source_column, target_column, timestamp_column = columns

    dataset_df = pd.read_csv(uri)
    if format == "datetime":
        dataset_df[timestamp_column] = pd.to_datetime(
            dataset_df[timestamp_column], format="%m/%d/%y %I:%M %p"
        )

    G = nx.from_pandas_edgelist(
        dataset_df,
        source=source_column,
        target=target_column,
        edge_attr=[timestamp_column],
        create_using=nx.MultiDiGraph,
    )

    return (G, sorted(G.edges(data=True), key=lambda x: x[2][timestamp_column]))


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


def test_causal_path_algorithm(algorithm):
    _, test_edges = read_time_stamped_csv("test-edges.csv", "numeric")
    result = algorithm(test_edges, 2, 2)
    expected_result = {
        ("a", "b"): 2,
        ("b", "c"): 2,
        ("c", "d"): 1,
        ("d", "c"): 2,
        ("c", "b"): 1,
        ("b", "a"): 1,
        ("a", "b", "a"): 2,
        ("a", "b", "c"): 2,
        ("b", "c", "d"): 1,
        ("c", "b", "c"): 1,
        ("d", "c", "b"): 1,
        ("d", "c", "d"): 2,
    }
    try:
        assert result == expected_result
        print("Tests succeeded ✅")
    except:
        print("Tests failed ❌")


test_causal_path_algorithm(PaCo)
