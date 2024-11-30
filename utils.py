import networkx as nx
from typing import Iterable, Literal
import pandas as pd


def read_time_stamped_csv(
    uri: str,
    format: Literal["datetime", "numeric"] = "numeric",
    columns=("Source", "Target", "Timestamp"),
    is_directed=True,
) -> tuple[nx.MultiDiGraph, Iterable[tuple[str, str, dict]]]:
    source_column, target_column, timestamp_column = columns

    dataset_df = pd.read_csv(uri)
    if format == "datetime":
        dataset_df[timestamp_column] = pd.to_datetime(dataset_df[timestamp_column])

    G = nx.from_pandas_edgelist(
        dataset_df,
        source=source_column,
        target=target_column,
        edge_attr=[timestamp_column],
        create_using=nx.MultiDiGraph if is_directed else nx.MultiGraph,
    )

    if not is_directed:
        G = G.to_directed()

    return (G, sorted(G.edges(data=True), key=lambda x: x[2][timestamp_column]))
