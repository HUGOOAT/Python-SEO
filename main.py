###Etape 1:

#On importe le module "Counter" de "Collections", permettant de compter les occurences des mots.
from collections import Counter

#On définit notre variable
def occurence_mots(texte):
    #On séquence le texte en mots avec la fonction split, rattachée à "texte"
    mot = texte.lower().split()
    #On crée un dictionnaire qui associe les mots aux clés, et le compte aux valeurs,tri par occurence avec sorted.
    compte_mots = dict(sorted(Counter(mot).items(), key=lambda x: x[1], reverse=True))
    #On ordonne à la fonction de renvoyer le dictionnaire crée.
    return compte_mots

#Test de la fonction crée précédemment.
test = "La voiture est garée dans le garage de la maison, avec d'autres voitures dans le même garage"
#exemple = occurence_mots(test)
#print("Exemple fonction 1:", exemple)
#(on constate que les majuscules comptent comme de nouveaux mots, rajouter .lower à "texte" regle le pb.

###Etape 2
#On commence par creer la liste de mots parasites.
mots_parasites = ["le", "la", "les", "on", "des", "un", "une", "ma", "ta", "mes", "ton","votre","notre","tes",
                "de", "des"]

#On définit la fonction qui supprimera les mots parasites
def suppression_mots(dictionnaire: dict, listeparasites: list):
    #On passe sur chaque mot de la liste
    for parasite in listeparasites:
        #On regarde si un mot parasite est présent dans le dictionnaire
        if parasite in dictionnaire:
            #Si oui, on supprime le mot
            del dictionnaire[parasite]
    #On ordonne à la fonction de renvoyer le dictionnaire mis à jour.
    return dictionnaire

#Test de la fonction crée précédemment
#exemple2 = suppression_mots(exemple, mots_parasites)
#print("Exemple fonction 2:", exemple2)

###Etape 3
#On importe le module csv
import csv
#On définit notre fonction
def importcsv():
    nomfichier = R"C:\Users\hugod\Documents\parasite.csv"
    #On utlilise la fonction open pour ouvrir le fichier avec droits le lecture.
    with open(nomfichier, "r",) as fichiercsv:
        #On utlise l'import csv.reader pour lire le fichier depuis sa première ligne
        lecturecsv = csv.reader(fichiercsv)
        #On crée une variable qui récupère les entrées de chaque sous listes crées et les place dans une seule liste
        listeimport = [mot for sousliste in lecturecsv for mot in sousliste]
        return listeimport

#Test de la fonction crée précédemment
exemple3 = importcsv()
#print("Exemple fonction 3:", exemple3)
#La variable exemple3 n'est pas décommentée car elle est utilisée dans le programme final pour importer depuis un csv.
##Etape 4

#La fonction 3 renvoie bien une liste depuis le CSV, qu'il est possible de réintégrer dans la fonction 2:
#exemple22 = suppression_mots(exemple, exemple3)
#print("Exemple Etape 4, prenant la listeCSV crée par fonction 3:", exemple22)

##Etape 5

#On importe le module BeautifulSoup (Necessite l'execution de la commande "pip install beautifulsoup4"
from bs4 import BeautifulSoup
#On définit notre fonction
def removehtml(html: str):
    soup = BeautifulSoup(html, "html.parser")
    text_sansbalise = soup.get_text()
    return text_sansbalise

##Etape 6
#On définit notre fonction
def val_attribut(html, nom_balise, nom_attribut):
    soup = BeautifulSoup(html, "html.parser")
    balises = soup.find_all(nom_balise)
    valeur = [balise.get(nom_attribut) for balise in balises if balise.has_attr(nom_attribut)]
    return valeur

#Test de la fonction crée

html_test = ("""
<html>
    <body>
        <img class="classe1" src="" alt="alt1"/>
        <img class="classe2" src="" alt="alt2"/>
        <img class="classe3" src="" alt="alt3"/>
        <a href="/assest/href1">lorem ipsum</a>
        <a href="/assest/href2">lorem ipsum</a>
        <a href="/assest/href3">lorem ipsum</a>        
    </body>
</html>
""")

##Etape 7
#exemple6 = val_attribut(html_test, "img", "alt")
#exemple7 = val_attribut(html_test, "a", "href")
#print("Exemple Etape 7, balise img:", exemple6)
#print("Exemple Etape 7, balise a", exemple7)

##Etape 8
#On importe le module urlparse, qui permet de répondre à notre besoin.
from urllib.parse import urlparse

def nomdomaine(url):
    urlcomplet = urlparse(url)
    nom_domaine = urlcomplet.netloc
    return nom_domaine

#Test de la fonction définie:
#exemple8 = nomdomaine("https://www.nike.com/fr/t/chaussure-air-force-1-07-pour-VJhk3P/DV0788-001")
#print("Exemple fonction 8:", exemple8)

##Etape 9
def classedomaine(domain: str, urls: list):
    url_interne = []
    url_externe = []
    for url in urls:
        domaine_url = nomdomaine(url)
        if domaine_url == domain:
            url_interne.append(url)
        else:
            url_externe.append(url)
    return {"url_interne": url_interne, "url_externe":url_externe}
urltest = ["https://www.nike.com/fr/w/football-1gdj0", "https://www.nike.com/fr/w/cadeaux-3b0uf",
           "https://fr.wikipedia.org/wiki/Amazon"]



#Test fonction
#exemple9 = classedomaine("www.nike.com", urltest)
#print(exemple9)

##Etape 10
#On importe le module requests (Necessite d'effectuer 'pip install requests' au préalable)
import requests
#On définit notre fonction
def export_html(url):
    contenu = requests.get(url)
    return contenu.text

#Test de la fonction
#exemple10 = export_html("https://www.hdemarco.fr")
#print(exemple10)

##Etape 11
#On demande à l'utilisateur de rentrer l'URL de son choix:
url_input = input("Veuillez entrer une URL, au format https://... : ")
sortiehtml = export_html(url_input)
htmltotext = removehtml(sortiehtml)
motscles = occurence_mots(htmltotext)
trimots = suppression_mots(motscles, exemple3)
print("")
print("Voici les trois mots clés les plus utilisés sur la page:")
for index, (cle, valeur) in enumerate(trimots.items()):
    if index < 3:
        print(f"Mot : {cle}, Occurence : {valeur}")
    else:
        break
rootdomain = nomdomaine(url_input)
urlspresentes = val_attribut(sortiehtml, "a", "href")
comparatif = classedomaine(rootdomain, urlspresentes)
print("")
print("Autres statistiques:")
print(f"Nombre de liens internes: {len(comparatif['url_interne'])}")
print(f"Nombre de liens externes: {len(comparatif['url_externe'])}")
balisesalt = val_attribut(sortiehtml, "img", "alt")
print(f"Nombre de balises alt: {len(balisesalt)}")