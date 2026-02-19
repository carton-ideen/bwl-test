from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass(slots=True)
class ReceiptItem:
    description: str
    net_amount: Decimal
    vat_rate: Decimal

    @property
    def vat_amount(self) -> Decimal:
        return (self.net_amount * self.vat_rate).quantize(Decimal("0.01"))

    @property
    def gross_amount(self) -> Decimal:
        return (self.net_amount + self.vat_amount).quantize(Decimal("0.01"))


@dataclass(slots=True)
class ReceiptData:
    receipt_id: str
    merchant: str
    receipt_date: date
    items: list[ReceiptItem] = field(default_factory=list)

    @property
    def total_net(self) -> Decimal:
        return sum((item.net_amount for item in self.items), Decimal("0.00")).quantize(Decimal("0.01"))

    @property
    def total_vat(self) -> Decimal:
        return sum((item.vat_amount for item in self.items), Decimal("0.00")).quantize(Decimal("0.01"))

    @property
    def total_gross(self) -> Decimal:
        return (self.total_net + self.total_vat).quantize(Decimal("0.01"))


@dataclass(slots=True)
class PostingEntry:
    receipt_id: str
    posting_date: date
    merchant: str
    description: str
    net_amount: Decimal
    vat_amount: Decimal
    gross_amount: Decimal
    vat_rate: Decimal
    konto_skr03: str
    steuer_schluessel: str

    def to_csv_row(self) -> list[str]:
        return [
            self.receipt_id,
            self.posting_date.isoformat(),
            self.merchant,
            self.description,
            f"{self.net_amount:.2f}",
            f"{self.vat_amount:.2f}",
            f"{self.gross_amount:.2f}",
            f"{self.vat_rate * Decimal('100'):.0f}",
            self.konto_skr03,
            self.steuer_schluessel,
        ]
