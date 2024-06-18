from flask import Flask, send_file
import pandas as pd
from stats_can import StatsCan
import io

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

app = Flask(__name__)

@app.route('/data.csv', methods=['GET'])
def get_data_csv():
    # Save DataFrame to a CSV file
    csv_data = df_yearly.to_csv(index=False)

    # Create an in-memory file-like object
    csv_io = io.StringIO()
    csv_io.write(csv_data)
    csv_io.seek(0)

    # Return the CSV file as a downloadable link
    return send_file(csv_io, as_attachment=True, download_name='data.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
