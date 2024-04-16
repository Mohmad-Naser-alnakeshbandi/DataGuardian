from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
# Import your data quality check module
import data_quality_checks

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        csv_file = request.files['file']
        if csv_file:
            dataframe = pd.read_csv(csv_file, sep=';')
            html_results = data_quality_checks.run_checks(dataframe)
            sample_data_html = dataframe.head(10).to_html(classes='table table-striped', header="true", index=False, border=0)
            return render_template('results.html', tables=html_results, sample_data=sample_data_html)
    return render_template('upload.html')



@app.route('/validate', methods=['GET'])
def validate():
    dataframe = pd.read_csv('temp.csv')
    # Perform data quality checks
    results = data_quality_checks.run_checks(dataframe)
    return render_template('results.html', tables=[results.to_html(classes='data')], titles=results.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
