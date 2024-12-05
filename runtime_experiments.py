import time
import pandas as pd
import utils
import config
import numpy as np
from tap import Tap
import pathlib


class SimpleArgumentParser(Tap):
    dataset: str
    algorithm: str
    experiment: str
    results_dir: str = "results"
    # average time step in reality mining dataset that we use as reference
    reference_average_timestep: float = 16.704334086681733
    # timeout by default after 12 hours
    timeout: int = 12 * 60 * 60
    verbose: bool = False


def measure_runtime(
    configuration: dict, algorithm: tuple[str, any], timeout: int, verbose=False
) -> float:
    alg_name, alg_fn = algorithm
    try:
        with utils.timeout(timeout):
            start_time = time.process_time()
            alg_fn(**configuration)
            end_time = time.process_time()
            if verbose:
                print(f"Finished an evaluation with {alg_name}")
            return end_time - start_time
    except utils.TimeoutException:
        print("experiment took longer than threshold, aborting")
    return float("inf")


def run_runtime_experiment(
    dataset_sorted_edges,
    experiment,
    algorithm,
    progress_file,
    reference_timestep,
    timeout,
    verbose=False,
):
    if verbose:
        print(f"Dataset average time step: {reference_timestep:.2f}")

    # dictionary containing parameter keys and the values that we want to test
    parameter_ranges = {
        "sorted_edges": list(
            range(
                100_000,
                len(dataset_sorted_edges),
                100_000,
            )
        )
        + [len(dataset_sorted_edges)],
        "max_path_length": range(1, 15),
        "delta_time": [
            # This value represents delta time value in minutes divided by reference avg time step
            # meaning that it represents the estimated average temporal window size
            dt / config.reference_avg_time_step
            for dt in range(10, 121, 10)
        ],
    }
    # default values for the parameters
    parameter_defaults = {
        "sorted_edges": len(dataset_sorted_edges),
        "delta_time": 30 / config.reference_avg_time_step,
        "max_path_length": 4,
    }
    # mapper functions that transform parameter values to raw parameter values for algorithm
    # e.g. map sorted edges length to array containing the edges
    parameter_mappers = {
        "sorted_edges": lambda n: dataset_sorted_edges[:n],
        "delta_time": lambda m: int(m * 60 * reference_timestep),
    }

    results = []
    if verbose:
        print(f"testing {experiment}")
    for param_value in parameter_ranges[experiment]:
        # Merge defaults with current iteration
        readable_params = parameter_defaults | {experiment: param_value}

        # Map parameter values to raw values for the algorithm with preprocessors. E.g. apply scaling.
        processed_params = readable_params.copy()
        for processor_key, processor in parameter_mappers.items():
            processed_params[processor_key] = processor(readable_params[processor_key])

        # Measure the runtime of algorithm with these parameters
        runtime = measure_runtime(processed_params, algorithm, timeout, verbose)
        current_result = {
            "experiment": experiment,
            algorithm[0]: runtime,
        } | readable_params
        results.append(current_result)
        pd.DataFrame(results).to_csv(progress_file, index=False)
    return results


def main():
    args = SimpleArgumentParser().parse_args()

    algorithm = next((a for a in config.algorithms if a[0] == args.algorithm), None)
    if algorithm is None:
        print("no algorithm selected!")
        exit(1)

    dataset = next((d for d in config.datasets if args.dataset in d["uri"]), None)

    if dataset is None:
        print("no dataset selected!")
        exit(1)

    exp_filename_base = (
        f"{args.experiment}|{algorithm[0]}|{pathlib.Path(dataset["uri"]).stem}"
    )
    print(f"will save to {exp_filename_base}(.progress).csv")

    _, edges = utils.read_time_stamped_csv(**dataset)

    results = run_runtime_experiment(
        dataset_sorted_edges=edges,
        experiment=args.experiment,
        algorithm=algorithm,
        timeout=args.timeout,
        reference_timestep=args.reference_average_timestep,
        progress_file=f"{args.results_dir}/{exp_filename_base}.progress.csv",
        verbose=args.verbose,
    )
    pd.DataFrame(results).to_csv(
        f"{args.results_dir}/{exp_filename_base}.csv", index=False
    )


if __name__ == "__main__":
    main()
