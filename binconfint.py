"""
Binomial confidence interval module for Monte Carlo simulation analysis.

Calculates binomial parameter estimates and confidence intervals using the
F-distribution method with numpy and scipy.stats.
"""

import numpy as np
from scipy import stats


class BinomialConfidenceInterval:
    """
    Computes binomial parameter estimates and confidence intervals.

    Uses the F-distribution method for accurate confidence interval calculation.
    Reference: Johnson, Kotz & Kemp "Univariate Discrete Distributions"
    """

    def __init__(self):
        """Initialize the BinomialConfidenceInterval calculator."""
        pass

    @staticmethod
    def berconfint(n_errs, n_trials, level=0.95):
        """
        BER and confidence interval of Monte Carlo simulation.

        Parameters
        ----------
        n_errs : int or array-like
            Number of errors observed
        n_trials : int or array-like
            Total number of trials
        level : float, optional
            Confidence level (default 0.95 for 95% CI)

        Returns
        -------
        ber : float or ndarray
            Bit error rate (error probability)
        interval : ndarray
            Confidence interval as [lower, upper] bounds

        Raises
        ------
        ValueError
            If inputs are invalid or n_errs > n_trials
        """
        # Input validation
        n_errs = np.asarray(n_errs, dtype=int)
        n_trials = np.asarray(n_trials, dtype=int)

        if np.any(n_errs < 0):
            raise ValueError("n_errs must be non-negative")
        if np.any(n_trials <= 0):
            raise ValueError("n_trials must be positive")
        if np.any(n_errs > n_trials):
            raise ValueError("n_errs cannot exceed n_trials")
        if level < 0 or level > 1:
            raise ValueError("level must be between 0 and 1")

        # Use binofit with converted alpha
        alpha = 1 - level
        ber, interval = BinomialConfidenceInterval.binofit(n_errs, n_trials, alpha)

        return ber, interval

    @staticmethod
    def binofit(x, n, alpha=0.05):
        """
        Parameter estimates and confidence intervals for binomial data.

        Parameters
        ----------
        x : int or array-like
            Number of successes
        n : int or array-like
            Number of trials
        alpha : float, optional
            Significance level (default 0.05 for 95% CI)

        Returns
        -------
        phat : float or ndarray
            Maximum likelihood estimate of success probability
        pci : ndarray
            Confidence interval as [lower, upper] bounds or shape (N, 2)
        """
        # Store original shape to return appropriate type
        x_orig = x
        n_orig = n
        is_scalar = np.isscalar(x_orig) and np.isscalar(n_orig)

        x = np.asarray(x, dtype=float)
        n = np.asarray(n, dtype=float)
        alpha = float(alpha)

        # Input validation
        if np.any(n < 0) or np.any(n != np.round(n)) or np.any(np.isinf(n)):
            raise ValueError("n must be non-negative integers")
        if np.any(x < 0):
            raise ValueError("x must be non-negative")
        if np.any(x > n):
            raise ValueError("x cannot exceed n")
        if not (0 <= alpha <= 1):
            raise ValueError("alpha must be between 0 and 1")

        # Check if x contains non-integers (warning only)
        if np.any(x != np.round(x)):
            print("Warning: x contains non-integer values")

        # MLE of p
        phat = x / n

        # Compute confidence intervals
        pci = BinomialConfidenceInterval._statbinoci(x, n, alpha)

        # For scalar inputs, return scalar phat and 1D interval array
        if is_scalar:
            phat = float(phat)
            pci = pci.flatten()

        return phat, pci

    @staticmethod
    def _statbinoci(x, n, alpha):
        """
        Confidence interval for binomial p parameter using F-distribution.

        Parameters
        ----------
        x : ndarray
            Number of successes
        n : ndarray
            Number of trials
        alpha : float
            Significance level

        Returns
        -------
        pci : ndarray
            Shape (N, 2) array of [lower, upper] confidence bounds
        """
        x = np.asarray(x, dtype=float).flatten()
        n = np.asarray(n, dtype=float).flatten()

        # Ensure same shape
        if x.size == 1:
            x = np.repeat(x, n.size)
        if n.size == 1:
            n = np.repeat(n, x.size)

        if x.size != n.size:
            raise ValueError("x and n must have compatible shapes")

        # Lower limits
        nu1 = 2 * x
        nu2 = 2 * (n - x + 1)
        F = stats.f.ppf(alpha / 2, nu1, nu2)
        lb = (nu1 * F) / (nu2 + nu1 * F)

        # Fix NaNs caused by x=0
        lb[x == 0] = 0

        # Upper limits
        nu1 = 2 * (x + 1)
        nu2 = 2 * (n - x)
        F = stats.f.ppf(1 - alpha / 2, nu1, nu2)
        ub = (nu1 * F) / (nu2 + nu1 * F)

        # Fix NaNs caused by x=n
        ub[x == n] = 1

        # Combine into [lower, upper] format
        pci = np.column_stack([lb, ub])

        return pci


# Core functions for binomial confidence interval calculation
def berconfint(n_errs, n_trials, level=0.95):
    """Wrapper for BER and confidence interval calculation."""
    return BinomialConfidenceInterval.berconfint(n_errs, n_trials, level)


def binofit(x, n, alpha=0.05):
    """Wrapper for binomial parameter estimation and confidence intervals."""
    return BinomialConfidenceInterval.binofit(x, n, alpha)
