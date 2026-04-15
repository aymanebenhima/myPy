import json

inventaire = {
    "ordinateur": {
        "prix": 1200,
        "quantite": 5
    },
    "souris": {
        "prix": 150,
        "quantite": 20
    },
    "clavier": {
        "prix": 300,
        "quantite": 10
    },
    "ecran": { 
        "prix": 800,
        "quantite": 15
    }

}

def sauvegarder_stock(inventaire, fichier):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(inventaire, f, indent=4, ensure_ascii=False)

def charger_stock(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        # return json.load(f)
        return json.loads(f.read())

sauvegarder_stock(inventaire, "stock.json")

stock_charge = charger_stock("stock.json")

print(stock_charge)