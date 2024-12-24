import pandas as pd


def load_csv_file(csv_file):
    """
    Load the entire CSV file into a DataFrame.
    """
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Error loading CSV file from {csv_file}: {e}")


def load_column_from_csv(csv_file, column_name):
    """
    Extract a specific column from the CSV file.
    """
    try:
        df = load_csv_file(csv_file)
        if column_name not in df.columns:
            raise KeyError(f"The column '{column_name}' does not exist in the CSV file.")  
        return df[column_name].dropna().tolist()  
    except KeyError as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(f"Error extracting column '{column_name}' from {csv_file}: {e}")