# US7: Gerechte Aufteilung mit Rappen-Rest (Kristina Stevic)
# Der Betrag einer Rechnung wird gleichmässig auf die betroffenen Personen verteilt.
# Damit keine Rappen verloren gehen, wird in ganzen Rappen gerechnet.
# Beispiel: 100.00 CHF auf 3 Personen -> 33.34 / 33.33 / 33.33
# Die Anteile werden in der Rechnung unter "anteile" gespeichert
# (Dictionary: Name -> Betrag in CHF), die zahlende Person unter "bezahlt_von".
#
# NEU (für US8): Unter "bezahlt_betraege" wird gespeichert, wie viel jede Person
# schon bezahlt hat (Dictionary: Name -> Betrag in CHF). Daraus ergibt sich:
#   offener Betrag = Anteil - bereits bezahlt
#   > 0  -> offen,   < 0  -> Guthaben,   = 0  -> ausgeglichen

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


def offener_betrag(rechnung, person):
    """NEU (US8): Anteil minus bereits bezahlter Betrag einer Person.
    Positiv = offen, negativ = Guthaben, 0 = ausgeglichen.
    Funktioniert auch für Personen, die gar keinen Anteil (mehr) haben."""
    anteil = rechnung["anteile"].get(person, 0)
    bezahlt = rechnung["bezahlt_betraege"].get(person, 0)
    return round(anteil - bezahlt, 2)


def alle_namen(rechnung):
    """NEU (US8): Alle Personen mit Anteil ODER mit bereits bezahltem Betrag.
    Wer aus einer Rechnung entfernt wurde, aber schon bezahlt hat, ist hier auch dabei."""
    namen = list(rechnung["anteile"])
    for person in rechnung["bezahlt_betraege"]:
        if person not in namen:
            namen.append(person)
    return namen


def status_aktualisieren(rechnung):
    """NEU (US8): Setzt den Bezahlstatus aller betroffenen Personen neu:
    "offen", wenn noch etwas zu zahlen ist, sonst "bezahlt".
    Einträge mit 0 CHF bei bezahlt_betraege werden entfernt."""
    rechnung["bezahlstatus"] = {}
    for person in rechnung["personen"]:
        if offener_betrag(rechnung, person) > 0:
            rechnung["bezahlstatus"][person] = "offen"
        else:
            rechnung["bezahlstatus"][person] = "bezahlt"

    for person in list(rechnung["bezahlt_betraege"]):
        if rechnung["bezahlt_betraege"][person] == 0:
            del rechnung["bezahlt_betraege"][person]


def aufteilung_anzeigen(rechnung):
    """Kriterium 4: Gibt die Aufteilung pro Person in der Konsole aus.
    NEU (US8): zusätzlich, ob der Anteil offen, bezahlt oder ein Guthaben ist."""
    print(f"\n--- Aufteilung Rechnung {rechnung['nr']} ---")
    print(f"Bezahlt von: {rechnung['bezahlt_von']}")
    for person in alle_namen(rechnung):
        anteil = rechnung["anteile"].get(person, 0)
        offen = offener_betrag(rechnung, person)
        if offen > 0:
            info = f"offen {offen:.2f} CHF"
        elif offen < 0:
            info = f"Guthaben {-offen:.2f} CHF"
        else:
            info = "bezahlt"
        print(f"  {person:<25}{anteil:>10.2f} CHF   ({info})")

    total = 0
    for anteil in rechnung["anteile"].values():
        total = total + anteil
    print(f"  {'Total':<25}{total:>10.2f} CHF")


def rechnung_aufteilen(rechnung):
    """Berechnet die Anteile, speichert sie in der Rechnung und zeigt sie an.
    Wird beim Erfassen (US6) UND nach dem Bearbeiten (US8) aufgerufen.
    Wer die Rechnung bezahlt hat, schuldet sich seinen eigenen Anteil nicht:
    sein bezahlter Betrag ist darum immer gleich seinem (neuen) Anteil."""
    rechnung["anteile"] = betrag_aufteilen(rechnung["betrag"], rechnung["personen"])

    zahler = rechnung["bezahlt_von"]
    rechnung["bezahlt_betraege"][zahler] = rechnung["anteile"].get(zahler, 0)

    status_aktualisieren(rechnung)
    aufteilung_anzeigen(rechnung)


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
    try:

        aktueller_status = (
            gefundene_rechnung["bezahlstatus"][person]
        )

    except KeyError:

        print(
            "Fehler: Für diese Person existiert "
            "kein Bezahlstatus."
        )

        return

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

    # NEU (US8): Bezahlten Betrag passend zum Status setzen
    if neuer_status == "bezahlt":
        gefundene_rechnung["bezahlt_betraege"][person] = gefundene_rechnung["anteile"][person]
    elif person in gefundene_rechnung["bezahlt_betraege"]:
        del gefundene_rechnung["bezahlt_betraege"][person]

    # NEU: Änderung in die Datei schreiben, damit sie nach einem Neustart noch da ist
    rechnungen_data.rechnungen_speichern()

    # Erfolgsmeldung ausgeben
    print(
        f"Status von {person} wurde auf '{neuer_status}' geändert."
    )