import pandas as pd


def check_missing_values(df):
    """Check for missing values in the DataFrame."""
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]
    if not missing_data.empty:
        return f"Missing values found in columns: {missing_data.to_dict()}"
    else:
        return "No missing values found."


def check_duplicates(df):
    """Check for duplicate rows in the DataFrame."""
    if df.duplicated().any():
        return "Duplicates found in the data."
    else:
        return "No duplicates found."

def text_data_validation(df):
    """Validate text columns for common formatting issues."""
    text_issues = {}
    for column in df.select_dtypes(include=[object]).columns:
        if df[column].str.contains(r'[^\w\s]', regex=True).any():
            text_issues[column] = "Contains special characters"
    if not text_issues:
        return "No text formatting issues detected."
    return f"Text formatting issues found in columns: {text_issues}"


def check_data_types(df):
    """Generate an HTML table showing data types and any incorrect types in the DataFrame."""
    type_report = {}
    incorrect_types = {}

    for column in df.columns:
        # Clean column name from any leading or trailing spaces
        column_clean = column.strip()

        # Record the actual data type of each column
        dtype = df[column].dtype
        type_report[column_clean] = str(dtype)

        # Check if numeric data is mistakenly stored as a string
        if pd.api.types.is_string_dtype(df[column]) and df[column].str.isnumeric().any():
            incorrect_types[column_clean] = 'Expected numeric, found string'

    # Start HTML table
    html_content = '<table class="table table-bordered"><tr><th>Column</th><th>Data Type</th><th>Notes</th></tr>'

    # Populate table rows
    for column, dtype in type_report.items():
        note = incorrect_types.get(column, "Correct type")
        html_content += f'<tr><td>{column}</td><td>{dtype}</td><td>{note}</td></tr>'

    # Close HTML table
    html_content += '</table>'

    return html_content


def run_checks(df):
    """Run all data quality checks and compile results into HTML formatted string."""
    results = {}
    results['Missing Values'] = check_missing_values(df)
    results['Duplicates'] = check_duplicates(df)
    results['Data Types'] = check_data_types(df)
    results['Text Validation'] = text_data_validation(df)

    # Build HTML content
    html_content = '<table class="table table-striped"><tr><th>Check</th><th>Result</th></tr>'
    for check, result in results.items():
        html_content += f'<tr><td>{check}</td><td>{result}</td></tr>'
    html_content += '</table>'
    return html_content

