# US11: Statistik nach Kategorie (Kristina Stevic)
# Zeigt, wie viel Geld pro Kategorie ausgegeben wurde – als Tabelle im Terminal.
# Optional kann nach einem Monat (JJJJ-MM) gefiltert werden.

from data import rechnungen_data


def summen_pro_kategorie(monat):
    """Zählt die Beträge pro Kategorie zusammen.
    Ist monat leer (""), werden alle Rechnungen gezählt, sonst nur die des Monats.
    Gibt ein Dictionary zurück, z. B. {"Miete": 1800.0, "Einkauf": 203.45}."""
    summen = {}
    for rechnung in rechnungen_data.rechnungen_liste:
        if monat != "" and rechnung["monat"] != monat:
            continue                       # Rechnung gehört nicht zum gewählten Monat

        kategorie = rechnung["kategorie"]
        if kategorie in summen:
            summen[kategorie] = summen[kategorie] + rechnung["betrag"]
        else:
            summen[kategorie] = rechnung["betrag"]
    return summen


def tabelle_anzeigen(summen):
    """Kriterium 3: Gibt die Summen als Tabelle aus, grösster Betrag zuerst."""
    if len(summen) == 0:
        print("Es sind keine Rechnungen vorhanden.")
        return

    total = 0
    for betrag in summen.values():
        total = total + betrag

    zeilen = list(summen.items())          # z. B. [("Miete", 1800.0), ("Einkauf", 203.45)]
    zeilen.sort(key=lambda zeile: zeile[1], reverse=True)

    print(f"{'Kategorie':<20}{'Betrag CHF':>12}{'Anteil':>9}")
    print("-" * 41)
    for kategorie, betrag in zeilen:
        prozent = betrag / total * 100
        print(f"{kategorie:<20}{betrag:>12.2f}{prozent:>8.1f}%")
    print("-" * 41)
    print(f"{'Total':<20}{total:>12.2f}{100:>8.1f}%")


def statistik_nach_kategorie():
    """Kriterien 1–3: Fragt optional einen Monat ab und zeigt die Statistik."""
    while True:
        monat = input("Monat (JJJJ-MM) oder Enter für alle Monate: ").strip()

        if monat == "" or rechnungen_data.monat_gueltig(monat):
            break
        else:
            print("Fehler: Bitte den Monat im Format JJJJ-MM eingeben, z. B. 2026-11.")

    if monat == "":
        print("\n=== Ausgaben nach Kategorie (alle Monate) ===")
    else:
        print(f"\n=== Ausgaben nach Kategorie ({monat}) ===")

    summen = summen_pro_kategorie(monat)
    tabelle_anzeigen(summen)
