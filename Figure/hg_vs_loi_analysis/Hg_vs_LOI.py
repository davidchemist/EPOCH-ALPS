# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:49:41 2025

@author: david_chemist
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.stats import linregress
from pathlib import Path
import sys

def main():
    current_dir = Path(__file__).resolve().parent
    base_dir = current_dir.parent.parent
    data_dir = base_dir / "Data"
    
    # Define file paths
    hg_conc_file = data_dir / "Hg.xlsx"
    loi_file = data_dir / "LOI.xlsx"
    age_file = data_dir / "210_Pb_dating" / "Age.xlsx"

    # Check if files exist
    for f in [hg_conc_file, loi_file, age_file]:
        if not f.exists():
            print(f"File non trovato: {f}", file=sys.stderr)
            sys.exit(1)
    
    # Load data
    hg_data = pd.read_excel(hg_conc_file)
    loi_data = pd.read_excel(loi_file)
    age_data = pd.read_excel(age_file)
    
    # Controllo colonne esatte (adatta nomi colonne se serve)
    # Qui assumo che hg_data abbia colonna "Hg_conc_GDL"
    # loi_data abbia colonna "LOI_550_GDL"
    # age_data abbia colonna "age_GDL"
    
    # Unisci i dataframe per sincronizzare gli indici e rimuovere eventuali NaN
    df = pd.DataFrame({
        "Hg": hg_data["Hg_conc_GDL"],
        "LOI_550": loi_data["LOI_550_GDL"],
        "Age": age_data["age_GDL"]
    }).dropna()
    
    print(f"Dati caricati: {len(df)} righe utilizzabili")
    
    # Preparo i dati per la regressione
    x = df["LOI_550"].values.reshape(-1,1)
    y = df["Hg"].values
    colors = df["Age"].values
    
    # Fit modello lineare
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    
    # Calcolo R^2
    r2 = r2_score(y, y_pred)
    
    # Calcolo slope e p-value con linregress
    slope, intercept, r_value, p_value, stderr = linregress(x.flatten(), y)
    
    print(f"Regressione lineare: slope = {slope:.4f}, intercept = {intercept:.4f}")
    print(f"R^2 = {r2:.4f}, p-value = {p_value:.4g}")
    
    # Plot
    plt.figure(figsize=(8,6))
    scatter = plt.scatter(x.flatten(), y, c=colors, cmap="viridis", edgecolor='k')
    plt.plot(x, y_pred, 'k-', linewidth=2, label=f'$R^2$ = {r2:.3f}\n$p$ = {p_value:.3g}')
    plt.xlabel("LOI 550 (g/g)")
    plt.ylabel("THg (ng/g)")
    plt.title("GDL")
    plt.legend()
    
    cbar = plt.colorbar(scatter)
    cbar.set_label("Age")
    
    plt.tight_layout()
    plt.savefig("Hg_vs_LOI_GDL.pdf", bbox_inches='tight', pad_inches=0.2)
    plt.savefig("Hg_vs_LOI_GDL.png", bbox_inches='tight', pad_inches=0.2, dpi=500)
    plt.show()

if __name__ == "__main__":
    main()