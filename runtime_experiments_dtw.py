import time
import sys
import pandas as pd
import utils
import config
import numpy as np


def compare_runtime(
    configuration: dict, algorithms: list[tuple[str, any]], verbose=False
):
    results = {}
    for alg_name, alg in algorithms:
        start_time = time.process_time()
        alg(**configuration)
        end_time = time.process_time()
        results[alg_name] = end_time - start_time
        if verbose:
            print(f"Finished with {alg_name}")
    return results


def exp_runtime(dataset_sorted_edges, algorithms, progress_file, verbose=False):
    edge_list_size_step = len(dataset_sorted_edges) / 10
    reality_mining_avg_time_step = 16.704334086681733  # computed in window_sizes.ipynb
    dataset_avg_time_step = np.diff(
        np.array(
            [int(time_dict["Timestamp"]) for _, _, time_dict in dataset_sorted_edges]
        )
    ).mean()
    print("dataset average time step: " + str(dataset_avg_time_step))

    dt_list = list(range(10, 121, 10))

    # dictionary containing parameter keys and the values that we want to test. Each value is a tuple containing
    # the readable format and the real parameter
    alg_parameter_ranges = {
        "max_path_length": range(1, 15),
        "sorted_edges": list(
            range(
                edge_list_size_step,
                len(dataset_sorted_edges),
                edge_list_size_step,
            )
        )
        + [len(dataset_sorted_edges)],
        "delta_time": [dt / reality_mining_avg_time_step for dt in dt_list],
    }
    alg_parameter_defaults = {
        "sorted_edges": len(dataset_sorted_edges),
        "delta_time": 30 / reality_mining_avg_time_step,
        "max_path_length": 4,
    }
    parameter_preprocessors = {
        "sorted_edges": lambda n: dataset_sorted_edges[:n],
        "delta_time": lambda m: int(m * 60 * dataset_avg_time_step),
    }

    results = []

    for param_key in alg_parameter_ranges.keys():
        if verbose:
            print(f"testing {param_key}")
        for param_value in alg_parameter_ranges[param_key]:
            # Merge defaults with current iteration
            readable_params = alg_parameter_defaults | {param_key: param_value}

            # Apply processing to readable parameters to create proper parameters like an edge set or timedelta object
            processed_params = readable_params.copy()
            for processor_key, processor in parameter_preprocessors.items():
                processed_params[processor_key] = processor(
                    readable_params[processor_key]
                )

            runtimes_dict = compare_runtime(processed_params, algorithms, verbose)
            current_result = runtimes_dict | {"experiment": param_key} | readable_params
            results.append(current_result)
            pd.DataFrame(results).to_csv(progress_file, index=False)

    return results


def main():
    selected_algorithms = [
        config.algorithms[int(sys.argv[i])] for i in range(2, len(sys.argv))
    ]
    algorithms_string = "_".join([alg[0] for alg in selected_algorithms])
    progress_file_name = (
        f"dtw_{config.results_dir}/{algorithms_string}_{sys.argv[1]}.progress.csv"
    )
    results_file_name = (
        f"dtw_{config.results_dir}/{algorithms_string}_{sys.argv[1]}.csv"
    )
    print(f"testing {algorithms_string}")
    print(f"will save progress to {progress_file_name}")
    print(f"will save final results to {results_file_name}")

    _, edges = utils.read_time_stamped_csv(config.datasets[int(sys.argv[1])])

    results = exp_runtime(edges, selected_algorithms, progress_file_name)
    pd.DataFrame(results).to_csv(results_file_name, index=False)


if __name__ == "__main__":
    main()
