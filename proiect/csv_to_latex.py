import pandas as pd

# Read the CSV file
df = pd.read_csv('csv_output/recursive_largest_first_results.csv')

# Convert DataFrame to LaTeX table format
latex_table = df.to_latex(index=False)

# Save to a file
with open('table.tex', 'w') as f:
    f.write(latex_table)
