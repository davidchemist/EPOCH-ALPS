#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 15:02:58 2025

@author: mattiod
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 14:52:00 2025

@author: mattiod
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.font_manager import FontProperties
import os
from pathlib import Path
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

plt.rcParams.update({'axes.labelsize': 14, 'xtick.labelsize': 12, 'ytick.labelsize': 12})
italic_font = FontProperties(style='italic')


# Define color palettes
dark_blue = '#0b3d91'  # un blu scuro (più scuro di tab:blue)
dark_brown = '#4b2e05'  # un marrone scuro (più scuro di tab:brown)

# === Path to the data folder ===
data_dir = r"/Users/mattiod/Desktop/EPOCH-ALPS/Article/Data availbility statement/Data"

# === Load age data ===
age_data = pd.read_excel(os.path.join(data_dir, "210_Pb_dating", "Age.xlsx"))
age_eyc = age_data["age_EYC"]
age_gdl = age_data["age_GDL"]

# === Load Hg concentration data ===
hg = pd.read_excel(os.path.join(data_dir, "Hg.xlsx"))
hg_ar = pd.read_excel(os.path.join(data_dir, "HgAR.xlsx"))

# === Extract Hg and error columns ===
Hg_EYC = hg["Hg_conc_EYC"]
RSD_EYC = hg["RSD_EYC"]
Hg_GDL = hg["Hg_conc_GDL"]
RSD_GDL = hg["RSD_GDL"]
Depth_EYC=hg["Depth_EYC"]
Depth_GDL=hg["Depth_GDL"]


HgAR_EYC = hg_ar["Hg_AR_EYC"]
HgAR_EYC_err = hg_ar["Err_EYC"]
HgAR_GDL = hg_ar["Hg_AR_GDL"]
HgAR_GDL_err = hg_ar["Err_GDL"]

Hg_EYC_err = RSD_EYC * Hg_EYC 
Hg_GDL_err = RSD_GDL * Hg_GDL


def load_and_normalize_multilake_data(gdl_flux_file, gdl_age_file, lake_file, emission_file):
    """
    Load Hg fluxes for GDL and other lakes, normalize to 1940–1945 average.
    Returns fluxes, ages, normalized errors (only for GDL), and emissions.
    """
    gdl_flux_data = pd.read_excel(gdl_flux_file)
    gdl_age_data = pd.read_excel(gdl_age_file)
    lake_data = pd.read_excel(lake_file)
    emission_data = pd.read_excel(emission_file)

    lakes = ['GDL', 'Lui', 'Mont']
    flux_dict = {}
    age_dict = {}

    for lake in lakes:
        if lake == 'GDL':
            flux = gdl_flux_data['Hg_AR_GDL']
            age = gdl_age_data['age_GDL']
            error = gdl_flux_data['Err_GDL']

            ref = flux.max()
            norm_flux = flux / ref
            norm_error = error / flux * norm_flux

            flux_dict[lake] = norm_flux
            age_dict[lake] = age
            gdl_error = norm_error

        else:
            flux_col = f'Flux_{lake}'
            age_col = f'Age_{lake}'
            flux = lake_data[flux_col]
            age = lake_data[age_col]

            ref = flux.max()
            norm_flux = flux / ref

            flux_dict[lake] = norm_flux
            age_dict[lake] = age

    return flux_dict, age_dict, gdl_error, emission_data


if __name__ == "__main__":
    # === Define paths ===
    base_dir = Path(__file__).resolve().parent.parent
    gdl_flux_file = base_dir.parent / "Data" / "HgAR.xlsx"
    gdl_age_file = base_dir.parent/ "Data" / "210_Pb_dating" / "Age.xlsx"
    lake_file = base_dir.parent / "Data" / "Hg_lake.xlsx"
    emission_file = base_dir.parent / "Data" / "european_Hg_emission.xlsx"

    # === Load additional data ===
    flux_dict, age_dict, gdl_error, emission_data = load_and_normalize_multilake_data(
        gdl_flux_file, gdl_age_file, lake_file, emission_file
    )

    # === Font and style settings for uniform look ===
    label_fontsize = 12
    tick_fontsize = 10
    legend_fontsize = 10
    panel_label_fontsize = 14
    dark_brown = '#654321' # Segnaposto per il colore
    dark_blue = '#00008B'   # Segnaposto per il colore
    
    # Segnaposto per il font corsivo. Se hai una tua definizione, usa quella.
    italic_font = FontProperties(style='italic')
    
    
   # === Create the figure with two panels ===
    fig, axs = plt.subplots(1, 2, figsize=(10, 6), sharey=False,
                            gridspec_kw={'wspace': 0.075}, constrained_layout=True)
    
    # === PANEL (a): Grand Lake ===
    axs[0].plot(Hg_GDL, Depth_GDL, color=dark_brown, lw=2, linestyle='--', label='Concentration')
    axs[0].invert_yaxis()  # Invert Y axis: depth increases downward
    axs[0].set_xlabel('THg (ng g$^{-1}$)', color=dark_brown, fontsize=label_fontsize)
    axs[0].set_ylabel('Depth (cm)', fontsize=label_fontsize)
    axs[0].tick_params(axis='x', colors=dark_brown, labelsize=tick_fontsize)
    axs[0].tick_params(axis='y', labelsize=tick_fontsize)
    axs[0].grid(True, linestyle='--', alpha=0.3)
    axs[0].set_ylim(200, 0)
    
    axs[0].xaxis.set_major_locator(ticker.MultipleLocator(50))
    axs[0].xaxis.set_minor_locator(ticker.MultipleLocator(25))
    
    # Twin X-axis: Hg Accumulation Rate
    ax0b = axs[0].twiny()
    ax0b.plot(HgAR_GDL, Depth_GDL, color='tab:brown', lw=3, label='Accumulation Rate')
    ax0b.set_xlabel(r'Hg AR ($\mu$g m$^{-2}$ y$^{-1}$)', color='tab:brown', fontsize=label_fontsize)
    ax0b.tick_params(axis='x', colors='tab:brown', labelsize=tick_fontsize)
    
    ax0b.xaxis.set_major_locator(ticker.MultipleLocator(50))
    ax0b.xaxis.set_minor_locator(ticker.MultipleLocator(25))
    
    # Legend and label
    legend_elements_gdl = [
        Line2D([0], [0], color=dark_brown, lw=2, linestyle='--', label='Concentration'),
        Line2D([0], [0], color='tab:brown', lw=3, label='Accumulation Rate')
    ]
    axs[0].legend(handles=legend_elements_gdl, loc='upper right',
                  title='Grand Lake', title_fontproperties=italic_font,
                  fontsize=legend_fontsize, framealpha=0.9)
    axs[0].text(0.95, 0.02, '(a)', transform=axs[0].transAxes,
                fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')
    
    # === PANEL (b): Eychauda ===
    axs[1].plot(Hg_EYC, Depth_EYC, color=dark_blue, lw=2, linestyle='--', label='Concentration')
    axs[1].invert_yaxis()
    axs[1].set_xlabel('THg (ng g$^{-1}$)', color=dark_blue, fontsize=label_fontsize)
    axs[1].tick_params(axis='x', colors=dark_blue, labelsize=tick_fontsize)
    axs[1].tick_params(axis='y', labelsize=tick_fontsize)
    axs[1].grid(True, linestyle='--', alpha=0.3)
    axs[1].set_ylim(350, 0)
    
    axs[1].xaxis.set_major_locator(ticker.MultipleLocator(10))
    axs[1].xaxis.set_minor_locator(ticker.MultipleLocator(5))
    
    # Twin X-axis for accumulation rate
    ax1b = axs[1].twiny()
    ax1b.plot(HgAR_EYC, Depth_EYC, color='tab:blue', lw=3, label='Accumulation Rate')
    ax1b.set_xlabel(r'Hg AR ($\mu$g m$^{-2}$ y$^{-1}$)', color='tab:blue', fontsize=label_fontsize)
    ax1b.tick_params(axis='x', colors='tab:blue', labelsize=tick_fontsize)
    
    ax1b.xaxis.set_major_locator(ticker.MultipleLocator(50))
    ax1b.xaxis.set_minor_locator(ticker.MultipleLocator(25))
    
    # Legend and label
    legend_elements_eyc = [
        Line2D([0], [0], color=dark_blue, lw=2, linestyle='--', label='Concentration'),
        Line2D([0], [0], color='tab:blue', lw=3, label='Accumulation Rate')
    ]
    axs[1].legend(handles=legend_elements_eyc, loc='upper left',
                  title='Eychauda Lake', title_fontproperties=italic_font,
                  fontsize=legend_fontsize, framealpha=0.9)
    axs[1].text(0.95, 0.02, '(b)', transform=axs[1].transAxes,
                fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')
    
    
    # === Save and show figure ===
    plt.savefig('Figure_depth.pdf', bbox_inches='tight', pad_inches=0.2)
    plt.savefig('Figure_depth.png', bbox_inches='tight', pad_inches=0.2, dpi=1000)
    plt.show()