from __future__ import annotations

import csv
from pathlib import Path

from .model import PostingEntry, ReceiptData
from .tax_rules import get_rule


class ReceiptProcessor:
    def create_postings(self, receipt: ReceiptData) -> list[PostingEntry]:
        postings: list[PostingEntry] = []
        for item in receipt.items:
            rule = get_rule(item.vat_rate)
            postings.append(
                PostingEntry(
                    receipt_id=receipt.receipt_id,
                    posting_date=receipt.receipt_date,
                    merchant=receipt.merchant,
                    description=item.description,
                    net_amount=item.net_amount,
                    vat_amount=item.vat_amount,
                    gross_amount=item.gross_amount,
                    vat_rate=item.vat_rate,
                    konto_skr03=rule.konto_skr03,
                    steuer_schluessel=rule.steuer_schluessel,
                )
            )
        return postings

    def export_csv(self, postings: list[PostingEntry], output_path: str | Path) -> Path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)

        with target.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh, delimiter=";")
            writer.writerow(
                [
                    "Belegnummer",
                    "Buchungsdatum",
                    "Lieferant",
                    "Beschreibung",
                    "Netto",
                    "MwSt",
                    "Brutto",
                    "MwSt_Satz",
                    "Konto_SKR03",
                    "Steuerschluessel",
                ]
            )
            for posting in postings:
                writer.writerow(posting.to_csv_row())

        return target
