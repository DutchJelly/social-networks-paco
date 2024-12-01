import causalpathalgorithms

datasets = ["data/college-msg.csv", "data/reality-mining.csv"]
algorithms = [
    ("PaCo", causalpathalgorithms.PaCo),
    ("PaCo2", causalpathalgorithms.PaCo2),
    ("PathPy", causalpathalgorithms.pathpy_causal_paths),
    ("PathPy2", causalpathalgorithms.pathpy2_causal_paths),
]
results_dir = "results"
