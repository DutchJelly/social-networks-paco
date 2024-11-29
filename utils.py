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
