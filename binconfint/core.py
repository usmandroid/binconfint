"""
Binomial Confidence Interval Module - Core Implementation

Binomial confidence interval calculations using F-distribution method.
Reference: Johnson, Kotz & Kemp "Univariate Discrete Distributions"
"""

import numpy as np
from scipy import stats


def berconfint(n_errs, n_trials, level=0.95):
    """
    BER and confidence interval of Monte Carlo simulation.

    Parameters
    ----------
    n_errs : int
        Number of errors observed
    n_trials : int
        Total number of trials
    level : float, optional
        Confidence level (default 0.95 for 95% CI)

    Returns
    -------
    ber : float
        Bit error rate (error probability)
    interval : ndarray
        Confidence interval as [lower, upper] bounds
    """
    n_errs = int(n_errs)
    n_trials = int(n_trials)

    if n_errs < 0:
        raise ValueError("n_errs must be non-negative")
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    if n_errs > n_trials:
        raise ValueError("n_errs cannot exceed n_trials")
    if level < 0 or level > 1:
        raise ValueError("level must be between 0 and 1")

    alpha = 1 - level
    ber, interval = binofit(n_errs, n_trials, alpha)

    return ber, interval


def binofit(x, n, alpha=0.05):
    """
    Parameter estimates and confidence intervals for binomial data.

    Parameters
    ----------
    x : int or float
        Number of successes
    n : int or float
        Number of trials
    alpha : float, optional
        Significance level (default 0.05 for 95% CI)

    Returns
    -------
    phat : float
        Maximum likelihood estimate of success probability
    pci : ndarray
        Confidence interval as [lower, upper] bounds shape (2,)
    """
    x = float(x)
    n = float(n)
    alpha = float(alpha)

    if n < 0 or n != int(n):
        raise ValueError("n must be a non-negative integer")
    if x < 0:
        raise ValueError("x must be non-negative")
    if x > n:
        raise ValueError("x cannot exceed n")
    if not (0 <= alpha <= 1):
        raise ValueError("alpha must be between 0 and 1")

    phat = x / n
    pci = _statbinoci(x, n, alpha)

    return phat, pci


def _statbinoci(x, n, alpha):
    """
    Confidence interval for binomial p parameter using F-distribution.

    Parameters
    ----------
    x : float
        Number of successes
    n : float
        Number of trials
    alpha : float
        Significance level

    Returns
    -------
    pci : ndarray
        Confidence interval as [lower, upper] bounds shape (2,)
    """
    x = float(x)
    n = float(n)

    # Lower limits
    nu1 = 2.0 * x
    nu2 = 2.0 * (n - x + 1.0)

    if nu1 == 0:
        lb = 0.0
    else:
        F = stats.f.ppf(alpha / 2.0, nu1, nu2)
        lb = (nu1 * F) / (nu2 + nu1 * F)

    # Upper limits
    nu1 = 2.0 * (x + 1.0)
    nu2 = 2.0 * (n - x)

    if nu2 == 0:
        ub = 1.0
    else:
        F = stats.f.ppf(1.0 - alpha / 2.0, nu1, nu2)
        ub = (nu1 * F) / (nu2 + nu1 * F)

    return np.array([lb, ub])
