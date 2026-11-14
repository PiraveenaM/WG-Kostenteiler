from datetime import date
from data import rechnungen_data

# US5: Reminder für Überfällige Rechnungen (Piraveena Murugupillai)
# Die Funktion durchsucht alle erfassten Rechnungen nach abgelaufenen Fristen.
# Rechnungen, deren Frist vor dem heutigen Datum liegt, werden als überfällig erkannt.
# Überfällige Rechnungen werden nach Frist und Rechnungsnummer sortiert
# und mit den wichtigsten Informationen in der Konsole ausgegeben. 

def zeige_ueberfaellige_rechnungen():
    
    # Heutiges Datum ermitteln
    heute = date.today()

    print(f"Heutiges Datum: {heute}")

    # Liste für überfällige Rechnungen
    ueberfaellige_rechnungen = []

    # Alle Rechnungen prüfen
    for rechnung in rechnungen_data.rechnungen_liste:

        frist = date.fromisoformat(rechnung["frist"])

        if frist < heute:
            ueberfaellige_rechnungen.append(rechnung)

    if len(ueberfaellige_rechnungen) == 0:
        print("\nKeine überfälligen Rechnungen vorhanden.")

    else:
        print("\nÜberfällige Rechnungen:")

        ueberfaellige_rechnungen.sort(
             key=lambda r: (r["frist"], r["nr"])
        )

        for rechnung in ueberfaellige_rechnungen:
            print("------------------------------")
            print("Rechnungsnummer:", rechnung["nr"])
            print("Monat:", rechnung["monat"])
            print("Kategorie:", rechnung["kategorie"])
            print("Frist:", rechnung["frist"])
            print(f"Betrag: CHF {rechnung['betrag']:.2f}")
            print("Beteiligte Personen:",
                  ", ".join(rechnung["personen"]))