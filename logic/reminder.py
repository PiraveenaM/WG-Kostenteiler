from datetime import date
from data import rechnungen_data

# US5: Reminder für Überfällige Rechnungen (Piraveena Murugupillai)
# Die Funktion durchsucht alle erfassten Rechnungen nach abgelaufenen Fristen.
# Als überfällig gelten nur Rechnungsanteile, deren Frist überschritten ist
# und deren Bezahlstatus auf "offen" steht.
# Die überfälligen Rechnungsanteile werden nach Frist,
# Rechnungsnummer und Person sortiert und in der Konsole ausgegeben.

def zeige_ueberfaellige_rechnungen():
    
    # Heutiges Datum ermitteln
    heute = date.today()

    print(f"Heutiges Datum: {heute}")

    # Liste für überfällige Rechnungen
    ueberfaellige_rechnungen = []

    # Alle Rechnungen prüfen
    for rechnung in rechnungen_data.rechnungen_liste:

        frist = date.fromisoformat(rechnung["frist"])

        # Prüfen, ob die Frist überschritten ist
        if frist < heute:

            # Bezahlstatus jeder beteiligten Person prüfen
            for person, status in rechnung["bezahlstatus"].items():

                # Nur offene Anteile berücksichtigen
                if status == "offen":

                    offener_betrag = rechnung["anteile"][person]

                    if offener_betrag > 0:

                        ueberfaellige_rechnungen.append({
                            "nr": rechnung["nr"],
                            "monat": rechnung["monat"],
                            "kategorie": rechnung["kategorie"],
                            "frist": rechnung["frist"],
                            "person": person,
                            "betrag": offener_betrag,
                            "bezahlt_von": rechnung["bezahlt_von"]
                        })

    if len(ueberfaellige_rechnungen) == 0:
        print("\nKeine überfälligen Rechnungen vorhanden.")

    else:
        print("\nÜberfällige Rechnungen:")

        # Nach Frist, Rechnungsnummer und Person sortieren
        ueberfaellige_rechnungen.sort(
             key=lambda r: (
                 r["frist"], 
                 r["nr"],
                 r["person"]
            )
        )

        # Überfällige Rechnungsanteile ausgeben
        for rechnung in ueberfaellige_rechnungen:
            print("------------------------------")
            print("Rechnungsnummer:", rechnung["nr"])
            print("Monat:", rechnung["monat"])
            print("Kategorie:", rechnung["kategorie"])
            print("Frist:", rechnung["frist"])
            print("Person:", rechnung["person"])
            print("Bezahlt von:", rechnung["bezahlt_von"])
            print(f"Offener Betrag: CHF {rechnung['betrag']:.2f}")