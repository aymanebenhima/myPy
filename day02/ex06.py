"""
Exercice : Le Système de Gestion de Parc Informatique (Asset Manager)
Contexte : Vous devez créer un outil pour un administrateur système qui gère un inventaire de serveurs. L'inventaire doit être sauvegardé de manière permanente dans un fichier.

1. La Classe Serveur
Créez une classe Serveur avec :

Attributs privés : __nom, __ip, et __etat (booléen : True si en ligne).

Propriétés : Utilisez @property pour lire le nom et l'IP, mais empêchez leur modification.

Méthodes :

allumer() / eteindre() : Change l'état du serveur.

to_dict() : Retourne une représentation du serveur sous forme de dictionnaire (utile pour le JSON).

2. La Classe Inventaire
Cette classe gère une liste d'objets Serveur et s'occupe de la persistance :

ajouter_serveur(serveur) : Ajoute un serveur à la liste.

sauvegarder(fichier_json) : Utilise le module json et un Context Manager (with) pour enregistrer tous les serveurs dans un fichier.

charger(fichier_json) : Lit le fichier, reconstruit les objets Serveur et les ajoute à l'inventaire.

3. Le Challenge (Robustesse)
Implémentez une gestion d'erreur (try/except) lors du chargement pour prévenir le cas où le fichier JSON serait corrompu ou absent (FileNotFoundError).
"""
import json
from pathlib import Path


class Serveur:
    def __init__(self, nom: str, ip: str, etat: bool = False):
        self.__nom = nom
        self.__ip = ip
        self.__etat = etat  # False = éteint, True = allumé

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def ip(self) -> str:
        return self.__ip
    
    @property
    def etat(self) -> bool:
        return self.__etat

    def allumer(self):
        self.__etat = True
        print(f"{self.__nom} is now ON.")

    def eteindre(self):
        self.__etat = False
        print(f"{self.__nom} is now OFF.")

    def to_dict(self) -> dict:
        return {
            "nom": self.__nom,
            "ip": self.__ip,
            "etat": self.__etat
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Serveur':
        return cls(
            nom=data["nom"],
            ip=data["ip"],
            etat=data["etat"]
        )
    
    def __str__(self) -> str:
        return f"{self.__nom} ({self.__ip}) - {'ON' if self.__etat else 'OFF'}"
    
class Inventaire:
    _BASE_DIR = Path(__file__).parent.resolve()

    def __init__(self):
        self.serveurs: list[Serveur] = []

    def _safe_path(self, fichier: Path) -> Path:
        path = (self._BASE_DIR / fichier.name).resolve()
        if not path.is_relative_to(self._BASE_DIR):
            raise ValueError(f"[ERROR] Access denied: '{fichier}' is outside the allowed directory.")
        return path

    def ajouter_serveur(self, serveur: Serveur):
        self.serveurs.append(serveur)
        print(f"[+] Added: {serveur}")

    def sauvegarder(self, fichier: Path):
        self._safe_path(fichier).write_text(
            json.dumps([s.to_dict() for s in self.serveurs], indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"[✔] Inventory saved to '{fichier.name}'")

    def charger(self, fichier: Path):
        try:
            self.serveurs = [Serveur.from_dict(s) for s in json.loads(self._safe_path(fichier).read_text(encoding="utf-8"))]
            print(f"[✔] Inventory loaded from '{fichier.name}'")
        except ValueError as e:
            print(e)
        except FileNotFoundError:
            print(f"[ERROR] File '{fichier.name}' not found.")
        except json.JSONDecodeError:
            print(f"[ERROR] File '{fichier.name}' is not valid JSON.")

# =========================
# TEST / RUN
# =========================

inventaire = Inventaire()

# Create servers
s1 = Serveur("Web-01", "192.168.1.10")
s2 = Serveur("DB-01", "192.168.1.20", True)

# Add to inventory
inventaire.ajouter_serveur(s1)
inventaire.ajouter_serveur(s2)

# Change states
s1.allumer()
s2.eteindre()

# Save inventory
inventaire.sauvegarder(Path("inventaire.json"))

print("\n--- Reload Inventory ---")

# Load into new inventory
nouvel_inventaire = Inventaire()
nouvel_inventaire.charger(Path("inventaire.json"))

# Display loaded servers
for serveur in nouvel_inventaire.serveurs:
    print(serveur)

print("\n--- Error Handling Tests ---")

# Missing file test
nouvel_inventaire.charger(Path("missing_file.json"))

# Corrupted JSON test
Path(__file__).parent.joinpath("corrupted.json").write_text("{ invalid json }", encoding="utf-8")

nouvel_inventaire.charger(Path("corrupted.json"))