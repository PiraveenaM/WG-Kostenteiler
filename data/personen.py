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
    Solange es noch keinen Bezahlstatus gibt (US9), gilt jeder Anteil als offen.
    Darum: Ist die Person bei einer Rechnung betroffen, hat sie offene Anteile."""
    ganzer_name = f"{bewohner['vorname']} {bewohner['name']}"
    for rechnung in rechnungen_data.rechnungen_liste:
        if ganzer_name in rechnung["personen"]:
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
