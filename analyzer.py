def analyze_data(df):

    analysis = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": df.isnull().sum().sum(),
        "Column Names": list(df.columns)
    }

    cleaned_df = df.drop_duplicates()

    cleaned_file = "cleaned_dataset.xlsx"

    cleaned_df.to_excel(
        cleaned_file,
        index=False
    )
    analysis["Cleaned File"] = cleaned_file
    return analysis