from data import personen 


def wg_bewohner_anzeigen():
    if len(personen.wg_bewohner_liste)==0:
        print("Es sind noch keine WG-Bewohner:innen erfasst.")
        return

    print("WG-Bewohner:innen:")
    for bewohner in personen.wg_bewohner_liste:
        print(bewohner["id"], bewohner["vorname"], bewohner["name"])