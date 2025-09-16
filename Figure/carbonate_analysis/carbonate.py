#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:23:09 2025
@author: Davide Mattio

This script creates a multi-panel figure to compare THg concentrations with 
FTIR-based carbonate proxy (PC2) and LOI950, using FTIR, Hg, and LOI datasets.
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from pathlib import Path

# === Set up directories ===
script_dir = Path(__file__).resolve().parent
base_dir = script_dir.parents[1] / "Data"
figure_dir = script_dir  # same folder as script, or change to a dedicated 'Figure_4' folder

# === Define input file paths ===
ftir_file = base_dir / "FT-IR_ATR" / "FT-IR_ATR.xlsx"
hg_file = base_dir / "HgAR.xlsx"
loi_file = base_dir / "LOI.xlsx"
age_file = base_dir / "210_Pb_dating" / "Age.xlsx"

# === Load datasets ===
ftir_scores = pd.read_excel(ftir_file, sheet_name="EYC_scores")
ftir_loadings = pd.read_excel(ftir_file, sheet_name="EYC_loadings")
hg_data = pd.read_excel(hg_file)
loi_data = pd.read_excel(loi_file)
age_data = pd.read_excel(age_file)

# === Column names ===
eyc_columns = [f"EYC23-{i}" for i in range(1, 35)]
pc2_column = "PC2"
d_column = "Wave_number"
Hg_EYC = "HgAR_EYC"
PC2 = "PC2_ord"
Age_EYC = "age_EYC"
LOI950 = "LOI_950_EYC"

# === Merge into single DataFrame for regression ===
data = pd.DataFrame({
    Hg_EYC: hg_data[Hg_EYC],
    Age_EYC: age_data[Age_EYC],
    LOI950: loi_data[LOI950],
    PC2: ftir_loadings[PC2]
}).dropna()

# === Regression variables ===
x_pc2 = data[PC2].values.reshape(-1, 1)
x_loi = data[LOI950].values.reshape(-1, 1)
y_hg = data[Hg_EYC].values
colors = data[Age_EYC].values

# === Linear regressions ===
# PC2
slope_pc2, intercept_pc2, r_pc2, p_pc2, _ = linregress(x_pc2.flatten(), y_hg)
y_pred_pc2 = slope_pc2 * x_pc2 + intercept_pc2
r2_pc2 = r_pc2**2
label_pc2 = f'R² = {r2_pc2:.3f} \n$p$ = {p_pc2:.3g}'

# LOI950
slope_loi, intercept_loi, r_loi, p_loi, _ = linregress(x_loi.flatten(), y_hg)
y_pred_loi = slope_loi * x_loi + intercept_loi
r2_loi = r_loi**2
label_loi = f'R² = {r2_loi:.3f} \n$p$ = {p_loi:.3g}'

# === Plotting settings ===
plt.rc('font', size=16)
fig, axs = plt.subplots(1, 3, figsize=(21.5, 6.5), gridspec_kw={'width_ratios': [2, 1, 1]})

# --- Subplot (a): FTIR spectra ---
for col in eyc_columns:
    axs[0].plot(ftir_scores[d_column], ftir_scores[col], linestyle='-', alpha=0.5, linewidth=0.5)
axs[0].plot(ftir_scores[d_column], ftir_scores[pc2_column], linestyle='--', color='red', linewidth=2, label="PC2")

# Arrows for carbonate regions
axs[0].annotate('', xy=(1440, 3.5), xytext=(1530, 3.5),
                arrowprops=dict(facecolor='red', width=2, headwidth=10))
axs[0].annotate('', xy=(880, 2), xytext=(950, 2),
                arrowprops=dict(facecolor='red', width=2, headwidth=10))

axs[0].invert_xaxis()
axs[0].set_xlim(4000, 400)
axs[0].set_xlabel("Wave number (cm$^{-1}$)")
axs[0].set_ylabel("Absorbance units")
axs[0].grid(True)
axs[0].text(0.05, 0.07, "(a)", transform=axs[0].transAxes, fontsize=20, fontweight='bold', va='top')

# --- Subplot (b): PC2 vs THg ---
sc1 = axs[1].scatter(x_pc2, y_hg, c=colors, cmap="viridis", edgecolor='k')
axs[1].plot(x_pc2, y_pred_pc2, color='black', linewidth=2, label=label_pc2)
axs[1].set_xlabel("PC2 (carbonate proxy)")
axs[1].set_ylabel("THg (ng/g)")
axs[1].set_ylim(70, 260)
axs[1].legend()
axs[1].text(0.05, 0.07, "(b)", transform=axs[1].transAxes, fontsize=20, fontweight='bold', va='top')

# --- Subplot (c): LOI950 vs THg ---
sc2 = axs[2].scatter(x_loi, y_hg, c=colors, cmap="viridis", edgecolor='k')
axs[2].plot(x_loi, y_pred_loi, color='black', linewidth=2, label=label_loi)
axs[2].set_xlabel("LOI 950")
axs[2].set_ylim(70, 260)
axs[2].legend()
axs[2].text(0.05, 0.07, "(c)", transform=axs[2].transAxes, fontsize=20, fontweight='bold', va='top')

# --- Colorbar (shared) ---
fig.subplots_adjust(right=0.87)
cbar_ax = fig.add_axes([0.88, 0.15, 0.02, 0.7])
cbar = fig.colorbar(sc1, cax=cbar_ax)
cbar.set_label("Age")

# === Save outputs ===
figure_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(figure_dir / 'carbonate.pdf', bbox_inches='tight', pad_inches=0.2)
plt.savefig(figure_dir / 'carbonate.png', bbox_inches='tight', pad_inches=0.2, dpi=500)
plt.show()