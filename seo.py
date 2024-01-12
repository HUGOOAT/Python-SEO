from collections import Counter
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

class SEOAnalyser:
    def __init__(self, url: str, motscles = []):
        self.url = url
        self.motscles = motscles
        self.motsparasites = []
        self.get_motsparasites()

    def occurence_mots(self, texte):
        mot = texte.lower().split()
        compte_mots = dict(sorted(Counter(mot).items(), key=lambda x: x[1], reverse=True))
        return compte_mots

    def suppression_mots(self, dictionnaire):
        for parasite in self.motsparasites:
            if parasite in dictionnaire:
                del dictionnaire[parasite]
        return dictionnaire

    def get_motsparasites(self):
        nomfichier = R"C:\Users\Administrateur\Documents\parasite.csv"
        with open(nomfichier, "r",) as fichiercsv:
            lecturecsv = csv.reader(fichiercsv)
            for row in lecturecsv:
                self.motsparasites.append(row[0])

    def removehtml(self, html):
        soup = BeautifulSoup(html, "html.parser")
        text_sansbalise = soup.get_text()
        return text_sansbalise

    def val_attribut(self, html, nom_balise, nom_attribut):
        soup = BeautifulSoup(html, "html.parser")
        balises = soup.find_all(nom_balise)
        valeur = [balise.get(nom_attribut) for balise in balises if balise.has_attr(nom_attribut)]
        return valeur

    def nombreimg(self, html, nom_balise):
        soup = BeautifulSoup(html, "html.parser")
        balises = len(soup.find_all(nom_balise))
        return balises

    def nomdomaine(self, url):
        urlcomplet = urlparse(url)
        nom_domaine = urlcomplet.netloc
        return nom_domaine

    def classedomaine(self, domain, urls):
        url_interne = []
        url_externe = []
        for url in urls:
            domaine_url = self.nomdomaine(url)
            if domaine_url == domain:
                url_interne.append(url)
            else:
                url_externe.append(url)
        return {"url_interne": url_interne, "url_externe": url_externe}

    def export_html(self, url):
        contenu = requests.get(url)
        return contenu.text

    def troismots(self, trimots):
        result = []
        for index, (mot, occurence) in enumerate(trimots.items()):
            if index < 3:
                result.append((mot))
            else:
                break
        return result

    def getUrlInterne(self, listeurl):
        nbinterne = len(listeurl['url_interne'])
        return nbinterne

    def getUrlExterne(self, listeurl):
        nbexterne = len(listeurl['url_externe'])
        return nbexterne

    def compteBalise(self, listebalise):
        nbBalise = len(listebalise)
        return nbBalise

    def comparateurmots(self, troismots):
        identique = 0
        for motcle in self.motscles:
            if motcle in troismots:
                identique = identique + 1
        if identique == 3:
            return "Oui"
        else:
            return "Non"

    def pourcentagealt(self, nombre_image, nombre_alt):
        if nombre_image == 0:
            return 0
        pourcentage = round((nombre_alt / nombre_image) * 100)
        pourcentage = str(pourcentage)
        pourcentage = pourcentage + "%"
        return pourcentage

    def analyse_seo(self):
        sortiehtml = self.export_html(self.url)
        htmltotext = self.removehtml(sortiehtml)
        motscles = self.occurence_mots(htmltotext)
        trimots = self.suppression_mots(motscles)
        troisPremiers = self.troismots(trimots)
        comparaison = self.comparateurmots(troisPremiers)
        rootdomain = self.nomdomaine(self.url)
        urlspresentes = self.val_attribut(sortiehtml, "a", "href")
        comparatif = self.classedomaine(rootdomain, urlspresentes)
        urlsinternes = self.getUrlInterne(comparatif)
        urlsexternes = self.getUrlExterne(comparatif)
        balisesalt = self.val_attribut(sortiehtml, "img", "alt")
        nbreimg = self.nombreimg(sortiehtml, "img")
        nombrebalise = self.compteBalise(balisesalt)
        pourcentage = self.pourcentagealt(nbreimg, nombrebalise)

        #Les prints ci-dessous sont laissés pour démontrer le fonctionnement du programme hors GUI
        print("trois premiers mots clés:", troisPremiers)
        print("Nombre d'URL internes:", urlsinternes)
        print("Nombre d'URL externes:", urlsexternes)
        print("Nombre de balises alt:", nombrebalise)
        print("Nombre d'images:", nbreimg)
        print("Pourcentage de image/alt", pourcentage)
        print("Resultat de la comparaison:", comparaison)

        return {
            "Trois mots les plus présents sur la page": troisPremiers,
            "Les 3 mots sont parmis vos mots renseignés": comparaison,
            "Nombre de liens internes sur la page": urlsinternes,
            "Nombre de liens externes sur la page": urlsexternes,
            "% de présence de balise alt pour balise img": pourcentage
        }
