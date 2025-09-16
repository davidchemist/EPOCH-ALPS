#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 10:25:00 2025

@author: Davide Mattio

"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os
from pathlib import Path
from scipy.interpolate import interp1d

if __name__ == "__main__":
    # Define directories relative to script location
    current_dir = Path(__file__).resolve().parent
    base_dir = current_dir.parent.parent
    data_dir = base_dir / "Data"

    # Define file paths
    hg_file = data_dir / "HgAR.xlsx"
    age_file = data_dir / "210_Pb_dating" / "Age.xlsx"
    emission_file = data_dir / "european_Hg_emission.xlsx"
    xray_file = data_dir / "X_ray.xlsx"
    hg_conc_file = data_dir / "Hg.xlsx"
    loi_file = data_dir / "LOI.xlsx"
    delta_file = data_dir / "C_total_delta13C.xlsx"
    glacier_file = data_dir / "mass_balance_glacier.xlsx"
    ftir_file = data_dir / "FT-IR_ATR" / "FT-IR_ATR.xlsx"

    # Debug paths
    print("Looking for HgAR file at:", hg_file)
    print("Looking for Age file at:", age_file)
    print("Looking for European Hg emission file at:", emission_file)
    
    # Check existence
    if not hg_file.exists():
        raise FileNotFoundError(f"HgAR file not found at: {hg_file}")
    if not age_file.exists():
        raise FileNotFoundError(f"Age file not found at: {age_file}")
    if not emission_file.exists():
        raise FileNotFoundError(f"European Hg emission file not found at: {emission_file}")

    # === Load and process data ===

    # Load mercury flux data, age models, and European emissions
    data = pd.read_excel(hg_file)
    age_data = pd.read_excel(age_file)
    emission_data = pd.read_excel(emission_file)

    # Normalize Hg fluxes relative to selected reference points
    norm_flux_GDL = data['Hg_AR_GDL'] / data.at[20, 'Hg_AR_GDL']
    norm_flux_EYC = data['Hg_AR_EYC'] / data.at[17, 'Hg_AR_EYC']

    # Normalize uncertainties accordingly
    err_flux_GDL = data['Err_GDL'] / data['Hg_AR_GDL'] * norm_flux_GDL
    err_flux_EYC = data['Err_EYC'] / data['Hg_AR_EYC'] * norm_flux_EYC
    
    # Read the required columns from other files
    fe_data = pd.read_excel(xray_file, usecols=["Age_X_EYC", "CLR_Fe", "CLR_Ti"])
    hg_data = pd.read_excel(hg_conc_file, usecols=["Hg_conc_EYC", "RSD_EYC"])
    loi_data = pd.read_excel(loi_file, usecols=["LOI_550_EYC", "LOI_950_EYC"])
    delta_data = pd.read_excel(delta_file, usecols=["C_total", "delta_13_C"])
    glacier_data = pd.read_excel(glacier_file)
    pca_data = pd.read_excel(ftir_file, sheet_name="EYC_loadings", usecols=["PC2_ord", "sCp3"])

    # === Extract and smooth data ===
    age = age_data["age_EYC"]
    err_age = age_data["err_age_GDL"]
    age_x = fe_data["Age_X_EYC"]
    Fe = fe_data["CLR_Fe"]
    Fe_smoothed = pd.Series(Fe).rolling(window=10, center=True).mean()
    Ti = fe_data["CLR_Ti"]
    Ti_smoothed = pd.Series(Ti).rolling(window=10, center=True).mean()

    Hg = hg_data["Hg_conc_EYC"]
    RSD = hg_data["RSD_EYC"]
    Hg_err = Hg * RSD

    LOI_550 = loi_data["LOI_550_EYC"] * 100
    LOI_550[24] = np.nan
    LOI_950 = loi_data["LOI_950_EYC"] * 100
    PC2 = pd.concat([pca_data["PC2_ord"], pd.Series([np.nan] * 5)], ignore_index=True)
    sCp3 = pd.concat([pca_data["sCp3"], pd.Series([np.nan] * 5)], ignore_index=True)
    C_total = delta_data["C_total"] * 100
    C_total = np.append(C_total, [np.nan]*6)
    delta_13_C= np.append(delta_data["delta_13_C"], [np.nan]*6)
    
    # Select the first 20 values
    x = delta_13_C[:25]
    y = age[:25]

    # --- Linear regression for trendline (effect of Suess) ---
    coeffs = np.polyfit(y, x, 1)  # fit x = m*y + b
    trendline = np.poly1d(coeffs)
    
    y_trend= trendline(y) 

    n = 3
    SOR_rolling = glacier_data['Bilan_SOR'].rolling(window=n).mean()
    SAR_rolling = glacier_data['Bilan_SAR'].rolling(window=n).mean()
    SEG_rolling = glacier_data['Bilan_SEG'].rolling(window=n).mean()
    Huss_rolling = glacier_data['Bilan_Huss'].rolling(window=n).mean()

    # === Font and style settings for uniform look ===
    label_fontsize = 12
    tick_fontsize = 10
    legend_fontsize = 10
    panel_label_fontsize = 14


import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.interpolate import interp1d

# --- Figure 1: three panels ---
fig1, axs1 = plt.subplots(1, 4, figsize=(16, 7), sharey=True,
                          gridspec_kw={'wspace': 0.05, 'width_ratios':[2,0.7,2,0.7]}, constrained_layout=True)

for ax in axs1:
    ax.set_ylim(1900, 2025)

# --- PANEL (a): Hg and LOI 950°C ---
axs1[0].axhspan(1942, 1949, color='#E0E0E0', alpha=1)  # Highlight key period
axs1[0].plot(Hg, age, color='#0b3d91', lw=2, label='Hg concentration')  # Hg curve
axs1[0].fill_betweenx(age, Hg - Hg_err, Hg + Hg_err, color='#90E0EF', alpha=0.3)  # Error band
axs1[0].set_xlabel('THg (ng g$^{-1}$)', color='#0b3d91', fontsize=label_fontsize)
axs1[0].tick_params(axis='x', colors='#0b3d91', labelsize=tick_fontsize)
axs1[0].grid(True, linestyle='--', alpha=0.3)
axs1[0].xaxis.set_major_locator(mticker.MultipleLocator(10))
axs1[0].xaxis.set_minor_locator(mticker.MultipleLocator(5))
axs1[0].axhline(1970, linestyle='--', linewidth=2, color='black', alpha=0.7)
axs1[0].text(0.95, 0.02, '(a)', transform=axs1[0].transAxes,
             fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')

# Twin axis for LOI 950
ax0b = axs1[0].twiny()
ax0b.plot(LOI_950, age, color='tab:brown', lw=2, label='LOI 950°C')
ax0b.set_xlabel('Carbonate content (%)', color='tab:brown', fontsize=label_fontsize)
ax0b.tick_params(axis='x', colors='tab:brown', labelsize=tick_fontsize)
ax0b.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))

# Combine legends
h1, l1 = axs1[0].get_legend_handles_labels()
h2, l2 = ax0b.get_legend_handles_labels()
axs1[0].legend(h1 + h2, l1 + l2, loc='lower left', fontsize=legend_fontsize)

# --- PANEL (b): PCA sCP3 vs Age (trestto) ---
axs1[1].plot(sCp3, age, color='tab:purple', lw=2, label='sCP3')
axs1[1].set_xlabel('sCp3', fontsize=label_fontsize)
axs1[1].grid(True, linestyle='--', alpha=0.3)
axs1[1].text(0.95, 0.02, '(b)', transform=axs1[1].transAxes,
             fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')
axs1[1].legend(fontsize=legend_fontsize)

# # --- PANEL (c): Hg and LOI 550°C + CLR Fe ---
# axs1[2].axhspan(1942, 1949, color='#E0E0E0', alpha=1)
# axs1[2].plot(Hg, age, color='#0b3d91', lw=2, label='Hg concentration')
# axs1[2].fill_betweenx(age, Hg - Hg_err, Hg + Hg_err, color='#90E0EF', alpha=0.3)
# axs1[2].set_xlabel('THg (ng g$^{-1}$)', color='#0b3d91', fontsize=label_fontsize)
# axs1[2].tick_params(axis='x', colors='#0b3d91', labelsize=tick_fontsize)
# axs1[2].grid(True, linestyle='--', alpha=0.3)
# axs1[2].xaxis.set_major_locator(mticker.MultipleLocator(10))
# axs1[2].xaxis.set_minor_locator(mticker.MultipleLocator(5))
# axs1[2].axhline(1970, linestyle='--', linewidth=2, color='black', alpha=0.7)
# axs1[2].text(0.95, 0.02, '(c)', transform=axs1[2].transAxes,
#              fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')


# # Twin axis for LOI 550
#  ax2b = axs1[2].twiny()
#  ax2b.plot(C_total, age, color='tab:green', lw=2, label='C total (%)')
#  ax2b.set_xlabel('C total (%)', color='tab:green', fontsize=label_fontsize)
#  ax2b.tick_params(axis='x', colors='tab:green', labelsize=tick_fontsize)
#  ax2b.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
#  ax2b.set_xlim(0.1, 0.5)


# # Twin axis for CLR Fe
# ax2c = axs1[2].twiny()
# ax2c.plot(Fe_smoothed, age_x, color='tab:red', lw=2, label='CLR Fe')
# ax2c.set_xlabel('CLR Fe', color='tab:red', fontsize=label_fontsize)
# ax2c.tick_params(axis='x', colors='tab:red', labelsize=tick_fontsize)
# ax2c.spines["top"].set_position(("axes", 1.15))
# ax2c.set_xlim(1.8, 2.3)

# # Combine legends for panel c
# h1, l1 = axs1[2].get_legend_handles_labels()
# h2, l2 = ax2b.get_legend_handles_labels()
# h3, l3 = ax2c.get_legend_handles_labels()
# axs1[2].legend(h1 + h2 + h3, l1 + l2 +l3, loc='best', fontsize=legend_fontsize)

# --- PANEL (c): C_total (asse principale) + Fe (asse gemello) ---

# Plot C_total on main axis
axs1[2].plot(C_total, age, color='tab:green', lw=2, label='C total (%)')
axs1[2].set_xlabel('C total (%)', color='tab:green', fontsize=label_fontsize)
axs1[2].tick_params(axis='x', colors='tab:green', labelsize=tick_fontsize)
axs1[2].grid(True, linestyle='--', alpha=0.3)

# Axis label and panel label
axs1[2].text(0.95, 0.02, '(c)', transform=axs1[2].transAxes,
             fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')
#axs1[2].set_ylabel('Age (years)', fontsize=label_fontsize)
axs1[2].tick_params(axis='y', labelsize=tick_fontsize)

# Twin axis for CLR Fe
ax2b = axs1[2].twiny()
ax2b.plot(Fe_smoothed, age_x, color='tab:red', lw=2, label='CLR Fe')
ax2b.set_xlabel('CLR Fe', color='tab:red', fontsize=label_fontsize)
ax2b.tick_params(axis='x', colors='tab:red', labelsize=tick_fontsize)
ax2b.spines["top"].set_position(("axes", 1))
ax2b.set_xlim(1.8, 2.3)

# Combine legends
h1, l1 = axs1[2].get_legend_handles_labels()
h2, l2 = ax2b.get_legend_handles_labels()
axs1[2].legend(h1 + h2, l1 + l2, loc='best', fontsize=legend_fontsize)



# --- PANEL (d)): PCA sCP3 vs Age (trestto) ---
axs1[3].plot(delta_13_C[:25], age[:25], color='tab:orange', lw=2, label='$\delta^{13}$C')
axs1[3].plot(y_trend, y, color='tab:red', lw=2, linestyle='--', label='Suess\n effect')
axs1[3].set_xlabel('$\delta^{13}$C', fontsize=label_fontsize)
axs1[3].grid(True, linestyle='--', alpha=0.3)
axs1[3].text(0.95, 0.02, '(d)', transform=axs1[3].transAxes,
             fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')
axs1[3].set_xlim(-26,-23)
axs1[3].legend(fontsize=legend_fontsize)

# --- Shared Y-axis label ---
axs1[0].set_ylabel('Age (years)', fontsize=label_fontsize)
for ax in axs1:
    ax.tick_params(axis='y', labelsize=tick_fontsize)

# --- Save figure ---
fig1.savefig('Figure_Hg_LOI_PCA.png', dpi=300)
plt.show()


# --- FIGURE 2: Panels (a) and (b) ---
fig2, axs2 = plt.subplots(1, 2, figsize=(14, 7), sharey=True, gridspec_kw={'wspace': 0.075}, constrained_layout=True)

# --- PANEL (a): Glacier mass balance ---
axs2[0].plot(SEG_rolling, glacier_data['Age_SEG'], linestyle='-', linewidth=3, color='tab:red', label='Segurét Foran Glacier')
axs2[0].plot(SOR_rolling, glacier_data['Age_SOR'], linestyle='-', linewidth=1, color='tab:blue', label='Saint Sorlin Glacier')
axs2[0].plot(Huss_rolling, glacier_data['Age_Huss'], linestyle='-', linewidth=1, color='tab:green', label='European average')
axs2[0].set_xlabel('Mass balance (m w.e.)', fontsize=label_fontsize)
axs2[0].grid(True, linestyle='--', alpha=0.3)
axs2[0].axhspan(1942, 1949, color='#E0E0E0', alpha=1)
axs2[0].axhline(1970, linestyle='--', linewidth=2, color='black', alpha=0.7)
axs2[0].legend(loc='lower left', fontsize=legend_fontsize)
axs2[0].text(0.95, 0.02, '(a)', transform=axs2[0].transAxes, fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')
axs2[0].tick_params(axis='x', labelsize=tick_fontsize)

# --- PANEL (d): Normalized Hg AR flux with error bands ---
axs2[1].axhspan(1942, 1949, color='#E0E0E0', alpha=1)
axs2[1].plot(norm_flux_EYC, age_data['age_EYC'], color='tab:blue', linewidth=2, label='EYC')
axs2[1].fill_betweenx(age_data['age_EYC'],
                      norm_flux_EYC - err_flux_EYC,
                      norm_flux_EYC + err_flux_EYC,
                      color='tab:blue', alpha=0.3)
axs2[1].plot(norm_flux_EYC, age_data['age_EYC'], 'o', color='tab:blue', markersize=5)

axs2[1].plot(norm_flux_GDL, age_data['age_GDL'], color='tab:brown', linewidth=2, label='GDL')
axs2[1].fill_betweenx(age_data['age_GDL'],
                      norm_flux_GDL - err_flux_GDL,
                      norm_flux_GDL + err_flux_GDL,
                      color='tab:brown', alpha=0.3)
axs2[1].plot(norm_flux_GDL, age_data['age_GDL'], 'o', color='tab:brown', markersize=5)

axs2[1].set_xlabel('Normalized Hg AR', fontsize=label_fontsize)
axs2[1].set_xlim(0.4, 1.7)
axs2[1].set_ylim(1900, 2025)
axs2[1].set_yticks(range(1900, 2025, 20))
axs2[1].tick_params(axis='x', labelsize=tick_fontsize)
axs2[1].grid(True, linestyle='--', alpha=0.3)
axs2[1].legend(loc='best', fontsize=legend_fontsize)
axs2[1].text(0.95, 0.02, '(b)', transform=axs2[1].transAxes, fontsize=panel_label_fontsize, ha='right', va='bottom', fontweight='bold')

# Highlight climate penalty area
mask_eyc = (age_data['age_EYC'] >= 1970) & (age_data['age_EYC'] <= 2023)
age_eyc_masked = age_data['age_EYC'][mask_eyc]
norm_EYC_masked = norm_flux_EYC[mask_eyc]
interp_GDL = interp1d(age_data['age_GDL'], norm_flux_GDL, bounds_error=False, fill_value="extrapolate")
norm_GDL_interp = interp_GDL(age_eyc_masked)
lower = np.minimum(norm_EYC_masked, norm_GDL_interp)
upper = np.maximum(norm_EYC_masked, norm_GDL_interp)
axs2[1].fill_betweenx(age_eyc_masked, lower, upper, color='tab:orange', alpha=0.3, label='Climate penalty')
axs2[1].legend(loc='best', fontsize=legend_fontsize)

# Shared Y-axis label
axs2[0].set_ylabel('Age (years)', fontsize=label_fontsize)
axs2[0].tick_params(axis='y', labelsize=tick_fontsize)
axs2[1].tick_params(axis='y', labelsize=tick_fontsize)

# Save second figure
fig2.savefig('Figure_Glacier_HgAR.png', dpi=500)
plt.show()