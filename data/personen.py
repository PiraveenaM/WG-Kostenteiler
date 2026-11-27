from data import rechnungen_data

# US1: WG-Bewohner:innen erfassen (Piraveena Murugupillai)
# Die Funktion erfasst die Stammdaten von WG-Bewohner:innen.
# Für jede Person werden Vorname, Name, E-Mailadresse und Telefonnummer gespeichert.
# Die erfassten Personen stehen danach für weitere Funktionen des
# WG-Kostenteilers zur Verfügung.

def wg_bewohner():
    name = input("Name: ").strip().title()
    vorname = input("Vorname: ").strip().title()
    email = input("E-Mail: ").strip().lower()
    telefon = input("Telefon ").strip()

    return {"name": name, 
            "vorname": vorname,
            "email": email,
            "telefon": telefon
            }

wg_bewohner_liste = []

def personen_anlegen():
    id_number = 1
    while True:
        answer = input("\nNeuen Bewohner erfassen? ").strip().lower()

        if answer == "ja":
            neuer_wg_bewohner = wg_bewohner()

            neuer_wg_bewohner["id"] = id_number
            id_number = id_number + 1

            wg_bewohner_liste.append(neuer_wg_bewohner)

            print("WG-Bewohner wurde gespeichert.")

        else:
            print("WG-Bewohner Liste komplett")
            break
    return

for wg_bewohner in wg_bewohner_liste:
    print("-------------------")
    print("ID:", wg_bewohner["id"])
    print("Vorname:", wg_bewohner["vorname"])
    print("Name:", wg_bewohner["name"])
    print("E-Mail:", wg_bewohner["email"])
    print("Telefon:", wg_bewohner["telefon"])


# US2 

def wg_bewohner_anzeigen():
    """Kriterium 1: Zeigt alle WG-Bewohner:innen mit ID, Vorname und Name an."""
    if len(wg_bewohner_liste) == 0:
        print("Es sind noch keine WG-Bewohner:innen erfasst.")
        return

    print("WG-Bewohner:innen:")
    for bewohner in wg_bewohner_liste:
        print(bewohner["id"], bewohner["vorname"], bewohner["name"])


def person_finden(vorname, name):
    """Sucht eine Person über Vorname und Name – Gross-/Kleinschreibung egal.
    Gibt das Dictionary der Person zurück oder None, wenn es sie nicht gibt."""
    for bewohner in wg_bewohner_liste:
        gleicher_vorname = bewohner["vorname"].lower() == vorname.strip().lower()
        gleicher_name = bewohner["name"].lower() == name.strip().lower()
        if gleicher_vorname and gleicher_name:
            return bewohner
    return None


def hat_offene_anteile(bewohner):
    """Kriterium 3: True, wenn die Person noch offene Anteile hat.
    Offen heisst: Die Person ist bei einer Rechnung betroffen
    und ihr Bezahlstatus ist noch "offen" (wird in US9 auf "bezahlt" gesetzt)."""
    ganzer_name = f"{bewohner['vorname']} {bewohner['name']}"
    for rechnung in rechnungen_data.rechnungen_liste:
        if ganzer_name in rechnung["personen"] and rechnung["bezahlstatus"][ganzer_name] == "offen":
            return True
    return False


def personen_löschen(vorname, name):
    """Kriterien 2–4: Löscht eine Person über Vorname und Name.
    Gibt True zurück, wenn gelöscht wurde, sonst False."""
    bewohner = person_finden(vorname, name)

    if bewohner == None:
        print(f"{vorname} {name} wurde nicht gefunden.")
        return False

    if hat_offene_anteile(bewohner):
        print(f"{bewohner['vorname']} {bewohner['name']} hat noch offene Anteile "
              "und kann nicht gelöscht werden.")
        return False

    wg_bewohner_liste.remove(bewohner)
    print(f"{bewohner['vorname']} {bewohner['name']} wurde gelöscht.")
    return True


def name_in_rechnungen_ersetzen(alter_name, neuer_name):
    """Ersetzt einen Namen in allen Rechnungen: in der Personenliste,
    beim Bezahlstatus, bei den Anteilen und bei bezahlt_von."""
    for rechnung in rechnungen_data.rechnungen_liste:

# Bereits bezahlte Beträge (aus US8) – gilt auch für entfernte Personen mit Guthaben
        if alter_name in rechnung["bezahlt_betraege"]:
            rechnung["bezahlt_betraege"][neuer_name] = rechnung["bezahlt_betraege"][alter_name]
            del rechnung["bezahlt_betraege"][alter_name]

        if alter_name in rechnung["personen"]:
            # Personenliste neu aufbauen, alter Name wird durch neuen ersetzt
            neue_liste = []
            for person in rechnung["personen"]:
                if person == alter_name:
                    neue_liste.append(neuer_name)
                else:
                    neue_liste.append(person)
            rechnung["personen"] = neue_liste

            # Bezahlstatus: Wert unter neuem Namen speichern, alten Eintrag löschen
            rechnung["bezahlstatus"][neuer_name] = rechnung["bezahlstatus"][alter_name]
            del rechnung["bezahlstatus"][alter_name]

            # Anteile (aus US7): gleich wie beim Bezahlstatus
            rechnung["anteile"][neuer_name] = rechnung["anteile"][alter_name]
            del rechnung["anteile"][alter_name]

        # Zahler (aus US7) ebenfalls umbenennen
        if rechnung["bezahlt_von"] == alter_name:
            rechnung["bezahlt_von"] = neuer_name


def personen_bearbeiten(vorname, name):
    """Ändert Vorname, Name, E-Mail und Telefon einer Person.
    Enter lässt einen Wert unverändert. Gibt True zurück, wenn gespeichert wurde."""
    bewohner = person_finden(vorname, name)

    if bewohner == None:
        print(f"{vorname} {name} wurde nicht gefunden.")
        return False

    print("Neue Angaben eingeben (Enter = unverändert lassen):")
    neuer_vorname = input(f"Vorname ({bewohner['vorname']}): ").strip().title()
    neuer_name = input(f"Name ({bewohner['name']}): ").strip().title()
    neue_email = input(f"E-Mail ({bewohner['email']}): ").strip().lower()
    neues_telefon = input(f"Telefon ({bewohner['telefon']}): ").strip()

    # Leere Eingabe = alter Wert bleibt
    if neuer_vorname == "":
        neuer_vorname = bewohner["vorname"]
    if neuer_name == "":
        neuer_name = bewohner["name"]
    if neue_email == "":
        neue_email = bewohner["email"]
    if neues_telefon == "":
        neues_telefon = bewohner["telefon"]

    # Gibt es den neuen Namen schon bei einer ANDEREN Person?
    andere_person = person_finden(neuer_vorname, neuer_name)
    if andere_person != None and andere_person != bewohner:
        print(f"Fehler: {neuer_vorname} {neuer_name} gibt es bereits.")
        return False

    # Namen auch in allen Rechnungen anpassen
    alter_ganzer_name = f"{bewohner['vorname']} {bewohner['name']}"
    neuer_ganzer_name = f"{neuer_vorname} {neuer_name}"
    if neuer_ganzer_name != alter_ganzer_name:
        name_in_rechnungen_ersetzen(alter_ganzer_name, neuer_ganzer_name)
        rechnungen_data.rechnungen_speichern()     # geänderte Rechnungen in die Datei schreiben

    # Neue Werte in der Person speichern
    bewohner["vorname"] = neuer_vorname
    bewohner["name"] = neuer_name
    bewohner["email"] = neue_email
    bewohner["telefon"] = neues_telefon

    print(f"{neuer_ganzer_name} wurde gespeichert.")
    return True
