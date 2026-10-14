
import pandas as pd
from pathlib import Path


def load_data(file_path):
    """Load and validate CSV data."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if file_path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    data = pd.read_csv(file_path)

    if data.empty:
        raise ValueError("The CSV file contains no data.")

    if data.columns.duplicated().any():
        raise ValueError("The CSV file contains duplicate column names.")

    if data.isnull().values.any():
        raise ValueError("The CSV file contains missing values.")

    return data


def generate_summary(data):
    """Generate summary statistics for numeric columns."""
    numeric_data = data.select_dtypes(include="number")

    if numeric_data.empty:
        raise ValueError("The CSV file must contain numeric columns.")

    summary = {
        "total_records": len(data),
        "columns": list(data.columns),
        "numeric_summary": numeric_data.describe().round(2).to_dict(),
    }

    return summary
