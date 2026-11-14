from datetime import date


def zeige_ueberfaellige_rechnungen():
    heute = date.today()

    print(f"Heutiges Datum: {heute}")

    ueberfaellige_anteile = []

    for rechnung in rechnungen_liste:

        frist = date.fromisformat(rechnung["frist"])

        if frist < heute:
            ueberfaellige_rechnungen.append(rechnung)

    if len(ueberfaellige_rechnungen) == 0:
        print("\nKeine überfälligen Rechnungen vorhanden.")

    else:
         print("\nÜberfällige Rechnungen:")

        ueberfaellige_rechnungen.sort(
             key=lambda r: (r["frist"], r["nr"])
        )


    # Sortierung nach Zahlungsfrist, Rechnungsnummer und Person
    ueberfaellige_anteile.sort(
        key=lambda a: (
            a["zahlungsfrist"],
            a["rechnungsnummer"],
            a["person"]
        )
    )

    # Ausgabe
    if len(ueberfaellige_anteile) == 0:
        print("\nKeine überfälligen Rechnungen vorhanden.")
    else:
        print("\nÜberfällige Rechnungen:")

        for anteil in ueberfaellige_anteile:
            print("------------------------------")
            print("Rechnungsnummer:", anteil["rechnungsnummer"])
            print("Kategorie:", anteil["kategorie"])
            print("Zahlungsfrist:", anteil["zahlungsfrist"])
            print("WG-Bewohner:", anteil["person"])
            print("Zahlungsempfänger:", anteil["zahlungsempfaenger"])
            print(f"Offener Betrag: CHF {anteil['betrag']:.2f}")