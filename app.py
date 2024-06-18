from flask import Flask, send_file
import io
from dataprocessing import df_yearly

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
