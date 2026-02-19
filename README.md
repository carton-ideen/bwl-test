# Beleg-Buchungstool (Deutschland)

Dieses Tool liest Kassenbelege aus OCR-Textdateien ein und erzeugt Buchungssätze als CSV für die Weitergabe an den Steuerberater.

## Steuerlogik (vereinfachtes Beispiel)

- **7 % MwSt.** für typische Lebensmittel-/Essenspositionen (z. B. "Essen", "Sandwich").
- **19 % MwSt.** für Getränke und Standardfälle (z. B. "Kaffee", "Wasser").
- Zuordnung zu SKR03-Konten:
  - 7 %: Konto **4660**, Steuerschlüssel **8**
  - 19 %: Konto **4650**, Steuerschlüssel **9**

> Hinweis: Steuerliche Sonderfälle (Bewirtung, Vorsteuerabzugseinschränkungen, Reverse-Charge, Kleinunternehmer etc.) sind in dieser Demo nicht vollständig abgedeckt und müssen individuell geprüft werden.

## Nutzung

```bash
python -m beleg_buchung.cli beispielbeleg.txt --receipt-id RE-2026-001 --output export/buchungen.csv
```

## Beispiel für Eingabedatei

```text
Cafe Muster GmbH
Belegdatum: 2026-01-12
Essen Tagesgericht 12,90
Wasser still 3,50
Kaffee 2,80
```

## Ausgabe

CSV mit Spalten:

- Belegnummer
- Buchungsdatum
- Lieferant
- Beschreibung
- Netto
- MwSt
- Brutto
- MwSt_Satz
- Konto_SKR03
- Steuerschluessel
