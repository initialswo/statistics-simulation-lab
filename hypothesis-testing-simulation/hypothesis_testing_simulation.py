import numpy as np
import math

def generate_sample(rng, null_mean, population_sd, sample_size):
    sample = rng.normal(loc=null_mean, scale=population_sd, size=sample_size)

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

def main():
    rng = np.random.default_rng()
    null_mean = 50
    population_sd = 10
    sample_size = 30

    sample = generate_sample(rng, null_mean, population_sd, sample_size)
    sample_mean = calculate_sample_mean(sample)
    standard_error = calculate_standard_error(population_sd, sample_size)

    print(sample)
    print(sample_mean)
    print(standard_error)

if __name__ == "__main__":
    main()