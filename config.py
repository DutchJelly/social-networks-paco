import causalpathalgorithms

datasets = [
    {"uri": "data/college-msg.csv", "is_directed": True},
    {"uri": "data/reality-mining.csv", "is_directed": False},
    {"uri": "data/sx-stackoverflow.csv", "is_directed": True},
]
algorithms = [
    ("PaCo", causalpathalgorithms.PaCo),
    ("PaCo2", causalpathalgorithms.PaCo2),
    ("PathPy", causalpathalgorithms.pathpy_causal_paths),
    ("PathPy2", causalpathalgorithms.pathpy2_causal_paths),
]

# average time step in reality mining dataset, which is used as reference
reference_avg_time_step = 16.704334086681733
