import random
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE_DIR = Path(__file__).parent
FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

def generate_population(population_size):
    return [random.randint(1, 100) for _ in range(population_size)]

def calculate_population_mean(population):
    return sum(population) / len(population)

def take_sample(population, sample_size):
    return random.sample(population, k=sample_size)

def calculate_sample_mean(sample):
    return sum(sample) / len(sample)

def calculate_sample_standard_deviation(sample):
    mean = calculate_sample_mean(sample)
    sum_squared_deviations = 0

    for value in sample:
        squared_deviation = (value - mean) ** 2
        sum_squared_deviations += squared_deviation

    sample_variance = sum_squared_deviations / (len(sample) - 1)
    sample_standard_deviation = math.sqrt(sample_variance)

    return sample_standard_deviation

def calculate_confidence_interval(sample):
    sample_mean = calculate_sample_mean(sample)
    sample_standard_deviation = calculate_sample_standard_deviation(sample)
    standard_error = sample_standard_deviation / math.sqrt(len(sample))
    margin_error = 1.96 * standard_error
    lower_bound = sample_mean - margin_error
    upper_bound = sample_mean + margin_error

    return (lower_bound, upper_bound)

def contains_population_mean(confidence_interval, population_mean):
    lower_bound, upper_bound = confidence_interval

    if population_mean >= lower_bound and population_mean <= upper_bound:
        return True
    else:
        return False

def run_confidence_interval_simulation(population, sample_size, number_of_samples):
    population_mean = calculate_population_mean(population)
    intervals_containing_mean_count = 0
    interval_results = []

    for _ in range(number_of_samples):
        sample = take_sample(population, sample_size)
        confidence_interval = calculate_confidence_interval(sample)
        contains_mean = contains_population_mean(confidence_interval, population_mean)

        if contains_mean == True:
            intervals_containing_mean_count += 1

        interval_result = (confidence_interval, contains_mean)
        interval_results.append(interval_result)
    
    capture_rate = intervals_containing_mean_count / number_of_samples
    
    return capture_rate, intervals_containing_mean_count, interval_results, population_mean

def plot_confidence_intervals(interval_results, population_mean):
    fig, ax = plt.subplots(figsize=(8, 5))

    for index, interval in enumerate(interval_results):
        index += 1
        confidence_interval, contains_mean = interval
        lower_bound, upper_bound = confidence_interval

        if contains_mean is True: 
            ax.hlines(
                y=index,
                xmin=lower_bound,
                xmax=upper_bound,
                color="green",
                linestyle="-",
                linewidth=2
            )
        else: 
            ax.hlines(
                y=index,
                xmin=lower_bound,
                xmax=upper_bound,
                color="red",
                linestyle="-",
                linewidth=2
            )

    ax.axvline(
        x=population_mean,
        color="black",
        linestyle="--",
        linewidth=2
    )

    ax.set_title("Confidence Interval Simulation Results")
    ax.set_xlabel("Confidence Interval Bounds")
    ax.set_ylabel("Confidence Intervals")

    legend_items = [
        Line2D([0], [0], color="green", linewidth=2, label="Interval captured mean"),
        Line2D([0], [0], color="red", linewidth=2, label="Interval missed mean"),
        Line2D([0], [0], color="black", linestyle="--", linewidth=2, label="True population mean"),
    ]

    ax.legend(
        handles=legend_items,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=3
    )
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "confidence_interval_simulation_results.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

def main():
    POPULATION_SIZE = 10000
    SAMPLE_SIZE = 30
    NUMBER_OF_SAMPLES = 100
    CONFIDENCE_LEVEL = 0.95

    population = generate_population(POPULATION_SIZE)

    capture_rate, intervals_containing_mean_count, interval_results, population_mean = run_confidence_interval_simulation(
        population,
        SAMPLE_SIZE,
        NUMBER_OF_SAMPLES
    )

    capture_rate_percent = capture_rate * 100

    print(f"Population mean: {population_mean:.2f}")
    print(f"Sample size: {SAMPLE_SIZE}")
    print(f"Number of intervals: {len(interval_results)}")
    print(f"Intervals containing population mean: {intervals_containing_mean_count}")
    print(f"Capture rate: {capture_rate_percent:.2f}%")

    plot_confidence_intervals(interval_results, population_mean)


if __name__ == "__main__":
    main()