from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class TaxRule:
    vat_rate: Decimal
    konto_skr03: str
    steuer_schluessel: str


GERMAN_TAX_RULES = {
    Decimal("0.19"): TaxRule(vat_rate=Decimal("0.19"), konto_skr03="4650", steuer_schluessel="9"),
    Decimal("0.07"): TaxRule(vat_rate=Decimal("0.07"), konto_skr03="4660", steuer_schluessel="8"),
}

FOOD_KEYWORDS = {
    "essen",
    "gericht",
    "mahlzeit",
    "snack",
    "brot",
    "kuchen",
    "sandwich",
}

DRINK_KEYWORDS = {
    "getränk",
    "wasser",
    "cola",
    "saft",
    "bier",
    "kaffee",
    "tee",
    "wein",
}


def classify_vat_rate(description: str) -> Decimal:
    normalized = description.strip().lower()
    if any(keyword in normalized for keyword in FOOD_KEYWORDS):
        return Decimal("0.07")
    if any(keyword in normalized for keyword in DRINK_KEYWORDS):
        return Decimal("0.19")
    return Decimal("0.19")


def get_rule(vat_rate: Decimal) -> TaxRule:
    if vat_rate not in GERMAN_TAX_RULES:
        raise ValueError(f"Keine Steuerregel für MwSt.-Satz {vat_rate} hinterlegt")
    return GERMAN_TAX_RULES[vat_rate]
