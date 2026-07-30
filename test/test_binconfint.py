#!/usr/bin/env python3.12
"""
Python Test Suite for Binomial Confidence Interval

Tests binconfint.berconfint and binconfint.binofit functions with various inputs.
Logs results with timestamps for reference and comparison.
"""

import sys
import os
from datetime import datetime
import traceback

# Add parent directory to path to import binconfint
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binconfint import berconfint, binofit


def ensure_log_dir():
    """Ensure log directory exists."""
    log_dir = os.path.join(os.path.dirname(__file__), "log")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def main():
    """Run all tests and log results."""
    # Setup logging
    log_dir = ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"python_test_{timestamp}.log")

    with open(log_file, "w") as fid:
        fid.write("=== Python Binomial Confidence Interval Test Suite ===\n")
        fid.write(f"Timestamp: {datetime.now()}\n")
        fid.write("=====================================================\n\n")

        # Test cases: (n_errors, n_trials, level, description)
        test_cases = [
            (0, 100, 0.95, "Zero errors"),
            (5, 100, 0.95, "Few errors (5/100)"),
            (50, 100, 0.95, "Half errors (50/100)"),
            (95, 100, 0.95, "Most errors (95/100)"),
            (100, 100, 0.95, "All errors (100/100)"),
            (1, 1000, 0.95, "Single error in many trials"),
            (10, 100, 0.90, "Different confidence level (90%)"),
            (10, 100, 0.99, "High confidence level (99%)"),
        ]

        n_passed = 0
        n_failed = 0

        # Run tests
        for i, (n_errs, n_trials, level, description) in enumerate(test_cases, 1):
            fid.write(f"Test {i}: {description}\n")
            fid.write(
                f"  Input: n_errs={n_errs}, n_trials={n_trials}, level={level:.2f}\n"
            )

            try:
                ber, interval = berconfint(n_errs, n_trials, level)

                # Extract bounds (interval is returned as 1D array [lower, upper])
                lower = interval[0]
                upper = interval[1]

                fid.write(f"  BER: {ber:.10f}\n")
                fid.write(f"  Confidence Interval: [{lower:.10f}, {upper:.10f}]\n")
                fid.write("  Status: PASS\n\n")
                n_passed += 1

            except Exception as e:
                fid.write(f"  Error: {str(e)}\n")
                fid.write(f"  Traceback: {traceback.format_exc()}\n")
                fid.write("  Status: FAIL\n\n")
                n_failed += 1

        # Summary
        fid.write("=====================================================\n")
        fid.write("Test Summary\n")
        fid.write(f"  Total: {len(test_cases)}\n")
        fid.write(f"  Passed: {n_passed}\n")
        fid.write(f"  Failed: {n_failed}\n")
        fid.write("=====================================================\n")

    print(f"Log file written to: {log_file}")
    return 0 if n_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
