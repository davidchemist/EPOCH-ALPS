# FT-IR ATR Data and Workflow

This folder hosts the raw and processed Fourier-Transform Infrared (FT-IR) Attenuated Total Reflectance (ATR) spectra for the two sediment cores analysed in the study—Lac de l’Eychauda (EYC) and Grand Lac (GDL)—together with the Orange workflows used to perform multivariate analyses.

## Directory Layout

```
FT-IR_ATR/
├── EYC/
│   ├── input_EYC.csv             # Raw absorbance spectra
│   ├── data_analysis_EYC.ows     # Orange workflow for FT-IR processing and PCA
│   ├── PCA_loadings_EYC.xlsx     # Principal-component loadings exported by Orange
│   └── PCA_scores_EYC.xlsx       # Principal-component scores exported by Orange
├── GDL/
│   ├── input_GDL.csv
│   ├── data_analysis_GDL.ows
│   ├── PCA_loadings_GDL.xlsx
│   └── PCA_scores_GDL.xlsx
└── FT-IR_ATR.xlsx                # Consolidated key results from both cores
```

## Orange Workflow

Each `.ows` file contains an identical pipeline built in **Orange 3.38.1**:

1. **File** widget imports `input_<core>.csv`.
2. **Preprocess** widget applies a *Baseline Correction*
3. **PCA** widget performs Principal Component Analysis (auto-scaled; components with eigenvalue ≥ 1 retained).
4. **Save Data** widgets export:
   - `PCA_loadings_<core>.xlsx`
   - `PCA_scores_<core>.xlsx`


## Consolidated Spreadsheet

The file `FT-IR_ATR.xlsx` brings together the essential outputs from both cores:

| Sheet | Content |
|-------|---------|
| `EYC_loading` | PCA loadings (from `PCA_loadings_EYC.xlsx`) |
| `EYC_scores` | PCA scores (from `PCA_scores_EYC.xlsx`) |
| `GDL_loading` | PCA loadings (from `PCA_loadings_GDL.xlsx`) |
| `GDL_scores` | PCA scores (from `PCA_scores_GDL.xlsx`) |

## How to Reproduce

1. Download and install **Orange ≥ 3.38.1**: via **Anaconda Navigator**
2. Open `data_analysis_EYC.ows` or `data_analysis_GDL.ows`.
3. Ensure the **File** widget correctly links to `input_<core>.csv`.
4. Click **Run > Run All** to execute the workflow.
5. The output files (`PCA_loadings_<core>.xlsx` and `PCA_scores_<core>.xlsx`) will be updated automatically.

---

**Contact:**  
Davide Mattio  
IGE – Institut des Géosciences de l’Environnement, Grenoble  
📧 davide.mattio@univ-grenoble-alpes.fr
