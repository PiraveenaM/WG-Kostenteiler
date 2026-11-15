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



def main():

    # US5: Überfällige Rechnungen beim Programmstart prüfen
    reminder.zeige_ueberfaellige_rechnungen()

    while True:
        print(f"\n=== WG-Kostenteiler ===")
        print("1. Rechnungen")
        print("2. Auswertungen")
        print("3. Personen")
        print("4. Kategorien")
        print("5. Menü verlassen")
        wahl = input("Wähle ein Menü: ").strip()

        if wahl == "1":
            menu_rechnungen()
        elif wahl == "2":
            menu_auswertungen()
        elif wahl == "3":
          menu_personen()
        elif wahl == "4":
            menu_kategorien()
        elif wahl == "5":
            print("Auf wiedersehen!")
            break
        else:
            print("Bitte gib eine gültige Zahl ein")

#Menü für Personen
def menu_personen():
    print("Option 1: Person anlegen")
    print("Option 2: Person löschen")
    print("Option 3: Personenliste anzeigen")
    print("Option 4: Zurück")
    wahl_personen = input("Option ").strip()
    if wahl_personen == "1":
        personen.personen_anlegen()
    elif wahl_personen == "2":
        vorname = input("Vorname der Person: ")
        name = input("Name der Person: ")
        personen.personen_löschen(vorname, name)
    elif wahl_personen == "3":
        personen.wg_bewohner_anzeigen()
    elif wahl_personen == "4":
        return
    else:
        print("Bitte geben Sie eine gültige Option an")
        menu_personen()
    return

#Menü für Kategorien
def menu_kategorien():
    while True:
        print("Option 1: Kategorie anlegen")
        print("Option 2: Kategorien anzeigen")
        print("Option 3: Kategorie umbenennen")
        print("Option 4: Kategorie löschen")
        print("Option 5: Zurück")
        wahl_kategorien = input("Option: ").strip()
        if wahl_kategorien == "1":
            kategorien.kategorie_anlegen()
        elif wahl_kategorien == "2":
            kategorien.kategorien_anzeigen()
        elif wahl_kategorien == "3":
            kategorien.kategorie_umbenennen()
        elif wahl_kategorien == "4":
            kategorien.kategorien_löschen()
        elif wahl_kategorien == "5":
            return
        else:
            print(f"'{wahl_kategorien}' ist keine gültige Option")
    
#Menü für Auswertungen
def menu_auswertungen():
    while True:
        print("Option 1: Statistik nach Kategorie")
        print("Option 2: Überfällige Rechnungen anzeigen")
        print("Option 3: Zurück")
        wahl_auswertungen = input("Option: ").strip()
        if wahl_auswertungen == "1":
            statistik.statistik_nach_kategorie()
        elif wahl_auswertungen == "2":
            reminder.zeige_ueberfaellige_rechnungen()
        elif wahl_auswertungen == "3":
            return
        else:
            print(f"'{wahl_auswertungen}' ist keine gültige Option")

#Menü für Rechnungen
def menu_rechnungen():
    print("Option 1: Rechnung erfassen")
    print("Option 2: Alle Rechnungen anzeigen")
    print("Option 3: Rechnungen nach Monat filtern")
    print("Option 4: Rechnungen nach Person filtern")
    print("Option 5: Rechnungen nach Status filtern")
    print("Option 6: Bezahlstatus bearbeiten")
    print("Option 7: Zurück")
    wahl_rechnungen = input("Option ").strip()
    if wahl_rechnungen == "1":
        rechnungen_data.rechnung_erfassen()
    elif wahl_rechnungen == "2":
        rechnung_anzeigen.alle_rechnungen_anzeigen()
    elif wahl_rechnungen == "3":
        rechnung_anzeigen.nach_monat_filtern()
    elif wahl_rechnungen == "4":
        rechnung_anzeigen.nach_person_filtern()
    elif wahl_rechnungen == "5":
        rechnung_anzeigen.nach_status_filtern()
    elif wahl_rechnungen == "6":
        rechnung_logic.bezahlstatus_bearbeiten()
    elif wahl_rechnungen == "7":
        return
    else:
        print("Bitte geben Sie eine gültige Option an")

if __name__ == "__main__":
    main()