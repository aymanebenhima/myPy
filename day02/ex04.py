import json
import os

class Produit:
    def __init__(self, nom, prix, quantite):
        self.nom      = nom
        self.prix     = prix
        self.quantite = quantite

    def to_dict(self):
        return {"nom": self.nom, "prix": self.prix, "quantite": self.quantite}

    @classmethod
    def from_dict(cls, data):
        return cls(data["nom"], data["prix"], data["quantite"])

    def __str__(self):
        return f"{self.nom} — {self.prix:.2f} MAD x {self.quantite} units"


class GestionnaireStock:
    def __init__(self):
        self.inventaire: dict[str, Produit] = {}

    def ajouter(self, produit: Produit):
        self.inventaire[produit.nom] = produit
        print(f"[+] Added: {produit}")

    def supprimer(self, nom: str):
        if nom not in self.inventaire:
            print(f"[ERROR] Product '{nom}' not found")
            return
        del self.inventaire[nom]
        print(f"[-] Removed: {nom}")

    def afficher(self):
        if not self.inventaire:
            print("Stock is empty.")
            return
        for produit in self.inventaire.values():
            print(f"  {produit}")

    def sauvegarder_stock(self, fichier: str):
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump({nom: p.to_dict() for nom, p in self.inventaire.items()}, f, indent=4)
        print(f"[✔] Stock saved to '{fichier}'")

    def charger_stock(self, fichier: str):
        if not os.path.exists(fichier):
            print(f"[ERROR] File '{fichier}' not found")
            return
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.inventaire = {nom: Produit.from_dict(p) for nom, p in data.items()}
        print(f"[✔] Stock loaded from '{fichier}'")


# --- Run ---
stock = GestionnaireStock()

stock.ajouter(Produit("Laptop",  9999.99, 10))
stock.ajouter(Produit("Mouse",    199.99, 50))
stock.ajouter(Produit("Keyboard", 349.99, 30))

print("\n=== Inventaire ===")
stock.afficher()

stock.sauvegarder_stock("stock.json")

# Load into a fresh instance
stock2 = GestionnaireStock()
stock2.charger_stock("stock.json")

print("\n=== Loaded Inventaire ===")
stock2.afficher()

stock2.supprimer("Mouse")
print("\n=== After Removal ===")
stock2.afficher()
