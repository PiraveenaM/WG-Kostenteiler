import os

# US3: Kategorien anlegen (Kristina Stevic)
# Die Kategorien werden in einer Textdatei gespeichert (eine Kategorie pro Zeile),
# damit sie nach einem Neustart noch vorhanden sind.
# Die Datei liegt im selben Ordner wie dieses Modul (data/kategorien.txt).
DATEI = os.path.join(os.path.dirname(__file__), "kategorien.txt")

kategorien_liste = []


def kategorien_laden():
    """Liest alle Kategorien aus der Datei in die Liste."""
    kategorien_liste.clear()
    if not os.path.exists(DATEI):
        return  # beim allerersten Start gibt es die Datei noch nicht
    with open(DATEI, "r", encoding="utf-8") as datei:
        for zeile in datei:
            name = zeile.strip()
            if name != "":
                kategorien_liste.append(name)


def kategorien_speichern():
    """Schreibt die ganze Liste in die Datei (überschreibt den alten Inhalt)."""
    with open(DATEI, "w", encoding="utf-8") as datei:
        for name in kategorien_liste:
            datei.write(name + "\n")


def kategorie_existiert(name):
    """True, wenn es die Kategorie schon gibt – Gross-/Kleinschreibung egal."""
    for kategorie in kategorien_liste:
        if kategorie.lower() == name.lower():
            return True
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
            kategorien_speichern()
            print(f"Kategorie '{name}' wurde gespeichert.")
            return

        nochmal = input("Nochmals versuchen? (ja/nein): ").strip().lower()
        if nochmal != "ja":
            return


# Beim Importieren des Moduls werden die gespeicherten Kategorien geladen.
kategorien_laden()


if __name__ == "__main__":
    # Nur zum Testen: python -m data.kategorien
    kategorie_anlegen()
    print("Aktuelle Kategorien:", kategorien_liste)
