import os
from datetime import date

from data import rechnungen_data
from logic import rechnung_logic

#Gibt ein Dictionary zurück: Name -> Liste von Posten.
#Personen ohne offene Beträge kommen nicht vor.
def offene_posten_sammeln(monat):
    """Gibt ein Dictionary zurück: Name -> Liste von Posten.
    Personen ohne offene Beträge kommen nicht vor."""
    posten_pro_person = {}
    for rechnung in rechnungen_data.rechnungen_liste:
        if rechnung["monat"] == monat:
            for person in rechnung_logic.alle_namen(rechnung):
                betrag = rechnung_logic.offener_betrag(rechnung, person)
                # Zahler schuldet sich selbst nichts, ausgeglichene Anteile sind kein Posten
                if person != rechnung["bezahlt_von"] and betrag != 0:
                    posten = {"nr": rechnung["nr"], "kategorie": rechnung["kategorie"],
                              "frist": rechnung["frist"], "zahler": rechnung["bezahlt_von"],
                              "betrag": betrag}
                    if person not in posten_pro_person:
                        posten_pro_person[person] = []
                    posten_pro_person[person].append(posten)
    return posten_pro_person

#Baut den Text des Auszugs als Liste von Zeilen auf.
def auszug_zeilen(monat, posten_pro_person):
    zeilen = [f"Monatsauszug WG-Kostenteiler {monat}", f"Erstellt am {date.today()}", "=" * 73]
    namen = list(posten_pro_person)
    namen.sort()
    for person in namen:
        posten_liste = posten_pro_person[person]
        posten_liste.sort(key=lambda p: (p["frist"], p["nr"]))
        zeilen.append("")
        zeilen.append(person)
        zeilen.append(f"  {'Rechnung':<10}{'Kategorie':<15}{'Frist':<12}{'Gegenüber':<24}{'CHF':>10}")
        total = 0
        for posten in posten_liste:
            if posten["betrag"] > 0:
                text = f"an {posten['zahler']}"
            else:
                text = f"Guthaben bei {posten['zahler']}"
            zeilen.append(f"  {posten['nr']:<10}{posten['kategorie']:<15}{posten['frist']:<12}"
                          f"{text:<24}{posten['betrag']:>10.2f}")
            total = total + posten["betrag"]
        zeilen.append(f"  {'Total':<61}{total:>10.2f}")
    return zeilen


def monatsauszug_speichern():
    monat = input("Monat (JJJJ-MM): ").strip()
    if not rechnungen_data.monat_gueltig(monat):
        print("Fehler: Bitte den Monat im Format JJJJ-MM eingeben, z. B. 2026-11.")
        return

    posten_pro_person = offene_posten_sammeln(monat)
    if len(posten_pro_person) == 0:
        print(f"Im Monat {monat} gibt es keine offenen Beträge. Es wurde keine Datei erstellt.")
        return

    dateiname = f"auszug_{monat}.txt"
    if os.path.exists(dateiname):
        print(f"Fehler: Die Datei '{dateiname}' ist bereits vorhanden.")
        antwort = input("Möchtest du sie überschreiben? (ja/nein): ").strip().lower()
        if antwort != "ja":
            print("Die Datei wurde nicht überschrieben.")
            return

    try:
        with open(dateiname, "w", encoding="utf-8") as datei:
            for zeile in auszug_zeilen(monat, posten_pro_person):
                datei.write(zeile + "\n")
    except OSError:
        print(f"Fehler: Die Datei '{dateiname}' konnte nicht gespeichert werden.")
    else:
        print(f"Der Auszug wurde als '{dateiname}' gespeichert.")
