# US6: Rechnung erfassen (Enes Varol)
# Hier werden alle Rechnungen der WG gespeichert.
# Jede Rechnung ist ein Dictionary mit:
# nr, monat (JJJJ-MM), kategorie, betrag, personen (Liste mit Namen),
# bezahlstatus (Dictionary: Name -> "offen" oder "bezahlt"), frist (JJJJ-MM-TT),
# bezahlt_von (wer bezahlt hat) und anteile (Dictionary: Name -> Betrag, aus US7)

from data import kategorien
from data import personen
from logic import rechnung_logic

rechnungen_liste = []


def rechnung_existiert(nr):
    """True, wenn es die Rechnungs-Nr. schon gibt - Gross-/Kleinschreibung egal."""
    for rechnung in rechnungen_liste:
        if rechnung["nr"].lower() == nr.lower():
            return True
    return False


def rechnungsnummer_einlesen():
    """Fragt die Rechnungs-Nr. ab, bis sie gültig ist, und gibt sie zurück."""
    while True:
        nr = input("Rechnungs-Nr.: ").strip()

        if nr == "":
            print("Fehler: Die Rechnungs-Nr. darf nicht leer sein.")
        elif rechnung_existiert(nr):
            print(f"Fehler: Die Rechnungs-Nr. '{nr}' gibt es bereits.")
        else:
            return nr


def nur_ziffern(text):
    """True, wenn text nicht leer ist und nur aus Ziffern 0–9 besteht."""
    if text == "":
        return False
    for zeichen in text:
        if zeichen not in "0123456789":
            return False
    return True


def monat_gueltig(text):
    """True, wenn text ein Monat im Format JJJJ-MM ist, z. B. 2026-11."""
    if len(text) != 7 or text[4] != "-":
        return False

    jahr = text[0:4]
    monat = text[5:7]
    if not nur_ziffern(jahr) or not nur_ziffern(monat):
        return False

    return 1 <= int(monat) <= 12


def monat_einlesen():
    """Fragt den Monat ab, bis er im Format JJJJ-MM ist, und gibt ihn zurück."""
    while True:
        monat = input("Monat (JJJJ-MM): ").strip()

        if monat_gueltig(monat):
            return monat
        else:
            print("Fehler: Bitte den Monat im Format JJJJ-MM eingeben, z. B. 2026-11.")


def betrag_gueltig(text):
    """True, wenn text eine positive Zahl ist: Rappen mit Punkt, max. 2 Dezimalstellen."""
    if text == "":
        return False

    anzahl_punkte = 0
    stellen_nach_punkt = 0
    for zeichen in text:
        if zeichen == ".":
            anzahl_punkte = anzahl_punkte + 1
        elif zeichen in "0123456789":
            if anzahl_punkte == 1:
                stellen_nach_punkt = stellen_nach_punkt + 1
        else:
            return False          # Buchstabe, Komma, Minus usw.

    if anzahl_punkte > 1 or stellen_nach_punkt > 2:
        return False
    if text[0] == "." or text[-1] == ".":
        return False

    return float(text) > 0


def betrag_einlesen():
    """Fragt den Betrag ab, bis er gültig ist, und gibt ihn als Zahl zurück."""
    while True:
        betrag = input("Betrag in CHF: ").strip()

        if betrag_gueltig(betrag):
            return float(betrag)
        else:
            print("Fehler: Bitte eine positive Zahl eingeben, Rappen mit Punkt "
                  "und höchstens 2 Dezimalstellen, z. B. 120.50")


def kategorie_waehlen():
    """Zeigt alle Kategorien nummeriert an und lässt eine auswählen.
    Gibt den Namen der Kategorie zurück oder None, wenn es keine gibt."""
    if len(kategorien.kategorien_liste) == 0:
        print("Es gibt noch keine Kategorien. Bitte zuerst eine Kategorie anlegen.")
        return None

    print("Kategorien:")
    nummer = 1
    for kategorie in kategorien.kategorien_liste:
        print(f"  {nummer}. {kategorie}")
        nummer = nummer + 1

    while True:
        auswahl = input("Nummer der Kategorie: ").strip()

        if nur_ziffern(auswahl) and 1 <= int(auswahl) <= len(kategorien.kategorien_liste):
            return kategorien.kategorien_liste[int(auswahl) - 1]
        else:
            print(f"Fehler: Bitte eine Zahl von 1 bis {len(kategorien.kategorien_liste)} eingeben.")


def personen_waehlen():
    """Zeigt alle WG-Bewohner:innen nummeriert an und lässt eine oder mehrere auswählen.
    Gibt eine Liste mit den Namen zurück, z. B. ["Enes Varol", "Lara Meier"],
    oder None, wenn es keine Personen gibt."""
    if len(personen.wg_bewohner_liste) == 0:
        print("Es gibt noch keine WG-Bewohner:innen. Bitte zuerst Personen anlegen.")
        return None

    print("WG-Bewohner:innen:")
    nummer = 1
    for bewohner in personen.wg_bewohner_liste:
        print(f"  {nummer}. {bewohner['vorname']} {bewohner['name']}")
        nummer = nummer + 1

    gewaehlte_personen = []
    while True:
        auswahl = input("Nummer der Person (Enter = fertig): ").strip()

        if auswahl == "":
            if len(gewaehlte_personen) == 0:
                print("Fehler: Bitte mindestens eine Person wählen.")
            else:
                return gewaehlte_personen
        elif nur_ziffern(auswahl) and 1 <= int(auswahl) <= len(personen.wg_bewohner_liste):
            bewohner = personen.wg_bewohner_liste[int(auswahl) - 1]
            ganzer_name = f"{bewohner['vorname']} {bewohner['name']}"
            if ganzer_name in gewaehlte_personen:
                print(f"{ganzer_name} ist bereits gewählt.")
            else:
                gewaehlte_personen.append(ganzer_name)
                print(f"{ganzer_name} hinzugefügt.")
        else:
            print(f"Fehler: Bitte eine Zahl von 1 bis {len(personen.wg_bewohner_liste)} eingeben.")


def frist_gueltig(text):
    """True, wenn text ein Datum im Format JJJJ-MM-TT ist, z. B. 2026-11-30."""
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        return False

    jahr = text[0:4]
    monat = text[5:7]
    tag = text[8:10]
    if not nur_ziffern(jahr) or not nur_ziffern(monat) or not nur_ziffern(tag):
        return False

    if int(monat) < 1 or int(monat) > 12:
        return False

    # Maximale Anzahl Tage pro Monat (Februar mit 29, damit Schaltjahre gehen)
    tage_pro_monat = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= int(tag) <= tage_pro_monat[int(monat) - 1]


def frist_einlesen():
    """Fragt die Frist ab, bis sie im Format JJJJ-MM-TT ist, und gibt sie zurück."""
    while True:
        frist = input("Frist (JJJJ-MM-TT): ").strip()

        if frist_gueltig(frist):
            return frist
        else:
            print("Fehler: Bitte die Frist im Format JJJJ-MM-TT eingeben, z. B. 2026-11-30.")


def rechnung_erfassen():
    """Fragt alle Angaben einer Rechnung ab und speichert sie in rechnungen_liste."""
    print("\n--- Neue Rechnung erfassen ---")

    nr = rechnungsnummer_einlesen()
    monat = monat_einlesen()

    kategorie = kategorie_waehlen()
    if kategorie == None: 
        return

    betrag = betrag_einlesen()

    betroffene_personen = personen_waehlen()
    if betroffene_personen == None:
        return

    zahler = rechnung_logic.zahler_waehlen()          # US7: wer hat bezahlt?

    frist = frist_einlesen()

    # Bezahlstatus: Jede betroffene Person startet mit "offen" (für US5 und US9)
    bezahlstatus = {}
    for person in betroffene_personen:
        bezahlstatus[person] = "offen"

    neue_rechnung = {
        "nr": nr,
        "monat": monat,
        "kategorie": kategorie,
        "betrag": betrag,
        "personen": betroffene_personen,
        "bezahlstatus": bezahlstatus,
        "frist": frist,
        "bezahlt_von": zahler}

    
    rechnungen_liste.append(neue_rechnung)

    print(f"\nRechnung {nr} wurde gespeichert:")
    print(f" Monat:     {monat}")
    print(f" Kategorie: {kategorie}")
    print(f" Betrag:    {betrag:.2f} CHF")
    print(f" Personen: {betroffene_personen}")
    print(f" Frist:    {frist}")

    rechnung_logic.rechnung_aufteilen(neue_rechnung)   # US7: Anteile berechnen und anzeigen
    rechnungen_speichern()                             # in die Datei schreiben


# Speichern und Laden der Rechnungen (Datei data/rechnungen.txt)
# Aufbau pro Rechnung, jede Angabe auf einer eigenen Zeile (wie in Notebook S08):
#   nr, monat, kategorie, betrag, frist, bezahlt_von, Anzahl Personen,
#   danach pro Person 3 Zeilen: Name, Bezahlstatus, Anteil

DATEI = "data/rechnungen.txt"


def rechnungen_speichern():
    """Schreibt alle Rechnungen in die Datei (alter Inhalt wird überschrieben)."""
    with open(DATEI, "w", encoding="utf-8") as datei:
        for rechnung in rechnungen_liste:
            datei.write(rechnung["nr"] + "\n")
            datei.write(rechnung["monat"] + "\n")
            datei.write(rechnung["kategorie"] + "\n")
            datei.write(str(rechnung["betrag"]) + "\n")
            datei.write(rechnung["frist"] + "\n")
            datei.write(rechnung["bezahlt_von"] + "\n")
            datei.write(str(len(rechnung["personen"])) + "\n")
            for person in rechnung["personen"]:
                datei.write(person + "\n")
                datei.write(rechnung["bezahlstatus"][person] + "\n")
                datei.write(str(rechnung["anteile"][person]) + "\n")


def rechnungen_laden():
    """Liest alle Rechnungen aus der Datei in die Liste."""
    rechnungen_liste.clear()
    try:
        with open(DATEI, "r", encoding="utf-8") as datei:
            nr = datei.readline()
            while nr != "":                     # leere Zeile = Ende der Datei
                monat = datei.readline().rstrip("\n")
                kategorie = datei.readline().rstrip("\n")
                betrag = float(datei.readline())
                frist = datei.readline().rstrip("\n")
                bezahlt_von = datei.readline().rstrip("\n")
                anzahl = int(datei.readline())

                # Personen, Bezahlstatus und Anteile wieder aufbauen
                betroffene_personen = []
                bezahlstatus = {}
                anteile = {}
                for i in range(anzahl):
                    person = datei.readline().rstrip("\n")
                    betroffene_personen.append(person)
                    bezahlstatus[person] = datei.readline().rstrip("\n")
                    anteile[person] = float(datei.readline())

                rechnung = {
                    "nr": nr.rstrip("\n"),
                    "monat": monat,
                    "kategorie": kategorie,
                    "betrag": betrag,
                    "personen": betroffene_personen,
                    "bezahlstatus": bezahlstatus,
                    "frist": frist,
                    "bezahlt_von": bezahlt_von,
                    "anteile": anteile}
                rechnungen_liste.append(rechnung)

                nr = datei.readline()           # Nr. der nächsten Rechnung
    except FileNotFoundError:
        return      # beim allerersten Start gibt es die Datei noch nicht


# Beim Programmstart werden die gespeicherten Rechnungen geladen.
rechnungen_laden()
