from decimal import Decimal

from beleg_buchung.parser import parse_receipt_text
from beleg_buchung.processor import ReceiptProcessor


def test_receipt_parsing_and_posting_rules() -> None:
    receipt = parse_receipt_text(
        """Cafe Test
2026-01-01
Essen Suppe 10,70
Getränk Wasser 2,38
""",
        receipt_id="B-1",
    )

    processor = ReceiptProcessor()
    postings = processor.create_postings(receipt)

    assert len(postings) == 2
    assert postings[0].vat_rate == Decimal("0.07")
    assert postings[0].konto_skr03 == "4660"
    assert postings[1].vat_rate == Decimal("0.19")
    assert postings[1].konto_skr03 == "4650"
