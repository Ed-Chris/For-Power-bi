import pandas as pd
import re
from stats_can import StatsCan

# Initialize StatsCan
sc = StatsCan()

flag = {"checking"}
flag_df = pd.DataFrame(flag)

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

# Group by necessary columns and calculate the mean
df_yearly = df_main.groupby(['Year', 'Characteristics', 'Industry', 'Sex', 'Age group'], as_index=False, observed=False).mean()

# Filter the data to include only 'Employment', 'Full time', and 'Part time' characteristics
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
processed_data.loc[:, 'Difference (%)'] = processed_data['Male Participation Rate (%)'] - processed_data['Female Participation Rate (%)']

# Save the processed data to a new CSV file
processed_data.to_csv('processed_participation_rates.csv', index=False)

# Save the original processed data to a CSV file
df_yearly.to_csv('processed_stats_canada_data.csv', index=False)

flag_df.to_csv('check.csv',index=False)

# Display the processed DataFrame (optional)
print("Data successfully saved to processed_stats_canada_data.csv and processed_participation_rates.csv")
