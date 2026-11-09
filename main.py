from data import ( 
    personen,
    kategorien, 
    rechnungen
)
from logic import (
    reminder,
    personen_bearbeiten,
    kategorien_bearbeiten,
    rechnung_erfassen,
    rechnung_bearbeiten,
)
from user_interface import (
    rechnung_anzeigen, 
    statistik, 
    export
)

def menu_personen():
    print("Option 1: Person anlegen")
    print("Option 2: Person bearbeiten")
    print("Option 3: Personenliste anzeigen")
    print("Option 4: Zurück")
    Wahl_personen = input("Option ").strip()
    if Wahl_personen == "1":
        personen.person_anlegen()
    elif Wahl_personen == "2":
        personen.person_bearbeiten()
    elif Wahl_personen == "3":
        personen.personenliste()
    elif Wahl_personen == "4":
         main()
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
        else:
            print("Bitte gib eine gültige Zahl ein")
            main()
        return

main()