import pandas as pd
from stats_can import StatsCan

# Initialize StatsCan
sc = StatsCan()

# Load labour data
df = sc.table_to_df("14-10-0023-01")

# Clean and rename DataFrame for labour data
df_clean = df[['REF_DATE', 'Labour force characteristics', 'North American Industry Classification System (NAICS)', 'Sex', 'Age group', 'VALUE']]
df_main = df_clean.rename(columns={
    'REF_DATE': 'Year',
    'Labour force characteristics': 'Characteristics',
    'North American Industry Classification System (NAICS)': 'Industry',
    'VALUE': 'Value'
})
df_main['Year'] = df_main['Year'].astype(str).str[:4]

# Remove content inside square brackets from 'Industry' column
df_main['Industry'] = df_main['Industry'].str.replace(r'\[.*?\]', '', regex=True).str.strip()

# Group by necessary columns and calculate the mean
df_yearly = df_main.groupby(['Year', 'Characteristics', 'Industry', 'Sex', 'Age group'], as_index=False, observed=False).mean()

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
processed_data.loc[:, 'Difference (%)'] = processed_data['Male Participation Rate (%)'] - processed_data['Female Participation Rate (%)']

# Save the processed data to a new CSV file
processed_data.to_csv('processed_participation_rates.csv', index=False)

# Save the original processed data to a CSV file
df_yearly.to_csv('processed_stats_canada_data.csv', index=False)

# Load wage data
df_wages = sc.table_to_df("14-10-0064-01")

# Clean and rename DataFrame for wages
df_clean_wages = df_wages[['REF_DATE', 'Wages', 'Type of work', 'North American Industry Classification System (NAICS)', 'Sex', 'Age group', 'VALUE']]
df_main_wages = df_clean_wages.rename(columns={
    'REF_DATE': 'Year',
    'Wages': 'Type of Wages',
    'Type of work': 'Characteristics',
    'North American Industry Classification System (NAICS)': 'Industry',
    'VALUE': 'Value'
})
df_main_wages['Year'] = df_main_wages['Year'].astype(str).str[:4]

# Remove content inside square brackets from 'Industry' column
df_main_wages['Industry'] = df_main_wages['Industry'].str.replace(r'\[.*?\]', '', regex=True).str.strip()

# Group by necessary columns and calculate the mean
df_yearly_wages = df_main_wages.groupby(['Year', 'Type of Wages', 'Characteristics', 'Industry', 'Sex', 'Age group'], as_index=False, observed=False).mean()

# Function to calculate the gender pay gap
def calculate_gender_pay_gap(df):
    # Pivot the table to have separate columns for Male and Female wages
    df_pivot = df.pivot_table(index=['Year', 'Industry', 'Type of Wages', 'Characteristics', 'Age group'], columns='Sex', values='Value', aggfunc='mean').reset_index()
    
    # Calculate Gender Pay Ratio and Gender Pay Gap
    df_pivot['Gender Pay Ratio'] = df_pivot['Females'] / df_pivot['Males']
    df_pivot['Gender Pay Gap (%)'] = (1 - df_pivot['Gender Pay Ratio']) * 100
    
    return df_pivot

# Get unique types of wages
unique_types_of_wages = df_yearly_wages['Type of Wages'].unique()

# Initialize an empty DataFrame to store combined results
df_combined_gender_pay_gap = pd.DataFrame()

# Process and combine results for each type of wage
for wage_type in unique_types_of_wages:
    df_filtered = df_yearly_wages[df_yearly_wages['Type of Wages'] == wage_type]
    df_gender_pay_gap = calculate_gender_pay_gap(df_filtered)
    
    # Add the type of wage as a column for clarity
    df_gender_pay_gap['Type of Wages'] = wage_type
    
    # Concatenate the results to the combined DataFrame
    df_combined_gender_pay_gap = pd.concat([df_combined_gender_pay_gap, df_gender_pay_gap], ignore_index=True)

# Save the combined data to a single CSV file
df_combined_gender_pay_gap.to_csv('combined_gender_pay_gap.csv', index=False)

# Save the processed data for general wages characpython update_csv.pyteristics to a CSV file
df_yearly_wages.to_csv('processed_wages_data.csv', index=False)

# Display the processed DataFrame (optional)
print("Data successfully saved to processed_stats_canada_data.csv, processed_participation_rates.csv, processed_wages_data.csv, and combined_gender_pay_gap.csv")
