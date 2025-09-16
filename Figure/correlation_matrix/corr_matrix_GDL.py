# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:44:27 2024

@author: mattiod
"""

import pandas as pd
import plotly.express as px
import numpy as np

# Load the data
data = pd.read_excel("corr_GDL.xlsx")

# Consider only the first 201 rows
data_limited = data.iloc[:201]

# List of columns to consider
columns = ['CLR_K', 'CLR_Ti', 'CLR_Si', 'CLR_Al', 'CLR_Ca', 'CLR_Mn', 'CLR_Fe', 'CLR_Rb', 'CLR_Sr', 'CLR_Zr', 'CLR_Pb', 'CLR_Br', 'LOI_950', 'Hg_AR']

# Apply a moving average to all columns and create a new DataFrame
n = 1
data_rolling = data_limited[columns].rolling(window=n).mean()

# Rename the columns for the new DataFrame
data_rolling.columns = [col.replace('CLR_', '').replace('_', ' ') for col in columns]

# Compute the correlation matrix
corr_matrix_GDL = data_rolling.corr()

# Round correlation values to two decimal places
rounded_corr_matrix_GDL = np.round(corr_matrix_GDL, 2)

# Create the interactive heatmap with rounded values
fig_GDL = px.imshow(rounded_corr_matrix_GDL, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r',
                    labels=dict(color="Correlation"), zmin=-1, zmax=1)

fig_GDL.update_layout(title="Correlation Matrix GDL", autosize=False, width=800, height=600)

# Customize hover labels
fig_GDL.update_traces(hovertemplate='x: %{x}<br>y: %{y}<br>Correlation: %{customdata:.2f}')

# Add 'customdata' to correctly format the correlation value
fig_GDL.data[0].update(customdata=rounded_corr_matrix_GDL.values)

# Display the figure
fig_GDL.show()

# Save the figure as a PDF file
fig_GDL.write_image("correlation_matrix_GDL.pdf", format='pdf', engine='kaleido')