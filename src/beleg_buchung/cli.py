from __future__ import annotations

import argparse
from pathlib import Path

from .parser import parse_receipt_text
from .processor import ReceiptProcessor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kassenbelege einlesen und für Steuerberater exportieren")
    parser.add_argument("input", type=Path, help="Pfad zur Textdatei mit OCR-Inhalt des Kassenbelegs")
    parser.add_argument("--receipt-id", default="AUTO", help="Beleg-ID für die Buchung")
    parser.add_argument("--output", default="export/buchungen.csv", help="Ausgabedatei für CSV-Export")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    text = args.input.read_text(encoding="utf-8")
    receipt = parse_receipt_text(text=text, receipt_id=args.receipt_id)
    processor = ReceiptProcessor()
    postings = processor.create_postings(receipt)
    output_file = processor.export_csv(postings, args.output)
    print(f"{len(postings)} Buchungssätze exportiert: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
