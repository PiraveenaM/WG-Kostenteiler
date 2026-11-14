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


def wg_bewohner_anzeigen():
    if len(personen.wg_bewohner_liste)==0:
        print("Es sind noch keine WG-Bewohner:innen erfasst.")
        return

    print("WG-Bewohner:innen:")
    for bewohner in personen.wg_bewohner_liste:
        print(bewohner["id"], bewohner["vorname"], bewohner["name"])
