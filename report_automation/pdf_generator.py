
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)


def generate_pdf_report(data, output_path):
    """Generate a PDF report containing data summaries and charts."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    chart_path = output_path.parent / "sales_chart.png"
    styles = getSampleStyleSheet()
    elements = []

    # Report title and date
    elements.append(
        Paragraph("Enterprise Data Analysis Report", styles["Title"])
    )
    elements.append(
        Paragraph(
            f"Generated on: {datetime.now():%d-%m-%Y %H:%M}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 20))

    # Basic report summary
    elements.append(Paragraph("Dataset Summary", styles["Heading2"]))
    elements.append(
        Paragraph(f"Total records: {len(data)}", styles["Normal"])
    )
    elements.append(
        Paragraph(
            f"Total columns: {len(data.columns)}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 15))

    # Numeric summary table
    numeric_data = data.select_dtypes(include="number")

    if not numeric_data.empty:
        summary = numeric_data.describe().round(2).reset_index()
        table_data = [summary.columns.tolist()]
        table_data.extend(summary.values.tolist())

        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24476B")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        elements.append(table)
        elements.append(Spacer(1, 20))

    # Create a chart from the first two numeric columns
    if len(numeric_data.columns) >= 2:
        x_column = numeric_data.columns[0]
        y_column = numeric_data.columns[1]

        plt.figure(figsize=(7, 4))
        plt.bar(
            data[x_column].astype(str),
            data[y_column],
        )
        plt.title(f"{y_column} by {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(chart_path, dpi=150)
        plt.close()

        elements.append(Paragraph("Data Visualization", styles["Heading2"]))
        elements.append(Image(str(chart_path), width=6 * inch, height=3.4 * inch))

    # Build the PDF
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        title="Enterprise Data Analysis Report",
    )
    document.build(elements)

    # Remove temporary chart file
    if chart_path.exists():
        chart_path.unlink()

    return output_path
