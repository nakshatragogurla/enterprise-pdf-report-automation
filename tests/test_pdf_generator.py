
from pathlib import Path

import pandas as pd

from report_automation.pdf_generator import generate_pdf_report


def test_generate_pdf_report(tmp_path):
    data = pd.DataFrame({
        "Department": ["ECE", "CSE", "EEE"],
        "Employees": [10, 20, 15],
        "Monthly_Sales": [100000, 200000, 150000],
    })

    output_file = tmp_path / "test_report.pdf"

    result = generate_pdf_report(data, output_file)

    assert result.exists()
    assert result.stat().st_size > 0
    assert result.suffix == ".pdf"
