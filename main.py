import tkinter as tk
from tkinter import messagebox
from seo import SEOAnalyser

class Gui:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Analyseur SEO")
        self.resultats = None

        self.url_label = tk.Label(fenetre, text="URL:")
        self.url_entry = tk.Entry(fenetre, width=100)

        self.mots_label = tk.Label(fenetre, text="Mots clés (séparés par des espaces):")
        self.mots_entry = tk.Entry(fenetre, width=100)

        self.bouton_analyse = tk.Button(fenetre, text="Analyser", command=self.lancer_analyse)

        self.url_label.pack()
        self.url_entry.pack()
        self.mots_label.pack()
        self.mots_entry.pack()
        self.bouton_analyse.pack()

    def lancer_analyse(self):
        url = self.url_entry.get()
        motscles = self.mots_entry.get().split(' ')

        analyseur = SEOAnalyser(url, motscles)
        self.resultats = analyseur.analyse_seo()
        fenetre_resultats = tk.Toplevel(self.fenetre)
        resultats_interface = ResultatsGui(fenetre_resultats, self.resultats)


class ResultatsGui:
    def __init__(self, fenetre, resultats):
        self.fenetre = fenetre
        self.fenetre.title("Résultats de l'analyse")

        self.afficher_resultats(resultats)

    def afficher_resultats(self, resultats):
        for cle, valeur in resultats.items():
            label = tk.Label(self.fenetre, text=f"{cle}: {valeur}")
            label.pack()

if __name__ == "__main__":
    fenetre_principale = tk.Tk()
    interface = Gui(fenetre_principale)
    fenetre_principale.mainloop()
