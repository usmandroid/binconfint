![binconfint banner](https://raw.githubusercontent.com/usmandroid/binconfint/main/docs/binconfint_banner.svg)
# binconfint - Python based confidence Interval for binomial data

## Use Cases

### Communications/Signal Processing
Estimate bit error rate (BER) from test results with statistical confidence:

```python
from binconfint import berconfint

# After transmitting 1,000,000 bits, 15 errors detected
ber, ci = berconfint(15, 1_000_000)
ci_lower, ci_upper = ci
print(f"BER: {ber:.2e} with 95% CI: [{ci_lower:.2e}, {ci_upper:.2e}]")
```

### Quality Control/Testing
Estimate defect rates with confidence intervals:

```python
from binconfint import berconfint

# 3 defective units out of 500 tested
ber, ci = berconfint(3, 500, level=0.99)
ci_lower, ci_upper = ci
print(f"Defect Rate with 99% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
```

### Clinical Trials / Medical Statistics
Calculate success rate confidence intervals:

```python
from binconfint import berconfint

# Treatment success: 42 out of 50 patients
success_rate, ci = berconfint(42, 50, level=0.95)
ci_lower, ci_upper = ci
print(f"Success Rate with 95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
```

## Algorithm Details

The confidence intervals use the **F-distribution method**, which is more accurate for extreme cases (0 errors or all errors) compared to normal approximation.

**References:**
- Johnson, Norman L., Kotz, Samuel, & Kemp, Adrienne W., "Univariate Discrete Distributions, Second Edition", Wiley 1992 p. 124-130.
- Abramowitz, M. and Stegun, I. A., "Handbook of Mathematical Functions", Government Printing Office, 1964, 26.6.2
