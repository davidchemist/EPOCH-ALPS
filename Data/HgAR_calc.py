#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 23 11:57:38 2025

@author: Davide Mattio
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def calculate_HgAR_vector(Hg_conc, density, SAR, err_Hg, err_DBD, err_SAR):
    """
    Compute HgAR and its absolute error.
    
    Parameters:
    - Hg_conc: vector of mercury concentrations
    - density: vector of dry bulk density
    - SAR: scalar value of sediment accumulation rate
    - err_Hg: vector of relative standard deviation of Hg
    - err_DBD: scalar value of relative error on density (fixed at 0.05)
    - err_SAR: scalar value of relative error on SAR

    Returns:
    - HgAR: vector of Hg accumulation rates
    - abs_error: vector of absolute errors on HgAR
    """
    HgAR = Hg_conc * density * SAR * 10
    rel_error = np.sqrt(err_Hg**2 + err_DBD**2 + err_SAR**2)
    abs_error = rel_error * HgAR
    return HgAR, abs_error

def integrate_HgAR(HgAR_vector, age_vector):
    """
    Compute the area under the HgAR curve using the trapezoidal rule.

    Parameters:
    - HgAR_vector: vector of Hg accumulation rate values [µg/m²/year]
    - age_vector: vector of age values [years]

    Returns:
    - area: total accumulated Hg over time [µg/m²]
    """
    return np.trapz(HgAR_vector, x=age_vector)

def integrate_error(HgAR_err_vector, age_vector):
    """
    Compute propagated uncertainty on the integral of HgAR using the trapezoidal rule.
    
    Parameters:
    - HgAR_err_vector: vector of absolute errors on HgAR [µg/m²/yr]
    - age_vector: vector of age values [years]
    
    Returns:
    - propagated_error: standard deviation on the area [µg/m²]
    """
    error_squared_sum = 0
    for i in range(len(age_vector) - 1):
        dx = age_vector.iloc[i+1] - age_vector.iloc[i]
        dy_err_i = HgAR_err_vector.iloc[i]
        dy_err_ip1 = HgAR_err_vector.iloc[i+1]
        trapezoid_var = ((dx / 2) ** 2) * (dy_err_i**2 + dy_err_ip1**2)
        error_squared_sum += trapezoid_var
    return np.sqrt(error_squared_sum)
# Superfici dei laghi in m²
surface_GDL_m2 = 47000     # Grand Lac
surface_EYC_m2 = 100000    # Eychauda

def compute_mass(F_vector_area, err_area, lake_surface_m2):
    """
    Compute total Hg mass in sediments and its uncertainty.
    
    Parameters:
        F_vector_area (float): integrated HgAR flux [µg/m²]
        err_area (float): uncertainty on integrated flux [µg/m²]
        lake_surface_m2 (float): lake surface [m²]
        
    Returns:
        tuple: (mass in µg, uncertainty in µg)
    """
    mass = F_vector_area * lake_surface_m2
    err_mass = err_area * lake_surface_m2
    return mass, err_mass


def main():
    # === Load input data ===
    df_Hg = pd.read_excel('Hg.xlsx')
    df_DBD = pd.read_excel('DBD.xlsx')
    df_Age = pd.read_excel('210_Pb_dating/Age.xlsx')

    # === Fixed error on DBD ===
    err_DBD = 0.05

    # === Extract constant SAR values (first row) ===
    SAR_EYC = df_Age['SAR_EYC'].iloc[0]
    err_SAR_EYC = df_Age['err_SAR_EYC'].iloc[0]
    SAR_GDL = df_Age['SAR_GDL'].iloc[0]
    err_SAR_GDL = df_Age['err_SAR_GDL'].iloc[0]

    # === Compute HgAR and errors for EYC ===
    HgAR_EYC, err_EYC = calculate_HgAR_vector(
        Hg_conc = df_Hg['Hg_conc_EYC'],
        density = df_DBD['DBD_EYC'],
        SAR = SAR_EYC,
        err_Hg = df_Hg['RSD_EYC'],
        err_DBD = err_DBD,
        err_SAR = err_SAR_EYC
    )

    # === Compute HgAR and errors for GDL ===
    HgAR_GDL, err_GDL = calculate_HgAR_vector(
        Hg_conc = df_Hg['Hg_conc_GDL'],
        density = df_DBD['DBD_GDL'],
        SAR = SAR_GDL,
        err_Hg = df_Hg['RSD_GDL'],
        err_DBD = err_DBD,
        err_SAR = err_SAR_GDL
    )

    # === Extract age vectors ===
    age_EYC = df_Age['age_EYC']
    age_GDL = df_Age['age_GDL']
    
    # === Select only 1970–2023 range ===
    HgAR_EYC_sel = HgAR_EYC.iloc[0:18]     # EYC 1–18
    age_EYC_sel = age_EYC.iloc[0:18]

    HgAR_GDL_sel = HgAR_GDL.iloc[0:20]     # GDL 1–20
    age_GDL_sel = age_GDL.iloc[0:20]
    
    # === Check and reverse if needed to ensure increasing age ===
    if age_EYC_sel.iloc[0] > age_EYC_sel.iloc[-1]:
        age_EYC_sel = age_EYC_sel[::-1]
        HgAR_EYC_sel = HgAR_EYC_sel[::-1]

    if age_GDL_sel.iloc[0] > age_GDL_sel.iloc[-1]:
        age_GDL_sel = age_GDL_sel[::-1]
        HgAR_GDL_sel = HgAR_GDL_sel[::-1]

    # === Integrate HgAR curves over the 1970–2023 period ===
    area_EYC = integrate_HgAR(HgAR_EYC_sel, age_EYC_sel)
    area_GDL = integrate_HgAR(HgAR_GDL_sel, age_GDL_sel)

    # === Select 1970–2023 range for error vectors ===
    err_EYC_sel = err_EYC.iloc[0:18]
    err_GDL_sel = err_GDL.iloc[0:20]

    # === Reverse errors if needed ===
    if age_EYC_sel.iloc[0] > age_EYC_sel.iloc[-1]:
        err_EYC_sel = err_EYC_sel[::-1]
    if age_GDL_sel.iloc[0] > age_GDL_sel.iloc[-1]:
        err_GDL_sel = err_GDL_sel[::-1]

    # === Compute uncertainty on area ===
    err_area_EYC = integrate_error(err_EYC_sel, age_EYC_sel)
    err_area_GDL = integrate_error(err_GDL_sel, age_GDL_sel)

    print(f"Hg flux 1970–2023:")
    print(f"  EYC: {area_EYC:.2f} ± {err_area_EYC:.2f} µg/m²")
    print(f"  GDL: {area_GDL:.2f} ± {err_area_GDL:.2f} µg/m²")
    
    # Calcolo masse
    mass_EYC, err_mass_EYC = compute_mass(area_EYC, err_area_EYC, surface_EYC_m2)
    mass_GDL, err_mass_GDL = compute_mass(area_GDL, err_area_GDL, surface_GDL_m2)

    # Stampa risultati in grammi
    print(f"Estimated Mercury mass in sediments (1970–2023):")
    print(f"  EYC lake: {mass_EYC/1e9:.3f} kg ± {err_mass_EYC/1e9:.3f} kg")
    print(f"  GDL lake: {mass_GDL/1e9:.3f} kg ± {err_mass_GDL/1e9:.3f} kg")

    # === Save results ===
    results = pd.DataFrame({
        'Hg_AR_EYC': HgAR_EYC,
        'Err_EYC': err_EYC,
        'Hg_AR_GDL': HgAR_GDL,
        'Err_GDL': err_GDL
    })

    results.to_excel('HgAR.xlsx', index=False)
    print("Results saved in 'HgAR.xlsx'")
    
    
    # --- Normalizza ciascuna curva al proprio valore nel 1970 ---

    # 1) funzione ausiliaria per avere vettori monotoni
    def _ensure_increasing(x, y):
        x = np.asarray(x)
        y = np.asarray(y)
        if x[0] > x[-1]:
            return x[::-1], y[::-1]
        return x, y
    
    # 2) ordina le età e i vettori
    age_EYC_arr, HgAR_EYC_arr = _ensure_increasing(age_EYC.values, HgAR_EYC)
    age_GDL_arr, HgAR_GDL_arr = _ensure_increasing(age_GDL.values, HgAR_GDL)
    
    # 3) valori di riferimento a 1970 (ottenuti per interpolazione)
    HgAR_EYC_ref = float(interp1d(age_EYC_arr, HgAR_EYC_arr, bounds_error=False, fill_value="extrapolate")(1970.0))
    HgAR_GDL_ref = float(interp1d(age_GDL_arr, HgAR_GDL_arr, bounds_error=False, fill_value="extrapolate")(1970.0))
    
    # 4) normalizza ogni curva sul proprio valore
    norm_EYC_all = HgAR_EYC_arr / HgAR_EYC_ref
    norm_GDL_all = HgAR_GDL_arr / HgAR_GDL_ref
    
    # 5) griglia comune di età
    age_common = np.linspace(1970, 2023, 1000)
    
    # 6) interpola sulle stessa griglia
    interp_norm_EYC = interp1d(age_EYC_arr, norm_EYC_all, bounds_error=False, fill_value="extrapolate")
    interp_norm_GDL = interp1d(age_GDL_arr, norm_GDL_all, bounds_error=False, fill_value="extrapolate")
    
    norm_EYC_common = interp_norm_EYC(age_common)
    norm_GDL_common = interp_norm_GDL(age_common)
    
    # 7) integra ciascuna curva
    integral_norm_EYC = np.trapz(norm_EYC_common, age_common)
    integral_norm_GDL = np.trapz(norm_GDL_common, age_common)
    
    # 8) area differenza
    area_between = integral_norm_EYC - integral_norm_GDL
    
    # 9) conversione in massa reale
    # Ora servono i valori di riferimento di ciascun lago:
    # usiamo HgAR_EYC_ref per riportare la differenza in termini reali di EYC
    mass_diff_ug = area_between * HgAR_EYC_ref * surface_EYC_m2
    mass_diff_g  = mass_diff_ug / 1e6
    mass_diff_kg = mass_diff_ug / 1e9
    
    print(f"Normalized integrals (1970-2023): EYC = {integral_norm_EYC:.6f} yr, GDL = {integral_norm_GDL:.6f} yr")
    print(f"Net area (EYC - GDL): {area_between:.6f} yr")
    print(f"Excess Hg due to glacier (1970–2023): {mass_diff_g:.3f} g ({mass_diff_kg:.6f} kg)")# ng/m² * m² = ng
    
    globals().update(locals())

# Clear environment by using main()
if __name__ == "__main__":
    main()
    