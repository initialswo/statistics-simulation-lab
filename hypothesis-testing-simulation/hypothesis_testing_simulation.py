import numpy as np
import math
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent
FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

def run_hypothesis_test(rng, population_mean, null_mean, population_sd, sample_size, alpha):
    sample = generate_sample(rng, population_mean, population_sd, sample_size)
    sample_mean = calculate_sample_mean(sample)
    standard_error = calculate_standard_error(population_sd, sample_size)
    z_stat = calculate_z_stat(sample_mean, null_mean, standard_error)
    p_value = calculate_p_value(z_stat)
    decision = hypothesis_test_decision(p_value, alpha)

    return z_stat, p_value, decision

def generate_sample(rng, population_mean, population_sd, sample_size):
    sample = rng.normal(loc=population_mean, scale=population_sd, size=sample_size)

    return sample

def calculate_sample_mean(sample):
    sample_mean = np.mean(sample)

    return sample_mean

def calculate_standard_error(population_sd, sample_size):
    standard_error = population_sd / math.sqrt(sample_size)

    return standard_error

def calculate_z_stat(sample_mean, null_mean, standard_error):
    z_stat = (sample_mean - null_mean) / standard_error

    return z_stat

def calculate_p_value(z_stat):
    p_val = 2 * stats.norm.cdf(-abs(z_stat))
    
    return p_val

def hypothesis_test_decision(p_value, alpha):
    return p_value < alpha

def run_repetitions(rng, population_mean, null_mean, population_sd, sample_size, alpha, repetitions):
    z_stats = []
    p_values = []
    decisions = []

    for _ in range(repetitions):
        z_stat, p_value, decision = run_hypothesis_test(rng, population_mean, null_mean, population_sd, sample_size, alpha)
        z_stats.append(z_stat)
        p_values.append(p_value)
        decisions.append(decision)

    return z_stats, p_values, decisions 

def calculate_type_1_error_rate(rejection_count, repetitions):
    rate = rejection_count / repetitions

    return rate

def calculate_p_value_below_alpha_rate(p_values, alpha):
    count = 0

    for p in p_values:
        if p < alpha:
            count += 1

    rate = count / len(p_values)

    return rate 

def validate_error_rate(rate, alpha_level, tolerance):
    return abs(rate - alpha_level) <= tolerance

def validate_mean_z_stat(mean_z_stat, z_tolerance):
    return abs(mean_z_stat) <= z_tolerance

def validate_sd_z_stat(sd_z_stat, z_tolerance):
    return abs(sd_z_stat - 1) <= z_tolerance

def validate_p_values(p_values):
    return all(0 <= p <= 1 for p in p_values)

def validate_p_value_rejection_rate(error_rate, p_value_alpha_rates, alpha):
    return error_rate == p_value_alpha_rates[alpha]

def make_z_plot(z_stats, alpha):
    plt.figure(figsize=(8, 4))

    z_critical = float(stats.norm.ppf(1 - alpha / 2))
    x_min = min(z_stats)
    x_max = max(z_stats)

    plt.hist(z_stats, bins=40, density=True, edgecolor='black', color='skyblue')
    plt.axvline(x=z_critical, color='red', label='Critical z-value')
    plt.axvline(x=-z_critical, color='red')
    plt.axvspan(z_critical, x_max, facecolor='red', alpha=0.4)
    plt.axvspan(x_min, -z_critical, facecolor='red', alpha=0.4, label='Rejection region')
    plt.title("Distribution of z-statistics")
    plt.xlabel("z-statistics")
    plt.ylabel("Density")

    x = np.linspace(x_min, x_max, 500)
    plt.plot(x, stats.norm.pdf(x), color="black", lw=2, label="Theoretical N(0, 1)")

    plt.legend()

    plt.savefig(
            FIGURES_DIR / "z_statistic_distribution.png",
            dpi=300,
            bbox_inches="tight"
        )
    
    plt.show()
    plt.close()

def make_p_plot(p_values):
    plt.figure(figsize=(8, 4))

    plt.hist(p_values, bins=10, range=(0, 1), edgecolor='black')

    plt.title("Distribution of p-values under H0")
    plt.xlabel("p-value")
    plt.ylabel("Frequency")

    plt.savefig(
                FIGURES_DIR / "p_value_distribution.png",
                dpi=300,
                bbox_inches="tight"
            )

    plt.show()
    plt.close()

def plot_alpha(p_below_alpha_rates):
    plt.figure(figsize=(8, 4))

    alpha_levels = sorted(p_below_alpha_rates.keys())
    error_rates = [p_below_alpha_rates[alpha] for alpha in alpha_levels]

    plt.plot(alpha_levels, error_rates, marker="o", label='Observed simulation')
    plt.xlabel("Significance level (alpha)")
    plt.ylabel("Observed Type I error rate")
    plt.title("Significance Level vs. Type I Error Rate")

    plt.plot(alpha_levels, alpha_levels, linestyle='--', label='Expected: error rate = alpha')

    plt.legend()

    plt.savefig(
                    FIGURES_DIR / "alpha_vs_type_1_error_rate.png",
                    dpi=300,
                    bbox_inches="tight"
                )

    plt.show()
    plt.close()

def report(count, error_rate, alpha, mean_z_stat, sd_z_stat, 
           error_rate_validation, z_mean_validation, sd_z_validation,
           p_value_validation, p_below_alpha_rates,
           p_value_rejection_rate_validation,
           alpha_level_validations):
    print(f"rejection count: {count}")
    print(f"Primary Type I error rate: {error_rate}")
    print(f"expected rate: {alpha}\n")

    print("Alpha comparison:")
    for alpha_level, rate in p_below_alpha_rates.items():
        validation = alpha_level_validations[alpha_level]
        print(f"alpha = {alpha_level} --> Type I error rate = {rate} --> validation = {validation}")

    print(f"\nmean z-statistic: {mean_z_stat}")
    print(f"z-statistic standard deviation: {sd_z_stat}")
    print(f"Type I error validation passed: {error_rate_validation}")
    print(f"Z mean validation passed: {z_mean_validation}")
    print(f"Z SD validation passed: {sd_z_validation}")
    print(f"p-value validation passed: {p_value_validation}")
    print(f"p-value rejection rate validation: {p_value_rejection_rate_validation}")

def main():
    rng = np.random.default_rng(seed=42)
    population_mean = 50
    null_mean = 50
    population_sd = 10
    sample_size = 30
    alpha = 0.05
    alpha_levels = [0.01, 0.05, 0.10]
    repetitions = 10000
    tolerance = 0.01
    z_tolerance = 0.05
    
    z_stats, p_values, decisions = run_repetitions(rng, population_mean, null_mean, population_sd, sample_size, alpha, repetitions)
    rejection_count = sum(decisions)
    type_1_error_rate = calculate_type_1_error_rate(rejection_count, repetitions)
    error_rate_validation = validate_error_rate(type_1_error_rate, alpha, tolerance)

    mean_z_stat = np.mean(z_stats)
    sd_z_stat = np.std(z_stats)

    z_mean_validation = validate_mean_z_stat(mean_z_stat, z_tolerance)
    sd_z_validation = validate_sd_z_stat(sd_z_stat, z_tolerance)
    p_value_validation = validate_p_values(p_values)

    p_below_alpha_rates = {}
    for alpha_level in alpha_levels:
        p_below_alpha_rate = calculate_p_value_below_alpha_rate(p_values, alpha_level)
        p_below_alpha_rates[alpha_level] = p_below_alpha_rate

    alpha_level_validations = {}
    for alpha_level, rate in p_below_alpha_rates.items():
        alpha_level_validations[alpha_level] = validate_error_rate(rate, alpha_level, tolerance)

    p_value_rejection_rate_validation = validate_p_value_rejection_rate(type_1_error_rate, p_below_alpha_rates, alpha)

    make_z_plot(z_stats, alpha)
    make_p_plot(p_values)
    plot_alpha(p_below_alpha_rates)

    report(
        rejection_count, 
        type_1_error_rate, 
        alpha, mean_z_stat, 
        sd_z_stat, 
        error_rate_validation,
        z_mean_validation,
        sd_z_validation,
        p_value_validation,
        p_below_alpha_rates,
        p_value_rejection_rate_validation,
        alpha_level_validations
        )


if __name__ == "__main__":
    main()