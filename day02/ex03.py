"""
Exercice 3 : Simulateur de Compte Bancaire (Encapsulation)
Objectif : Protéger les données sensibles avec des attributs privés.

Classe CompteBancaire :

Attribut privé __solde.

Méthode deposer(montant) : Ajoute au solde si le montant est > 0.

Méthode retirer(montant) : Retire du solde seulement si les fonds sont suffisants, sinon affiche une erreur.

Utilisez un décorateur @property pour permettre de consulter le solde mais empêcher sa modification directe (compte.solde = 1000000 doit échouer).

"""

class CompteBancaire:
    def __init__(self, titulaire, solde_initial=0):
        self.titulaire = titulaire
        self.__solde   = solde_initial

    @property
    def solde(self):
        return self.__solde

    @solde.setter
    def solde(self, value):
        raise AttributeError("Direct modification of 'solde' is not allowed. Use deposer() or retirer().")

    def deposer(self, montant):
        if montant <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__solde += montant
        print(f"[+] Deposited {montant:.2f} MAD — Balance: {self.__solde:.2f} MAD")

    def retirer(self, montant):
        if montant <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if montant > self.__solde:
            print(f"[ERROR] Insufficient funds — Balance: {self.__solde:.2f} MAD")
            return
        self.__solde -= montant
        print(f"[-] Withdrawn {montant:.2f} MAD — Balance: {self.__solde:.2f} MAD")

    def __str__(self):
        return f"Account [{self.titulaire}] — Balance: {self.__solde:.2f} MAD"


# --- Run ---
compte = CompteBancaire("Youssef", 500)

print(compte)
compte.deposer(200)
compte.retirer(100)
compte.retirer(1000)

print(f"\nBalance via property: {compte.solde}")

try:
    compte.solde = 1000000
except AttributeError as e:
    print(f"[ERROR] {e}")

