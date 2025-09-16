# Erosion Proxy Analysis – README


This script (`erosion_proxy_analysis.py`) generates a nine-panel scatter-plot matrix that explores the relationship between sediment-core geochemical proxies (centered-log-ratio, CLR, element intensities) and total mercury (THg) concentrations in the Eychauda (EYC) core.  
It also exports an intermediate, depth-averaged dataset (`processed_data.xlsx`) that can be reused for supplementary analyses.

> **Why this script?**  
> It provides the **simplest workflow to run linear regressions on variables sampled at different vertical resolutions**—low-resolution THg versus high-resolution XRF elemental scans—by automatically averaging the high-resolution data within each THg depth interval before fitting the models.

---

## 1. What the script does  

1. **Load input data**  
   * Reads `data_graph.xlsx`, which must contain:
   ```text
   Age_X_EYC   # depth (cm) or age assigned to X‑ray data rows
   Age_EYC     # depth (cm) or age for Hg measurements
   Hg_EYC      # Hg concentration (ng g⁻¹)
   CLR_Al, CLR_Si, …, CLR_Sr   # nine CLR‑transformed element intensities
   ```
2. **Depth aggregation** (`aggregate_core_scan`)  
   * For every pair of consecutive Hg depths, averages the CLR element values that fall in the same depth interval.  
   * Returns a tidy table with one row per Hg measurement.
3. **Save aggregated data**  
   * Writes the table to `processed_data.xlsx`.
4. **Plot regression sub‑plots** (`plot_regression_subplots`)  
   * Creates a 3×3 grid of scatter plots (CLR element vs. Hg).  
   * Performs ordinary‑least‑squares regression for each element.  
   * Colours points by core age, annotates each subplot with *R²* and *p*-value, and highlights strong fits in red.  
   * Saves the figure as `erosion.pdf` (vector) and `erosion.png` (high‑resolution).

---


## 2. Output files

| File                | Purpose                                                                                           |
|---------------------|---------------------------------------------------------------------------------------------------|
| `processed_data.xlsx` | Depth‑averaged dataset (Hg, mean CLR elements, midpoint depth). |
| `erosion.pdf`       | Publication‑quality figure (vector, editable).                                                    |
| `erosion.png`       | High‑resolution raster for quick viewing.                                             |

---