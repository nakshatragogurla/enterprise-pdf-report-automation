
from pathlib import Path

from report_automation.data_processor import load_data, generate_summary


def test_sample_data():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "sample_data.csv"
    )

    data = load_data(file_path)
    summary = generate_summary(data)

    assert len(data) == 5
    assert summary["total_records"] == 5
    assert "Monthly_Sales" in summary["columns"]
