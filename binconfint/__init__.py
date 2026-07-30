"""
Binomial Confidence Interval Module

Provides binomial confidence interval calculations using the F-distribution method.
"""

from .core import (
    berconfint,
    binofit,
)

__version__ = "0.1.0"
__author__ = "Sheikh Usman Ali"
__email__ = "usmanskp@yahoo.com"

__all__ = [
    "berconfint",
    "binofit",
]
