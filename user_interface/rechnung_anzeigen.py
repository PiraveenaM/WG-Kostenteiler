# US10: Alle Rechnungen anzeigen & filtern (Enes Varol)
# Zeigt die Rechnungen aus data/rechnungen_data.py im Terminal an
# und kann sie nach Monat, Person oder Bezahlstatus filtern.

from data import rechnungen_data


def rechnung_ausgeben(rechnung):
    """Gibt eine einzelne Rechnung mit allen Angaben aus."""
    print("------------------------------")
    print(f"Rechnungs-Nr.: {rechnung['nr']}")
    print(f"Betrag:        {rechnung['betrag']:.2f} CHF")
    print(f"Kategorie:     {rechnung['kategorie']}")
    print(f"Monat:         {rechnung['monat']}")
    print("Personen und Bezahlstatus:")
    for person in rechnung["personen"]:
        print(f"  - {person}: {rechnung['bezahlstatus'][person]}")


def rechnungen_anzeigen(liste):
    """Gibt alle Rechnungen einer Liste aus, oder einen Hinweis, wenn sie leer ist."""
    if len(liste) == 0:
        print("Es sind keine Rechnungen vorhanden.")
        return

    for rechnung in liste: 
        rechnung_ausgeben(rechnung)
    print("------------------------------")
    print(f"Anzahl Rechnungen: {len(liste)}")


def alle_rechnungen_anzeigen():
    """Kriterium 1 + 4: Zeigt alle erfassten Rechnungen an."""
    print("\n=== Alle Rechnungen ===")
    rechnungen_anzeigen(rechnungen_data.rechnungen_liste)


def nach_monat_filtern():
    """Kriterium 2 + 3: Zeigt nur die Rechnungen eines Monats (JJJJ-MM) an."""
    monat = input("Monat (JJJJ-MM): ").strip()

    if not rechnungen_data.monat_gueltig(monat):
        print("Fehler: Ungültiges Format. Bitte den Monat als JJJJ-MM eingeben, z. B. 2026-11.")
        return

    gefiltert = []
    for rechnung in rechnungen_data.rechnungen_liste:
        if rechnung["monat"] == monat:
            gefiltert.append(rechnung)

    print(f"\n=== Rechnungen im Monat {monat} ===")
    rechnungen_anzeigen(gefiltert)


def nach_person_filtern():
      """Kriterium 2 + 3: Zeigt nur die Rechnungen an, bei denen eine Person betroffen ist."""
      name = input("Vorname und Name (z. B. Enes Varol): ").strip()

      if name == "":
          print("Fehler: Bitte einen Namen eingeben.")
          return

      gefiltert = []
      for rechnung in rechnungen_data.rechnungen_liste:
          for person in rechnung["personen"]:
              if person.lower() == name.lower():
                  gefiltert.append(rechnung)


      print(f"\n=== Rechnungen von {name} ===")
      rechnungen_anzeigen(gefiltert)
     


    