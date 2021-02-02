from bs4 import BeautifulSoup
import requests
import pandas as pd

classement_bundesliga = ["bundesliga","https://www.matchendirect.fr/classement-foot/allemagne/classement-bundesliga-1.html"]
classement_ligue_1 = ["ligue_1","https://www.matchendirect.fr/classement-foot/france/classement-ligue-1.html"]
classement_serie_a = ["serie_a","https://www.matchendirect.fr/classement-foot/italie/classement-serie-a.html"]
classement_premier_league = ["premier_league","https://www.matchendirect.fr/classement-foot/angleterre/classement-barclays-premiership-premier-league.html"]
classement_liga = ["liga","https://www.matchendirect.fr/classement-foot/espagne/classement-primera-division.html"]
classement_championnats_url = [classement_bundesliga, classement_liga, classement_ligue_1, classement_serie_a, classement_premier_league]

def get_classement(url):
    r = requests.get(url[1])

    soup = BeautifulSoup(r.text, "html.parser")

    print("\n" + soup.find("title").text + "\n")

    table = soup.find("table", {"class": "table table-striped tableau_classement"})

    points = table.findAll("strong")
    equipes = table.findAll("td", {"class": "equipe"})
    lignes_classement = table.findAll("tr")
    del lignes_classement[1]

    championnat_master_list = []
    i=1
    for equipe in equipes:
        if i == 1:
            suffixe = "er"
        else:
            suffixe = "ème"
        stats = lignes_classement[i-1].findAll("td")
        data_dict = {}
        data_dict['classement'] = i
        data_dict['equipe'] = equipe.find("a").text
        data_dict['points'] = int(points[i-1].text)
        data_dict['journees'] = int(stats[2].text)
        data_dict['gagnes'] = int(stats[3].text)
        data_dict['nuls'] = int(stats[4].text)
        data_dict['perdus'] = int(stats[5].text)
        data_dict['buts_marques'] = int(stats[6].text)
        data_dict['buts_concedes'] = int(stats[7].text)
        championnat_master_list.append(data_dict)
        print(str(i) + suffixe + " : " + data_dict['equipe'] + " avec " + str(data_dict['points']) + " points")
        i+=1

    return championnat_master_list

def generate_classements_csv(classement_championnats_url):
    for classement_championnat in classement_championnats_url:
        df = pd.DataFrame(get_classement(classement_championnat))
        df.to_csv(classement_championnat[0]+ "/" + classement_championnat[0] + '_classement.csv', sep=';', index = False)

generate_classements_csv(classement_championnats_url)

