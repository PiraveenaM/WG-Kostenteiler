from data import ( 
    personen,
    kategorien, 
    rechnungen_data
)
from logic import (
    reminder,
    rechnung_logic
)
from user_interface import (
    rechnung_anzeigen, 
    statistik, 
    export
)

def menu_personen():
    print("Option 1: Person anlegen")
    print("Option 2: Person löschen")
    print("Option 3: Personenliste anzeigen")
    print("Option 4: Zurück")
    Wahl_personen = input("Option ").strip()
    if Wahl_personen == "1":
        personen.personen_anlegen()
    elif Wahl_personen == "2":
        vorname = input("Vorname der Person: ")
        name = input("Name der Person: ")
        personen.personen_löschen(vorname, name)
    elif Wahl_personen == "3":
        personen.wg_bewohner_anzeigen()
    elif Wahl_personen == "4":
        return
    else:
        print("Bitte geben Sie eine gültige Option an")
        menu_personen()
    return

def main():
    while True:
        print(f"\n=== WG-Kostenteiler ===")
        print("1. Rechnungen")
        print("2. Auswertungen")
        print("3. Personen")
        print("4. Kategorien")
        print("5. Menü verlassen")
        Wahl = input("Wähle ein Menü: ").strip()

        if Wahl == "1":
            menu_rechnungen()
        elif Wahl == "2":
            menu_auswertungen()
        elif Wahl == "3":
          menu_personen()
        elif Wahl == "4":
            menu_kategorien()
        elif Wahl == "5":
            print("Auf wiedersehen!")
            break
        else:
            print("Bitte gib eine gültige Zahl ein")


def menu_rechnungen():
    print("Option 1: Rechnung erfassen")
    print("Option 2: Zurück")
    wahl_rechnungen = input("Option ").strip()
    if wahl_rechnungen == "1":
        rechnungen_data.rechnung_erfassen()
    elif wahl_rechnungen =="2":
        return
    else:
        print("Bitte geben Sie eine gültige Option an")
if __name__ == "__main__":
    main()

