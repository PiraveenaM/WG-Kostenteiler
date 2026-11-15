# US7: Gerechte Aufteilung mit Rappen-Rest (Kristina Stevic)
# Der Betrag einer Rechnung wird gleichmässig auf die betroffenen Personen verteilt.
# Damit keine Rappen verloren gehen, wird in ganzen Rappen gerechnet.
# Beispiel: 100.00 CHF auf 3 Personen -> 33.34 / 33.33 / 33.33
# Die Anteile werden in der Rechnung unter "anteile" gespeichert
# (Dictionary: Name -> Betrag in CHF), die zahlende Person unter "bezahlt_von".

from data import personen
from data import rechnungen_data


def betrag_aufteilen(betrag, betroffene_personen):
    """Kriterien 1–3: Teilt den Betrag gerecht auf die betroffenen Personen auf.
    Gibt ein Dictionary zurück, z. B. {"Anna Meier": 33.34, "Ben Huber": 33.33}."""
    anteile = {}
    anzahl = len(betroffene_personen)
    if anzahl == 0:
        return anteile

    rappen_total = round(betrag * 100)     # 100.00 CHF -> 10000 Rappen
    grundanteil = rappen_total // anzahl   # ganzzahlige Division: 10000 // 3 = 3333
    rest = rappen_total % anzahl           # übrig gebliebene Rappen: 10000 % 3 = 1

    nummer = 0
    for person in betroffene_personen:
        rappen = grundanteil
        if nummer < rest:
            rappen = rappen + 1            # die ersten Personen bekommen je 1 Rappen mehr
        anteile[person] = rappen / 100
        nummer = nummer + 1

    return anteile


def zahler_waehlen():
    """Kriterium 5: Zeigt alle WG-Bewohner:innen nummeriert an und lässt
    die Person wählen, welche die Rechnung bezahlt hat.
    Gibt den Namen zurück oder None, wenn es keine Personen gibt."""
    if len(personen.wg_bewohner_liste) == 0:
        print("Es gibt noch keine WG-Bewohner:innen. Bitte zuerst Personen anlegen.")
        return None

    print("Wer hat die Rechnung bezahlt?")
    nummer = 1
    for bewohner in personen.wg_bewohner_liste:
        print(f"  {nummer}. {bewohner['vorname']} {bewohner['name']}")
        nummer = nummer + 1

    while True:
        auswahl = input("Nummer der Person: ").strip()

        if rechnungen_data.nur_ziffern(auswahl) and 1 <= int(auswahl) <= len(personen.wg_bewohner_liste):
            bewohner = personen.wg_bewohner_liste[int(auswahl) - 1]
            return f"{bewohner['vorname']} {bewohner['name']}"
        else:
            print(f"Fehler: Bitte eine Zahl von 1 bis {len(personen.wg_bewohner_liste)} eingeben.")


def aufteilung_anzeigen(rechnung):
    """Kriterium 4: Gibt die Aufteilung pro Person in der Konsole aus."""
    print(f"\n--- Aufteilung Rechnung {rechnung['nr']} ---")
    print(f"Bezahlt von: {rechnung['bezahlt_von']}")
    for person in rechnung["anteile"]:
        print(f"  {person:<25}{rechnung['anteile'][person]:>10.2f} CHF")

    total = 0
    for anteil in rechnung["anteile"].values():
        total = total + anteil
    print(f"  {'Total':<25}{total:>10.2f} CHF")


def rechnung_aufteilen(rechnung):
    """Berechnet die Anteile, speichert sie in der Rechnung und zeigt sie an.
    Wer die Rechnung bezahlt hat, schuldet sich seinen eigenen Anteil nicht:
    sein Bezahlstatus wird darum direkt auf "bezahlt" gesetzt."""
    rechnung["anteile"] = betrag_aufteilen(rechnung["betrag"], rechnung["personen"])

    if rechnung["bezahlt_von"] in rechnung["bezahlstatus"]:
        rechnung["bezahlstatus"][rechnung["bezahlt_von"]] = "bezahlt"

    aufteilung_anzeigen(rechnung)

from data import rechnungen_data

# US9: Bezahlstatus bearbeiten (Piraveena Murugupillai)
# Die Funktion ermöglicht das Ändern des Bezahlstatus einer Person
# für eine bestehende Rechnung.
# Eine beteiligte Person kann zwischen den Statuswerten
# "offen" und "bezahlt" wechseln.
# Ungültige Rechnungsnummern, Personen oder Statuswerte
# werden mit einer Fehlermeldung abgefangen.

def bezahlstatus_bearbeiten():
    """Ändert den Bezahlstatus einer Person für eine Rechnung."""

    # Prüfen, ob überhaupt Rechnungen vorhanden sind
    if len(rechnungen_data.rechnungen_liste) == 0:
        print("Es sind keine Rechnungen vorhanden.")
        return

    # Rechnungsnummer einlesen
    nr = input("Rechnungsnummer: ").strip()

    # Passende Rechnung suchen
    gefundene_rechnung = None

    for rechnung in rechnungen_data.rechnungen_liste:
        if rechnung["nr"].lower() == nr.lower():
            gefundene_rechnung = rechnung
            break

    # Fehlermeldung, falls keine Rechnung gefunden wurde
    if gefundene_rechnung is None:
        print("Fehler: Rechnungsnummer nicht gefunden.")
        return

    # Beteiligte Personen mit aktuellem Status anzeigen
    print("\nBeteiligte Personen:")

    for person in gefundene_rechnung["personen"]:
        status = gefundene_rechnung["bezahlstatus"][person]
        print(f"- {person} ({status})")

    # Person auswählen
    person = input("\nPerson: ").strip()

    # Prüfen, ob Person an der Rechnung beteiligt ist
    if person not in gefundene_rechnung["personen"]:
        print("Fehler: Person nicht an dieser Rechnung beteiligt.")
        return

    # Aktuellen Status ermitteln
    aktueller_status = gefundene_rechnung["bezahlstatus"][person]

    print(f"Aktueller Status: {aktueller_status}")

    # Neuen Status einlesen
    neuer_status = input(
        "Neuer Status (offen/bezahlt): "
    ).strip().lower()

    # Gültigkeit des Status prüfen
    if neuer_status not in ["offen", "bezahlt"]:
        print("Fehler: Status muss 'offen' oder 'bezahlt' sein.")
        return

    # Status aktualisieren
    gefundene_rechnung["bezahlstatus"][person] = neuer_status

    # Erfolgsmeldung ausgeben
    print(
        f"Status von {person} wurde auf '{neuer_status}' geändert."
    )