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
from scipy.stats import pearsonr
from tabulate import tabulate

# Set up font and axis sizes for all plots
plt.rc('font', size=15)
plt.rc('axes', titlesize=15, labelsize=15)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.rc('legend', fontsize=15)
plt.rc('figure', titlesize=15)

# Function to load data from an Excel file
def load_data(file_path):
    return pd.read_excel(file_path)

# Function to aggregate core scan data by averaging the elements and Hg values within depth intervals
def aggregate_core_scan(df, depth_col, element_cols, hg_col, hg_depth_col):
    result_rows = []  # List to store the aggregated results
    df = df.sort_values(by=depth_col)  # Sort data by depth column
    hg_depths = df[[hg_depth_col, hg_col]].dropna().sort_values(by=hg_depth_col)  # Select Hg depth and values, drop NaNs, and sort
    
    # Loop through the Hg depths and calculate the mean of the element concentrations within depth ranges
    for i in range(len(hg_depths) - 1):
        depth_min = hg_depths.iloc[i][hg_depth_col]  # Minimum depth
        depth_max = hg_depths.iloc[i + 1][hg_depth_col]  # Maximum depth
        hg_value = hg_depths.iloc[i][hg_col]  # Hg value at this depth
        
        # Subset the dataframe to include rows within the depth range
        subset = df[(df[depth_col] >= depth_min) & (df[depth_col] < depth_max)]
        # Calculate the mean values of the elements for the current depth range
        mean_values = subset[element_cols].mean()
        mean_values[hg_col] = hg_value  # Assign the Hg value for this depth
        mean_values[hg_depth_col] = (depth_min + depth_max) / 2  # Calculate the average depth for this range
        result_rows.append(mean_values)  # Append the results for this depth range
    
    # Return a DataFrame with the aggregated values
    return pd.DataFrame(result_rows)

# Function to plot regression subplots with element data and Hg correlation
def plot_regression_subplots(df, element_cols, y_var, color_var):
    # Create a 3x2 grid of subplots
    fig, axs = plt.subplots(3, 2, figsize=(12, 15), sharey=True)
    axs = axs.flatten()  # Flatten the 2D array of axes

    scatter_plots = []  # List to hold scatter plot objects for color bar
    labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']  # Only 6 labels

    for i, x_var in enumerate(element_cols):
        ax = axs[i]
        x = df[x_var].values.reshape(-1, 1)
        y = df[y_var].values
        colors = df[color_var].values

        # Fit linear regression
        model = LinearRegression()
        model.fit(x, y)
        y_pred = model.predict(x)
        r2 = r2_score(y, y_pred)
        slope, intercept, r_value, p_value, std_err = linregress(x.flatten(), y)

        scatter = ax.scatter(x.flatten(), y, c=colors, cmap="viridis", edgecolor='k')
        scatter_plots.append(scatter)

        line_color = 'red' if r2 > 0.5 else 'black'
        ax.plot(x, y_pred, color=line_color, linewidth=2, label=f'$R^2$ = {r2:.3f}\n$p$ = {p_value:.3g}')
        ax.set_xlabel(x_var.replace("_", " "))
        ax.set_title(labels[i], loc='left', fontweight='bold')
        ax.legend()

    axs[0].set_ylabel(f"{y_var.replace('_', ' ').replace('Hg EYC', 'THg')} (ng/g)")

    fig.subplots_adjust(right=0.88)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(scatter_plots[-1], cax=cbar_ax)
    cbar.set_label(color_var.replace("Age_EYC", "Age"))

    plt.savefig('erosion.pdf', bbox_inches='tight', pad_inches=0.2)
    plt.savefig('erosion.png', bbox_inches='tight', pad_inches=0.2, dpi=500)
    plt.show()
    
# Function to compute correlation between Hg and elements before and after 1970
def compute_correlations_by_period(df, element_cols, hg_col, age_col, cutoff=1970):
    rows = []
    for elem in element_cols:
        before = df[df[age_col] < cutoff]
        after = df[df[age_col] >= cutoff]

        # Calculate Pearson correlation and p-value only if at least 3 points
        if len(before) >= 3:
            r_before, p_before = pearsonr(before[elem], before[hg_col])
        else:
            r_before, p_before = (float('nan'), float('nan'))

        if len(after) >= 3:
            r_after, p_after = pearsonr(after[elem], after[hg_col])
        else:
            r_after, p_after = (float('nan'), float('nan'))

        rows.append({
            'Element': elem.replace("CLR_", ""),
            'R_before_1970': r_before,
            'p_before_1970': p_before,
            'R_after_1970': r_after,
            'p_after_1970': p_after
        })

    corr_df = pd.DataFrame(rows)
    corr_df.to_excel('correlation_table.xlsx', index=False)
    print("\nCorrelation Table:\n")
    print(tabulate(corr_df.round(4), headers='keys', tablefmt='fancy_grid'))
    return corr_df

# Main function to load the data, process it, and plot the regression subplots
def main(file_path):
    df = load_data(file_path)  # Load the data from the provided file path
    depth_col = 'Age_X_EYC'  # Column representing the depth (age) for the EYC core
    hg_depth_col = 'Age_EYC'  # Column representing the depth for the Hg EYC measurements
    element_cols = ['CLR_Al', 'CLR_Si', 'CLR_Ti', 'CLR_Zr', 'CLR_Fe', 'CLR_Br']
    hg_col = 'Hg_EYC'  # Hg concentration column
    age_col = 'Age_EYC'  # Age column for EYC core
    
    processed_df = aggregate_core_scan(df, depth_col, element_cols, hg_col, hg_depth_col)  # Process the data by aggregating core scan values
    processed_df.to_excel('processed_data.xlsx', index=False)  # Save the processed data to an Excel file
    
    plot_regression_subplots(processed_df, element_cols, hg_col, age_col)  # Plot the regression subplots
    compute_correlations_by_period(processed_df, element_cols, hg_col, age_col)
    

# Run the script if this file is executed directly
if __name__ == "__main__":
    file_path = 'data_graph.xlsx'  # Path to the input data file
    main(file_path)  # Call the main function with the file path