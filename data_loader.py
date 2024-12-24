import pandas as pd


def load_csv_file(csv_file):
    """
    Load the entire CSV file into a DataFrame.
    """
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Error loading CSV file from {csv_file}: {e}")


def load_tv_show_names_from_csv(csv_file):
    """
    Extract the TV show titles from the CSV file.
    """
    try:
        df = load_csv_file(csv_file)  
        return df["Title"].tolist()  
    except KeyError:
        raise ValueError(f"The 'Title' column is missing in {csv_file}")
    except Exception as e:
        raise ValueError(f"Error extracting TV show names from {csv_file}: {e}")
