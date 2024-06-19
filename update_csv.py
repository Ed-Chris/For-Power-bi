import pandas as pd
from stats_can import StatsCan

# Initialize StatsCan
sc = StatsCan()

# Load data
df = sc.table_to_df("14-10-0023-01")

# Clean and rename DataFrame
df_clean = df[['REF_DATE', 'Labour force characteristics', 'North American Industry Classification System (NAICS)', 'Sex', 'Age group', 'VALUE']]
df_main = df_clean.rename(columns={
    'REF_DATE': 'Year',
    'Labour force characteristics': 'Characteristics',
    'North American Industry Classification System (NAICS)': 'Industry',
    'VALUE': 'Value'
})
df_main['Year'] = df_main['Year'].astype(str)
df_main['Year'] = df_main['Year'].str[:4]

# Remove content inside square brackets from 'Industry' column
df_main['Industry'] = df_main['Industry'].str.replace(r'\[.*?\]', '', regex=True).str.strip()

df_yearly = df_main.groupby(['Year', 'Characteristics', 'Industry', 'Sex', 'Age group'], as_index=False).mean()

# Save the first CSV file
csv_file_path_1 = "processed_stats_canada_data.csv"
df_yearly.to_csv(csv_file_path_1, index=False)

# Filter the data to include only 'Employment', 'Full-time employment', and 'Part-time employment' characteristics
selected_characteristics = ['Employment', 'Full-time employment', 'Part-time employment']
employment_data = df_yearly[df_yearly['Characteristics'].isin(selected_characteristics)]

# Pivot the table to have 'Sex' as columns
pivot_table = employment_data.pivot_table(index=['Year', 'Industry', 'Age group', 'Characteristics'], columns='Sex', values='Value')

# Calculate participation rate for males and females in percentage
pivot_table['Male Participation Rate (%)'] = (pivot_table['Males'] / pivot_table['Both sexes']) * 100
pivot_table['Female Participation Rate (%)'] = (pivot_table['Females'] / pivot_table['Both sexes']) * 100

# Reset the index to make it easier to export
pivot_table.reset_index(inplace=True)

# Select relevant columns
processed_data = pivot_table[['Year', 'Industry', 'Age group', 'Characteristics', 'Male Participation Rate (%)', 'Female Participation Rate (%)']]

# Calculate the difference in participation rates between male and female
processed_data['Difference (%)'] = processed_data['Male Participation Rate (%)'] - processed_data['Female Participation Rate (%)']

# Save the second CSV file
csv_file_path_2 = "processed_participation_rates.csv"
processed_data.to_csv(csv_file_path_2, index=False)

# Output the processed DataFrames (optional)
print("Data successfully saved to", csv_file_path_1, "and", csv_file_path_2)
df_yearly
processed_data
