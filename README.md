# Fixed Income Portfolio: Curve Construction, Pricing, DV01 Hedging and Hull–White

Project for **Fixed Income** (MSc Quantitative Finance and Insurance, University of Turin, February 2026).

This is an end-to-end framework for pricing, assessing the risk of and hedging a portfolio of fixed-income instruments, built from raw EUR market data as of 11 December 2025.

## Contents

1. **Yield curve construction.** EURIBOR 6M zero rates and discount factors are used to calibrate a **Nelson–Siegel–Svensson** curve by least squares, followed by **cubic-spline** interpolation for exact instrument pricing.
2. **Instrument pricing.** The library prices:
   - fixed-coupon bonds,
   - floating-rate notes,
   - interest-rate swaps,
   - ATM semi-annual **caps under the Bachelier (normal) model**.
3. **Risk and hedging.** The **DV01** of each instrument and of the portfolio is computed, followed by a **delta-hedging** strategy against parallel rate shifts.
4. **Hull–White model.** The short-rate parameters are calibrated, then validated by Monte Carlo. The simulated 1Y zero-coupon price matches the curve within **0.09 bp** (20,000 paths, exact OU discretisation).

## Files

| File | Content |
|---|---|
| `FixedIncomeProject.ipynb` | Full project (executed, outputs included) |
| `FixedIncomeProject.pdf` | PDF export of the notebook |
| `FI_library.py` | Payment-schedule helper (`get_schedule_dataframe`) |

## Running it

The market data file `InputData2025.xlsx` (sheets `6m-zero-curve` and `cap-vol`) comes from a commercial data provider and is not redistributed. Place it in `data/` to rerun the notebook.

```bash
pip install numpy pandas scipy matplotlib QuantLib openpyxl
```

## Authors

Leonardo Maffei, Mattia Vizzino.
