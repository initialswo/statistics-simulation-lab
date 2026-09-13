# Central Limit Theorem Simulation

## Question

How does the distribution of sample means change as sample size increases?

## Method

This simulation uses an exponential distribution, which is strongly right-skewed. The program repeatedly takes samples from this distribution and calculates the mean of each sample.

The simulation compares different sample sizes:

1. n = 1
2. n = 5
3. n = 30
4. n = 100

For each sample size, the program:

1. Generates many random samples from an exponential distribution.
2. Calculates the mean of each sample.
3. Compares the empirical mean to the true population mean.
4. Compares the empirical standard deviation to the theoretical standard error.
5. Standardizes the sample means.
6. Checks the proportion of standardized sample means within ±1, ±2, and ±3 standard deviations.
7. Creates plots comparing the sampling distributions.

The sample means are standardized using:

standardized sample mean = (sample mean - population mean) / standard error

where:

standard error = population standard deviation / square root of sample size

For this simulation, the exponential distribution uses a scale factor of 2.0, so:

population mean = 2.0

population standard deviation = 2.0

## Result

As the sample size increases, the sampling distribution of the sample mean becomes more nearly normal.

For n = 1, the distribution is still highly skewed because each “sample mean” is just one value from the original exponential distribution.

For n = 5, the distribution begins to look more symmetric.

For n = 30 and n = 100, the standardized sample means are much closer to the standard normal distribution.

The interval proportions also support this pattern. For a standard normal distribution, approximately:

* 68.27% of values are within ±1 standard deviation
* 95.45% of values are within ±2 standard deviations
* 99.73% of values are within ±3 standard deviations

For n = 100, this simulation produced approximately:

* 68.57% within ±1 standard deviation
* 95.60% within ±2 standard deviations
* 99.71% within ±3 standard deviations

These results are very close to the standard normal benchmarks.

The simulation also shows that the spread of the sample means decreases as sample size increases. This matches the theoretical standard error:

standard error = population standard deviation / square root of sample size

The program creates two plots:

1. A plot showing the distribution of sample means for each sample size.
2. A plot showing the standardized sample means with a standard normal curve overlay.

In the plots:

* Blue histograms = simulated sample means or standardized sample means
* Red dashed vertical line = population mean in the first figure and 0 in the standardized figure
* Purple curve = standard normal density curve in the standardized figure

## What I Learned

This simulation demonstrates the Central Limit Theorem.

Even when the original population is not normally distributed, the sampling distribution of the sample mean becomes approximately normal as the sample size increases.

This helped me understand that the Central Limit Theorem is not saying the original data becomes normal. Instead, it says the distribution of sample means becomes approximately normal when we repeatedly take samples from a population.

The simulation also showed that larger sample sizes reduce the spread of the sample means. This happens because the standard error decreases as sample size increases.

It also showed that standardizing a distribution does not automatically make it normal. For small sample sizes, the standardized values can still have a strongly non-normal shape even when their mean is close to 0 and their standard deviation is close to 1.

## Files

central_limit_theorem_simulation.py

README.md

figures/central_limit_theorem_simulation_results.png

figures/central_limit_theorem_simulation_standardized_results.png

## Possible Future Extension

A future version of this module could compare different original population distributions, such as uniform, binomial, and normal distributions, to show how the Central Limit Theorem behaves across many different population shapes with finite variance.
