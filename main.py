from data import ( 
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
        return

main()