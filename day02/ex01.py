"""
Exercice 1 : Gestion d'une Bibliothèque (Héritage et Listes)
Objectif : Créer un système capable de gérer différents types de médias.

Classe de base Media : Attributs titre et auteur. Méthode afficher_infos().

Sous-classes Livre (page_count) et DVD (duree) : Elles héritent de Media et redéfinissent afficher_infos().

Classe Bibliotheque :

Un attribut contenu (liste d'objets Media).

Méthode ajouter(media) : Ajoute un livre ou un DVD.

Méthode lister_tout() : Affiche les détails de chaque élément en utilisant le polymorphisme.
"""
class Media:
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur

    def afficher_infos(self):
        return f"Titre: {self.titre}, Auteur: {self.auteur}"
    
class Livre(Media):
    def __init__(self, titre, auteur, page_count):
        super().__init__(titre, auteur)
        self.page_count = page_count

    def afficher_infos(self):
        return f"{super().afficher_infos()}, Pages: {self.page_count}"

class DVD(Media):
    def __init__(self, titre, auteur, duree):
        super().__init__(titre, auteur)
        self.duree = duree

    def afficher_infos(self):
        return f"{super().afficher_infos()}, Durée: {self.duree} minutes"

class Bibliotheque:
    def __init__(self):
        self.contenu = []

    def ajouter(self, media):
        self.contenu.append(media)

    def lister_tout(self):
        for media in self.contenu:
            print(media.afficher_infos())


# --- Run ---
lib = Bibliotheque()
lib.ajouter(Livre("Clean Code", "Robert C. Martin", 431))
lib.ajouter(Livre("The Pragmatic Programmer", "David Thomas", 352))
lib.ajouter(DVD("Inception", "Christopher Nolan", 148))
lib.ajouter(DVD("Interstellar", "Christopher Nolan", 169))

lib.lister_tout()