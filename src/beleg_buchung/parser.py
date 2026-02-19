from __future__ import annotations

from datetime import date
from decimal import Decimal
import re

from .model import ReceiptData, ReceiptItem
from .tax_rules import classify_vat_rate

ITEM_PATTERN = re.compile(r"^(.+?)\s+([0-9]+(?:[\.,][0-9]{1,2})?)$")
DATE_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})")


def parse_receipt_text(text: str, receipt_id: str = "AUTO") -> ReceiptData:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    merchant = lines[0] if lines else "Unbekannt"
    receipt_date = _extract_date(lines)
    items: list[ReceiptItem] = []

    for line in lines[1:]:
        match = ITEM_PATTERN.match(line)
        if not match:
            continue
        description = match.group(1)
        amount_raw = match.group(2).replace(",", ".")
        gross_amount = Decimal(amount_raw)
        vat_rate = classify_vat_rate(description)
        net_amount = (gross_amount / (Decimal("1.00") + vat_rate)).quantize(Decimal("0.01"))
        items.append(ReceiptItem(description=description, net_amount=net_amount, vat_rate=vat_rate))

    return ReceiptData(receipt_id=receipt_id, merchant=merchant, receipt_date=receipt_date, items=items)


def _extract_date(lines: list[str]) -> date:
    for line in lines:
        date_match = DATE_PATTERN.search(line)
        if date_match:
            return date.fromisoformat(date_match.group(1))
    return date.today()
