# Data and Code Availability – EPOCH-ALPS project

This repository contains all datasets and analysis scripts supporting the results presented in the manuscript:

**"Glacier melt as a source of legacy mercury: Implications for ecosystem recovery and environmental trends"**  
Submitted to *Environmental Science & Technology* (2025).

All materials are provided under open access via Zenodo and are organized as follows:

## Repository Structure

The repository is structured into two main folders:

- `Data/`  
  Contains all raw and processed datasets used in the study. This includes sediment core analysis, glacier mass balance, emissions, and dating results.

- `Figure/`  
  Contains Python scripts used to generate the figures presented in the manuscript. These scripts directly load and process data from the `data/` folder to produce the analysis and visualizations.

## Data Folder Contents

Within the `data/` folder, you will find the following key files and subfolders:

- **Subfolders:**  
  - `210_Pb_dating/`  
    Data related to 210Pb radiometric dating used to establish sediment core chronologies with serac R package [https://github.com/rosalieb/serac]. The final results are in `Age.xlsx`  

  - `FT-IR_ATR/`  
    Raw spectra and processed results from Fourier-transform infrared spectroscopy (FT-IR) Attenuated Total Reflectance analyses. More info in the dedicated `FT-IR.md` file

- **Excel Data Files:**  
  - `DBD.xlsx`  
    Dry bulk density measurements from sediment cores.  
  - `european_Hg_emission.xlsx`  
    Historical European mercury emission inventories used for comparison.  
  - `Hg_lake.xlsx`  
    Mercury concentration and flux data for *Luitel Lake and Montcortes Lake*.  
  - `Hg.xlsx`  
    Mercury (Hg) concentration data from sediment cores.  
  - `HgAR.xlsx`  
    Calculated mercury accumulation rates (Hg AR) based on sediment data.  
  - `LOI.xlsx`  
    Loss on Ignition data at 550 °C and 950 °C, proxies for organic matter and carbonates.  
  - `mass_balance_glacier.xlsx`  
    Glacier mass balance data from the study region, used to link glacial melt to mercury mobilization.  
  - `X_ray.xlsx`  
    X-ray fluorescence data and CLRs calculation.

- **Python Script:**  
  - `HgAR_calc.py`  
    Script that reads sediment and density data to calculate mercury accumulation rates, saving results to `HgAR.xlsx`.

## Figure Folder Contents

The `figure/` folder contains subfolders and Python scripts organized by figure or analysis type:

- `carbonate_analysis/`  
  Data and scripts related to carbonate content and its geochemical proxies in sediment cores.

- `correlation_matrices/`  
  Python scripts and datasets used to compute and visualize correlation matrices for sediment core variables from Grand Lac (GDL) and Eychauda (EYC), including supplementary figures.

- `erosion_proxy_analysis/`  
  Analysis of erosion-related proxies and their relationship to mercury cycling in alpine lake sediments.

- `figure_2/`  
  Python script(s) to generate Figure 2 of the manuscript.

- `figure_3/`  
  Python script(s) to generate Figure 3, including comparisons between high-resolution and low-resolution datasets.

- `hg_vs_loi_analysis/`  
  Scripts and data supporting the analysis of the relationship between mercury concentrations and Loss on Ignition (LOI), including linear regression and supplementary figure generation.

Each folder contains scripts that directly load the relevant data from the `data/` folder, perform analyses, and generate publication-quality figures.

---

## Citation

If you use these data or scripts, please cite the associated publication and the Zenodo DOI:

> Mattio, D. et al. (2025). *Glacier melt as a source of legacy mercury: Implications for ecosystem recovery and environmental trends.* Environmental Science & Technology. DOI: [doi-link]  
> Zenodo Repository: [https://doi.org/10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX)

## Contact

For questions or further information, please contact:  
**Davide Mattio**  
IGE – Institut des Géosciences de l’Environnement, Grenoble  
📧 davide.mattio@univ-grenoble-alpes.fr