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
