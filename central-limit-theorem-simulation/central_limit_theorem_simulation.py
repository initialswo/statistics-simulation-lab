import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_DIR = Path(__file__).parent
FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)


def simulate_exponential_means(rng, sample_size, repetitions, scale_factor):
    samples = rng.exponential(
        scale=scale_factor,
        size=(repetitions, sample_size)
    )
    means = np.mean(samples, axis=1)

    return means


def compare_sample_sizes(rng, sample_sizes, repetitions, scale_factor):
    means_dict = {}

    for sample_size in sample_sizes:
        means = simulate_exponential_means(
            rng,
            sample_size,
            repetitions,
            scale_factor
        )
        means_dict[sample_size] = means

    return means_dict


def standardize_sample_means(
    sample_means,
    population_mean,
    population_sd,
    sample_size
):
    standard_error = population_sd / math.sqrt(sample_size)

    standardized_sample_means = (
        sample_means - population_mean
    ) / standard_error

    return standardized_sample_means


def validate_sample_means(
    sample_means,
    repetitions,
    expected_mean,
    theoretical_standard_error
):
    empirical_mean = np.mean(sample_means)
    empirical_standard_deviation = np.std(sample_means, ddof=1)

    assert sample_means.shape == (repetitions,), (
        "Sample means shape assertion failed"
    )

    assert np.all(sample_means > 0), (
        "Negative sample means"
    )

    assert np.all(np.isfinite(sample_means)), (
        "Sample means values not finite"
    )

    assert np.isclose(
        empirical_mean,
        expected_mean,
        rtol=0,
        atol=0.03
    ), "Empirical mean is not within expected range"

    assert np.isclose(
        empirical_standard_deviation,
        theoretical_standard_error,
        rtol=0,
        atol=0.02
    ), "Empirical standard deviation is not within expected range"


def calculate_interval_proportions(standardized_means):
    within_one_standard_deviation = (
        np.abs(standardized_means) <= 1
    )

    within_two_standard_deviations = (
        np.abs(standardized_means) <= 2
    )

    within_three_standard_deviations = (
        np.abs(standardized_means) <= 3
    )

    proportion_one_standard_deviation = np.mean(
        within_one_standard_deviation
    )

    proportion_two_standard_deviations = np.mean(
        within_two_standard_deviations
    )

    proportion_three_standard_deviations = np.mean(
        within_three_standard_deviations
    )

    return {
        1: proportion_one_standard_deviation,
        2: proportion_two_standard_deviations,
        3: proportion_three_standard_deviations
    }


def check_reproducibility(
    sample_size,
    repetitions,
    scale_factor,
    seed,
    test_seed
):
    rng = np.random.default_rng(seed=seed)

    result_a = simulate_exponential_means(
        rng,
        sample_size,
        repetitions,
        scale_factor
    )

    rng = np.random.default_rng(seed=seed)

    result_b = simulate_exponential_means(
        rng,
        sample_size,
        repetitions,
        scale_factor
    )

    rng = np.random.default_rng(seed=test_seed)

    result_c = simulate_exponential_means(
        rng,
        sample_size,
        repetitions,
        scale_factor
    )

    assert np.array_equal(
        result_a,
        result_b
    ), "Identical array assertion failed"

    assert not np.array_equal(
        result_a,
        result_c
    ), "Different array assertion failed"


def plot_sample_size_comparison(results, population_mean):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    for ax, (sample_size, sample_means) in zip(
        axes.flat,
        results.items()
    ):
        ax.hist(
            sample_means,
            bins=50,
            density=True,
            edgecolor="black",
            color="skyblue"
        )

        ax.axvline(
            x=population_mean,
            color="red",
            linestyle="--",
            linewidth=2
        )

        ax.set_title(f"Sample Size n = {sample_size}")
        ax.set_xlabel("Sample Mean")
        ax.set_ylabel("Density")
        ax.set_xlim(0, 8)

    fig.suptitle("Central Limit Theorem Simulation Results")
    fig.tight_layout()

    fig.savefig(
        FIGURES_DIR / "central_limit_theorem_simulation_results.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


def plot_standardized_comparison(standardized_results):
    standard_normal_density_x = np.linspace(-4, 4, 200)

    standard_normal_density_y = (
        1 / np.sqrt(2 * np.pi)
    ) * np.exp(
        -(standard_normal_density_x ** 2) / 2
    )

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    for ax, (sample_size, standardized_means) in zip(
        axes.flat,
        standardized_results.items()
    ):
        ax.hist(
            standardized_means,
            bins=50,
            density=True,
            edgecolor="black",
            color="skyblue"
        )

        ax.axvline(
            x=0,
            color="red",
            linestyle="--",
            linewidth=2
        )

        ax.plot(
            standard_normal_density_x,
            standard_normal_density_y,
            color="purple",
            linewidth=2
        )

        ax.set_title(f"Sample Size n = {sample_size}")
        ax.set_xlabel("Standardized Sample Mean")
        ax.set_ylabel("Density")
        ax.set_xlim(-4, 4)

    fig.suptitle(
        "Central Limit Theorem Simulation Standardized Results"
    )

    fig.tight_layout()

    fig.savefig(
        FIGURES_DIR
        / "central_limit_theorem_simulation_standardized_results.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)


def main():
    sample_sizes = [1, 5, 30, 100]
    repetitions = 20_000
    scale_factor = 2.0

    population_mean = scale_factor
    population_sd = scale_factor

    seed = 42
    test_seed = 67

    rng = np.random.default_rng(seed=seed)

    results = compare_sample_sizes(
        rng,
        sample_sizes,
        repetitions,
        scale_factor
    )

    standardized_results = {}

    for sample_size, sample_means in results.items():
        theoretical_standard_error = (
            population_sd / math.sqrt(sample_size)
        )

        check_reproducibility(
            sample_size,
            repetitions,
            scale_factor,
            seed,
            test_seed
        )

        validate_sample_means(
            sample_means,
            repetitions,
            population_mean,
            theoretical_standard_error
        )

    for sample_size, sample_means in results.items():
        empirical_mean = np.mean(sample_means)

        empirical_standard_deviation = np.std(
            sample_means,
            ddof=1
        )

        theoretical_standard_error = (
            population_sd / math.sqrt(sample_size)
        )

        standardized_sample_means = standardize_sample_means(
            sample_means,
            population_mean,
            population_sd,
            sample_size
        )

        standardized_results[
            sample_size
        ] = standardized_sample_means

        standardized_mean = np.mean(
            standardized_sample_means
        )

        standardized_sd = np.std(
            standardized_sample_means,
            ddof=1
        )

        interval_proportions = calculate_interval_proportions(
            standardized_sample_means
        )

        print(f"n = {sample_size}")
        print(f"Empirical mean: {empirical_mean}")
        print(
            "Empirical standard deviation: "
            f"{empirical_standard_deviation}"
        )
        print(
            "Theoretical standard error: "
            f"{theoretical_standard_error}"
        )
        print(f"Standardized mean: {standardized_mean}")
        print(
            "Standardized standard deviation: "
            f"{standardized_sd}"
        )
        print(
            f"Within z = ±1: "
            f"{interval_proportions[1]:.2%}"
        )
        print(
            f"Within z = ±2: "
            f"{interval_proportions[2]:.2%}"
        )
        print(
            f"Within z = ±3: "
            f"{interval_proportions[3]:.2%}"
        )
        print()

    plot_sample_size_comparison(
        results,
        population_mean
    )

    plot_standardized_comparison(
        standardized_results
    )


if __name__ == "__main__":
    main()