import os
from data import rechnungen_data

# US3: Kategorien anlegen (Kristina Stevic)
# Die Kategorien werden in einer Textdatei gespeichert (eine Kategorie pro Zeile),
# damit sie nach einem Neustart noch vorhanden sind.
# Die Datei liegt im selben Ordner wie dieses Modul (data/kategorien.txt).
DATEI = os.path.join(os.path.dirname(__file__), "kategorien.txt")

kategorien_liste = []


def kategorien_laden():
    """Liest alle Kategorien aus der Datei in die Liste."""
    kategorien_liste.clear()
    try:
        with open(DATEI, "r", encoding="utf-8") as datei:
            for zeile in datei:
                name = zeile.strip()
                if name != "":
                    kategorien_liste.append(name)
    except FileNotFoundError:
        pass  # beim allerersten Start gibt es die Datei noch nicht – das ist kein Fehler
    except OSError:
        print("Fehler: Die Kategorien konnten nicht geladen werden.")


def kategorien_speichern():
    """Schreibt die ganze Liste in die Datei (überschreibt den alten Inhalt).
    Gibt True zurück, wenn das Speichern geklappt hat, sonst False."""
    try:
        with open(DATEI, "w", encoding="utf-8") as datei:
            for name in kategorien_liste:
                datei.write(name + "\n")
    except OSError:
        print("Fehler: Die Kategorien konnten nicht gespeichert werden.")
        return False
    else:
        return True

def kategorie_existiert(name):
    """True, wenn es die Kategorie schon gibt – Gross-/Kleinschreibung egal."""
    for kategorie in kategorien_liste:
        if kategorie.lower() == name.lower():
            return kategorie
    return False


def kategorie_anlegen():
    """Fragt einen Namen ab, prüft ihn und speichert die neue Kategorie."""
    while True:
        name = input("Name der neuen Kategorie: ").strip()

        if name == "":
            print("Fehler: Ein leerer Name wird nicht übernommen.")
        elif kategorie_existiert(name):
            print(f"Fehler: Die Kategorie '{name}' gibt es bereits.")
        else:
            kategorien_liste.append(name)
            if kategorien_speichern():
                print(f"Kategorie '{name}' wurde gespeichert.")
            else:
                kategorien_liste.remove(name)   # nicht gespeichert -> auch nicht in der Liste behalten
            return

        nochmal = input("Nochmals versuchen? (ja/nein): ").strip().lower()
        if nochmal != "ja":
            return


#US 4

def kategorien_anzeigen():
    if len(kategorien_liste) == 0:
        print("Es sind noch keine Kategorien erfasst.")
        return

    print("Aktuelle Kategorien:")
    nummer = 1
    for kategorie in kategorien_liste:
        print(f"  {nummer}. {kategorie}")
        nummer = nummer + 1

#prüft, ob eine Kategorie noch Anteile zugewiesen hat
def kategorie_offene_anteile(kategorie):
    for rechnung in rechnungen_data.rechnungen_liste:
        if rechnung["kategorie"].lower() == kategorie.lower():
            return True
    return False

#löscht eine Kategorie und überprüft den Input + Suche, ob Kategorie noch offene Anteile hat
def kategorien_löschen():
    while True:
        name = input("Welche Kategorie soll gelöscht werden? ").strip()
        gefunden = kategorie_existiert(name)

        if name == "":
            print("Fehler: Ein leerer Name wird nicht übernommen.")
        elif gefunden == False:
            print(f"Die Kategorie '{name}' exisitiert nicht.")
        elif kategorie_offene_anteile(gefunden):
            print(f"Fehler: Die Kategorie '{name}' hat noch offene Rechnungen zugewiesen und kann nicht gelöscht werden.")
        else:
            kategorien_liste.remove(gefunden)
            if kategorien_speichern():
                print(f"Die Kategorie'{name}' wurde erfolgreich gelöscht.")
            else:
                kategorien_liste.append(gefunden)
            return
    
        nochmal = input("Nochmals versuchen? (ja/nein): ").strip().lower()
        if nochmal != "ja":
            return

#Umbennen-Funktion muss noch eingebaut werden
def kategorie_umbenennen():
    while True:
        alter_name = input("Welche Kategorie soll umbenannt werden? ").strip()
        gefunden = kategorie_existiert(alter_name)
    
        if alter_name == "":
            print("Fehler: Ein leerer Name wird nicht übernommen.")
        elif gefunden == False:
            print(f"Die Kategorie '{alter_name}' exisitiert nicht.")
        else: 
            kategorie_offene_anteile(gefunden)
            print(f"Warnung: Die Kategorie '{alter_name}' hat noch offene Anteile zugewiesen!")
            wahl = input("Fortfahren? (ja/nein): ").strip().lower()
            if wahl != "ja":
                return
            
            neuer_name = input("Wie lautet der neue Name? ").strip()
            kategorien_liste[kategorien_liste.index(gefunden)] = neuer_name
            if kategorien_speichern():
                print(f"Die Kategorie'{alter_name}' wurde erfolgreich geändert zu '{neuer_name}'.")
            else:
                kategorien_liste[kategorien_liste.index(neuer_name)] = gefunden
            return
        
        nochmal = input("Nochmals versuchen? (ja/nein): ").strip().lower()
        if nochmal != "ja":
            return




# Beim Importieren des Moduls werden die gespeicherten Kategorien geladen.
kategorien_laden()


if __name__ == "__main__":
     #Nur zum Testen: python -m data.kategorien
    kategorie_anlegen()
    print("Aktuelle Kategorien:", kategorien_liste)