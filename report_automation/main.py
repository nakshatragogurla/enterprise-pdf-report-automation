
import argparse
import logging
from pathlib import Path

from report_automation.data_processor import load_data, generate_summary
from report_automation.pdf_generator import generate_pdf_report


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    parser = argparse.ArgumentParser(
        description="Enterprise PDF Report Automation"
    )

    parser.add_argument(
        "--input",
        default=str(PROJECT_ROOT / "data" / "sample_data.csv"),
        help="Path to the input CSV file",
    )

    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "reports" / "enterprise_report.pdf"),
        help="Path for the generated PDF report",
    )

    args = parser.parse_args()

    try:
        data = load_data(args.input)
        summary = generate_summary(data)
        report_path = generate_pdf_report(data, args.output)

        logging.info("PDF report generated successfully: %s", report_path)

        print("\nReport generated successfully!")
        print(f"Records processed: {summary['total_records']}")
        print(f"Columns found: {len(summary['columns'])}")
        print(f"PDF saved at: {report_path}")

    except (FileNotFoundError, ValueError, OSError) as error:
        logging.error("Report generation failed: %s", error)
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
