import tkinter as tk
from tkinter import messagebox
from seo import SEOAnalyser

class Gui:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Analyseur SEO")
        self.resultats = None
        self.listeparasite = []
        self.get_listparasite()

        self.url_label = tk.Label(fenetre, text="URL:")
        self.url_entry = tk.Entry(fenetre, width=100)

        self.mots_label = tk.Label(fenetre, text="Mots clés (séparés par des espaces):")
        self.mots_entry = tk.Entry(fenetre, width=100)

        self.bouton_analyse = tk.Button(fenetre, text="Analyser", command=self.lancer_analyse)
        self.bouton_motparasite = tk.Button(fenetre, text="Paramètres", command=self.afficher_liste)

        self.url_label.pack()
        self.url_entry.pack()
        self.mots_label.pack()
        self.mots_entry.pack()
        self.bouton_analyse.pack()
        self.bouton_motparasite.pack()

    def lancer_analyse(self):
        url = self.url_entry.get()
        motscles = self.mots_entry.get().split(' ')

        analyseur = SEOAnalyser(url, motscles)
        self.resultats = analyseur.analyse_seo()
        fenetre_resultats = tk.Toplevel(self.fenetre)
        resultats_interface = ResultatsGui(fenetre_resultats, self.resultats)

    def get_listparasite(self):
        url = "None"
        motscles = None
        liste = SEOAnalyser(url, motscles)
        self.listeparasite = liste.get_motsparasites()
        return self.listeparasite

    def afficher_liste(self):
        fenetre_listeparasite = tk.Toplevel(self.fenetre)
        liste_interface = GuiList(fenetre_listeparasite, self.listeparasite, self)

    def update_listeparasite(self, new_listeparasite):
        self.listeparasite = new_listeparasite

class ResultatsGui:

    def __init__(self, fenetre, resultats):
        self.fenetre = fenetre
        self.fenetre.title("Résultats de l'analyse SEO")

        self.afficher_resultats(resultats)

    def afficher_resultats(self, resultats):
        for cle, valeur in resultats.items():
            label_cle = tk.Label(self.fenetre, text=f"{cle}:", width=50, anchor='w')
            label_cle.grid(sticky='w')

            entry = tk.Entry(self.fenetre, width=20)
            entry.insert(tk.END, valeur)
            entry.grid(sticky='w')

class GuiList:
    def __init__(self, fenetre, listeparasites, gui_instance):
        self.fenetre = fenetre
        self.listeparasites = listeparasites
        self.gui_instance = gui_instance
        self.fenetre.title("Modification des mots parasites")

        self.listbox = tk.Listbox(fenetre, width=70, height=10)
        self.listbox.pack(padx=10, pady=10)

        self.afficher_listeparasites(listeparasites)

        self.entry_mot = tk.Entry(fenetre, width=30)
        self.entry_mot.pack(pady=5)

        self.bouton_ajouter_mot = tk.Button(fenetre, text="Ajouter un mot", command=self.ajouter_mot)
        self.bouton_ajouter_mot.pack(pady=10)

        self.fenetre.protocol("WM_DELETE_WINDOW", self.on_close)
    def afficher_listeparasites(self, listeparasites):
        for mot in listeparasites:
            self.listbox.insert(tk.END, mot)

    def ajouter_mot(self):
        nouveau_mot = self.entry_mot.get()
        if nouveau_mot not in self.listeparasites:
            self.listbox.insert(tk.END, nouveau_mot)
            self.entry_mot.delete(0, tk.END)  # Effacer le texte après l'ajout
            self.listeparasites.append(nouveau_mot)
            self.gui_instance.update_listeparasite(self.listeparasites)
        else:
            messagebox.showinfo("Mot déjà présent", "Le mot est déjà dans la liste.")

    def on_close(self):
        self.gui_instance.update_listeparasite(self.listeparasites)
        self.fenetre.destroy()

if __name__ == "__main__":
    fenetre_principale = tk.Tk()
    interface = Gui(fenetre_principale)
    fenetre_principale.mainloop()
