"""
Exercice 2 : Système de Paiement (Abstraction et Méthodes)
Objectif : Simuler une interface de paiement sécurisée.

Classe Paiement : Classe de base abstraite qui sert de modèle avec une méthode effectuer_paiement(montant).

Sous-classe CarteCredit : Demande un numéro de carte et vérifie si le montant est positif avant de "valider".

Sous-classe PayPal : Demande un email et simule une vérification de connexion.

Challenge : Créez une fonction traiter_achat(methode, montant) qui accepte n'importe quel objet de type Paiement et exécute la transaction.
"""

from abc import ABC, abstractmethod
import re

# --- Abstract Base ---
class Paiement(ABC):
    @abstractmethod
    def effectuer_paiement(self, montant):
        pass

    def _valider_montant(self, montant):
        if montant <= 0:
            raise ValueError(f"Invalid amount: {montant}")


# --- CarteCredit ---
class CarteCredit(Paiement):
    def __init__(self, numero_carte):
        if not re.fullmatch(r"\d{16}", numero_carte):
            raise ValueError("Card number must be 16 digits")
        self.numero_carte = f"**** **** **** {numero_carte[-4:]}"

    def effectuer_paiement(self, montant):
        self._valider_montant(montant)
        print(f"[CarteCredit] {self.numero_carte} — Payment of {montant:.2f} MAD validated.")


# --- PayPal ---
class PayPal(Paiement):
    def __init__(self, email):
        if "@" not in email:
            raise ValueError(f"Invalid email: {email}")
        self.email = email

    def _verifier_connexion(self):
        print(f"[PayPal] Connecting as {self.email}...")

    def effectuer_paiement(self, montant):
        self._valider_montant(montant)
        self._verifier_connexion()
        print(f"[PayPal] {self.email} — Payment of {montant:.2f} MAD validated.")


# --- Processor ---
def traiter_achat(methode: Paiement, montant):
    if not isinstance(methode, Paiement):
        raise TypeError("methode must be a Paiement instance")
    try:
        methode.effectuer_paiement(montant)
    except ValueError as e:
        print(f"[ERROR] Transaction failed: {e}")


# --- Run ---
carte  = CarteCredit("1234567812345678")
paypal = PayPal("user@example.com")

traiter_achat(carte,  250.00)
traiter_achat(paypal, 99.99)
traiter_achat(paypal, -50)     # invalid amount
# traiter_achat("invalid", 100) # invalid method