# 🏠 WG-Kostenteiler (Terminal-Anwendung)

Ein über das Terminal bedienbarer Kostenaufteiler für eine Wohngemeinschaft.
Rechnungen werden erfasst, gerecht auf die betroffenen Personen aufgeteilt und
nachverfolgt, damit am Monatsende auf einen Blick sichtbar ist, wer noch wie viel zahlen muss.


---

## 📝 Analyse

### Problem

In einer WG fallen laufend gemeinsame Kosten an (Miete, Strom, Internet, Einkäufe, …).
Eine Person bezahlt die Rechnung, die Kosten betreffen aber mehrere Personen. Wer die Anteile
von Hand ausrechnet, macht schnell Rechenfehler (z. B. beim Rappen-Rest), und es geht
vergessen, wer schon bezahlt hat und wer nicht.

### Szenario

Eine WG-Bewohner:in startet das Programm im Terminal, legt die Mitbewohner:innen und Kostenkategorien an
und erfasst die Rechnungen des Monats. Das Programm teilt den Betrag automatisch auf, zeigt die Anteile pro Person an
und weist beim Start auf überfällige Zahlungen hin. Über Filter, Statistik und den Monatsauszug
behält die WG den Überblick.

### Benutzerrolle

| Rolle | Beschreibung |
|-------|--------------|
| **WG-Bewohner:in** | Erfasst Personen, Kategorien und Rechnungen, pflegt den Bezahlstatus und wertet die Ausgaben aus. |

### Hauptstory

**Als** WG-Bewohner:in **möchte ich** Rechnungen erfassen und automatisch auf die betroffenen Personen aufteilen lassen,
**damit** ich am Monatsende auf einen Blick sehe, wer wie viel noch zahlen muss, und nicht alles von Hand ausrechnen muss.

### User Stories und Umsetzung

Die ausführlichen Akzeptanzkriterien stehen im Dokument *«User Stories und Akzeptanzkriterien»* (Abgabe 11.10.2026).

| ID | User Story | Verantwortlich | Modul |
|----|-----------|----------------|-------|
| US1 | Person anlegen | Piraveena Murugupillai | `data/personen.py` |
| US2 | Personenstamm anzeigen und bearbeiten | Enes Varol | `data/personen.py` |
| US3 | Kategorien anlegen | Kristina Stevic | `data/kategorien.py` |
| US4 | Kategorien anzeigen und bearbeiten | Julian Erni | `data/kategorien.py` |
| US5 | Reminder für überfällige Rechnungen | Piraveena Murugupillai | `logic/reminder.py` |
| US6 | Rechnung erfassen | Enes Varol | `data/rechnungen_data.py` |
| US7 | Gerechte Aufteilung mit Rappen-Rest | Kristina Stevic | `logic/rechnung_logic.py` |
| US8 | Rechnungsdetails bearbeiten | Julian Erni | `data/rechnungen_data.py` |
| US9 | Bezahlstatus bearbeiten | Piraveena Murugupillai | `logic/rechnung_logic.py` |
| US10 | Rechnungen anzeigen und filtern | Enes Varol | `user_interface/rechnung_anzeigen.py` |
| US11 | Statistik nach Kategorie | Kristina Stevic | `user_interface/statistik.py` |
| US12 | Monatsauszug als Datei speichern | Julian Erni | `user_interface/export.py` |

---

## ✅ Projektanforderungen

### 1. Interaktive Anwendung (Konsoleneingabe)

Die Bedienung erfolgt vollständig über Menüs im Terminal. Das Hauptmenü:

```text
=== WG-Kostenteiler ===
1. Rechnungen
2. Auswertungen
3. Personen
4. Kategorien
5. Menü verlassen
```

| Menü | Optionen |
|------|----------|
| **Rechnungen** | Rechnung erfassen · Alle Rechnungen anzeigen · nach Monat filtern · nach Person filtern · nach Status filtern · Bezahlstatus bearbeiten · Rechnung bearbeiten |
| **Auswertungen** | Statistik nach Kategorie · Überfällige Rechnungen anzeigen · Monatsauszug speichern |
| **Personen** | Person anlegen · löschen · Personenliste anzeigen · Person bearbeiten |
| **Kategorien** | Kategorie anlegen · anzeigen · umbenennen · löschen |

Beim Programmstart werden überfällige Rechnungsanteile automatisch angezeigt (US5).

### 2. Datenvalidierung

Alle Eingaben werden geprüft. Bei einem Fehler erscheint eine Meldung und die Eingabe wird wiederholt, das Programm stürzt nicht ab.

| Eingabe | Regel | Beispiel |
|---------|-------|----------|
| Name / Vorname einer Person | nicht leer, Person existiert noch nicht (Gross-/Kleinschreibung egal) | `Anna Meier` |
| Rechnungs-Nr. | nicht leer, noch nicht vorhanden (Gross-/Kleinschreibung egal) | `R-001` |
| Monat | Format `JJJJ-MM`, Monat 01–12 | `2026-11` |
| Betrag | positive Zahl, Punkt als Trennzeichen, max. 2 Dezimalstellen | `120.50` |
| Frist | Format `JJJJ-MM-TT`, gültiger Tag im Monat | `2026-11-30` |
| Kategorie / Person / Zahler | Auswahl über die angezeigte Nummer, nur vorhandene Einträge | `2` |
| Kategoriename | nicht leer, nicht doppelt (Gross-/Kleinschreibung egal) | `Strom` |
| Bezahlstatus | nur `offen` oder `bezahlt` | `bezahlt` |
| Löschen | Personen mit offenen Anteilen und Kategorien mit zugewiesenen Rechnungen können nicht gelöscht werden | – |
| Monatsauszug | gültiger Monat, bei vorhandener Datei Rückfrage zum Überschreiben | `2026-11` |

Beispiel aus `data/rechnungen_data.py` (Betragsprüfung):

```python
def betrag_gueltig(text):
    ...
    if anzahl_punkte > 1 or stellen_nach_punkt > 2:
        return False
    if text[0] == "." or text[-1] == ".":
        return False
    return float(text) > 0
```

### 3. Dateiverarbeitung

| Datei | Richtung | Inhalt |
|-------|----------|--------|
| `data/personen.txt` | lesen und schreiben | WG-Bewohner:innen, 5 Zeilen pro Person (ID, Name, Vorname, E-Mail, Telefon). |
| `data/kategorien.txt` | lesen und schreiben | Eine Kategorie pro Zeile. |
| `data/rechnungen.txt` | lesen und schreiben | Alle Rechnungen mit Personen, Bezahlstatus, Anteilen und bereits bezahlten Beträgen. |
| `auszug_JJJJ-MM.txt` | schreiben | Monatsauszug mit offenen Posten pro Person und Total (US12). |

Die Daten werden beim Programmstart geladen und nach jeder Änderung gespeichert. Fehlt eine Datei beim ersten Start (`FileNotFoundError`), startet das Programm trotzdem mit leeren Daten. Die Datei wird beim ersten Speichern neu angelegt. Weitere Dateifehler (`OSError`, `ValueError`) werden mit einer Fehlermeldung abgefangen.

Beispiel `kategorien.txt`:

```text
Essen
Miete
Strom
```

Beispiel `personen.txt` (eine Person):

```text
1
Meier
Anna
anna@example.ch
079 123 45 67
```

Beispiel `auszug_2026-11.txt`:

```text
Monatsauszug WG-Kostenteiler 2026-11
Erstellt am 2026-11-28
=========================================================================

Ben Huber
  Rechnung  Kategorie     Frist       Gegenüber                      CHF
  R-001     Strom         2026-11-30  an Anna Meier                33.33
  Total                                                              33.33
```

---

## ⚙️ Umsetzung

### Technologie

- Python 3.x
- Keine externen Bibliotheken (nur die Standardbibliothek)

### Aufteilung mit Rappen-Rest (US7)

Der Betrag wird in ganzen Rappen gerechnet, damit kein Rappen verloren geht.
Die ersten Personen erhalten je einen Rappen mehr, bis der Rest verteilt ist:

```text
100.00 CHF auf 3 Personen  →  33.34 / 33.33 / 33.33   (Summe = 100.00 CHF)
```

Beim Erfassen wird gewählt, wer die Rechnung bezahlt hat. Diese Person schuldet sich selbst nichts, ihr bereits bezahlter Betrag entspricht ihrem Anteil.

### Rechnung nachträglich bearbeiten (US8)

Rechnungs-Nr., Monat, Kategorie, Betrag und betroffene Personen können geändert werden. Dabei gelten dieselben Eingabeprüfungen wie beim Erfassen. Danach werden die Anteile neu berechnet und mit dem bereits Bezahlten verglichen:

```text
offener Betrag = Anteil − bereits bezahlt

> 0  →  offen          (Differenz muss noch bezahlt werden)
< 0  →  Guthaben       (die Person hat mehr bezahlt als ihr neuer Anteil)
= 0  →  ausgeglichen
```

Wird der Name einer Person geändert (Person bearbeiten), wird er automatisch in allen Rechnungen angepasst.

### Datenstruktur einer Rechnung

Rechnungen werden als Dictionary in `rechnungen_liste` gespeichert:

```python
{
    "nr": "R-001",
    "monat": "2026-11",
    "kategorie": "Strom",
    "betrag": 100.00,
    "personen": ["Anna Meier", "Ben Huber", "Cem Aydin"],
    "anteile": {"Anna Meier": 33.34, "Ben Huber": 33.33, "Cem Aydin": 33.33},
    "bezahlt_von": "Anna Meier",
    "bezahlt_betraege": {"Anna Meier": 33.34},
    "bezahlstatus": {"Anna Meier": "bezahlt", "Ben Huber": "offen", "Cem Aydin": "offen"},
    "frist": "2026-11-30"
}
```

### Repository-Struktur

```text
WG-Kostenteiler/
├── main.py                      # Hauptmenü, verknüpft user_interface, logic und data
├── data/
│   ├── personen.py              # US1, US2: WG-Bewohner:innen (personen.txt)
│   ├── kategorien.py            # US3, US4: Kategorien (kategorien.txt)
│   └── rechnungen_data.py       # US6, US8: Rechnungen erfassen/bearbeiten (rechnungen.txt)
├── logic/
│   ├── reminder.py              # US5: überfällige Rechnungen
│   └── rechnung_logic.py        # US7, US9: Aufteilung und Bezahlstatus
├── user_interface/
│   ├── rechnung_anzeigen.py     # US10: Rechnungen anzeigen und filtern
│   ├── statistik.py             # US11: Statistik nach Kategorie
│   └── export.py                # US12: Monatsauszug als Textdatei
└── README.md
```

Die Dateien `personen.txt`, `kategorien.txt` und `rechnungen.txt` liegen im Ordner `data/` und werden vom Programm selbst angelegt.

### Programm starten

1. Python 3 installieren (`python3 --version` prüfen).
2. Terminal im Ordner `WG-Kostenteiler/` öffnen. Die Rechnungsdatei wird relativ zu diesem Ordner gesucht.
3. Programm starten:

   ```bash
   python3 main.py
   ```

### Typischer Ablauf

1. **Personen** → *Person anlegen*: Mitbewohner:innen erfassen.
2. **Kategorien** → *Kategorie anlegen*: z. B. «Miete», «Strom».
3. **Rechnungen** → *Rechnung erfassen*: Nummer, Monat, Kategorie, Betrag, betroffene Personen, Zahler und Frist eingeben. Die Aufteilung wird sofort angezeigt.
4. **Rechnungen** → *Bezahlstatus bearbeiten*: Anteile als `bezahlt` markieren.
5. **Auswertungen**: Statistik pro Kategorie ansehen, überfällige Anteile prüfen oder den *Monatsauszug speichern*.

### Verwendete Bibliotheken

- `os`: Pfade zu den Datendateien und Prüfung, ob eine Datei existiert.
- `datetime` (`date`): heutiges Datum und Vergleich mit der Zahlungsfrist (Reminder), Datum im Monatsauszug.

Beide gehören zur Python-Standardbibliothek, eine Installation ist nicht nötig.

---

## ⚠️ Bekannte Einschränkungen

- **Kategorie umbenennen:** Bestehende Rechnungen behalten den alten Kategorienamen, sie werden nicht automatisch angepasst.
- **Namen eingeben:** Beim Bearbeiten des Bezahlstatus und beim Filtern nach Person muss der Name genau so eingegeben werden, wie er in der Rechnung steht (z. B. `Anna Meier`).
- **Startordner:** Das Programm muss im Ordner `WG-Kostenteiler/` gestartet werden, sonst findet es `data/rechnungen.txt` nicht.

---

## 👥 Team & Beiträge

| Name | Beitrag |
|------|---------|
| Enes Varol | US2 Personenstamm anzeigen/bearbeiten, US6 Rechnung erfassen, US10 Rechnungen anzeigen und filtern |
| Julian Erni | US4 Kategorien anzeigen/bearbeiten, US8 Rechnungen bearbeiten, US12 Monatsauszug |
| Kristina Stevic | US3 Kategorien anlegen, US7 Aufteilung mit Rappen-Rest, US11 Statistik |
| Piraveena Murugupillai | US1 Person anlegen, US5 Reminder, US9 Bezahlstatus bearbeiten |

## 📝 Lizenz

Dieses Projekt dient ausschliesslich Lernzwecken im Modul Grundlagen Programmierung (FHNW).
