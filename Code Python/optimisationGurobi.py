import gurobipy as gp
from gurobipy import GRB

# Données du problème
usines = range(3)
produits = range(2)
capacite_usine = [10, 20, 15]
matieres_premieres = [7, 9]
main_oeuvre = [5, 8]
capacite_stockage = 50
profit_unitaire = [10, 12]

# Création du modèle
m = gp.Model("Maximisation_profit")

# Variables de décision
x = m.addVars(produits, name="x", vtype=GRB.CONTINUOUS)

# Fonction objectif
m.setObjective(gp.quicksum(profit_unitaire[i] * x[i] for i in produits), GRB.MAXIMIZE)

# Contraintes
m.addConstrs((gp.quicksum(a[i, j] * x[i] for i in produits) <= capacite_usine[j] for j in usines), name="capacite_usine")
m.addConstr(gp.quicksum(matieres_premieres[i] * x[i] for i in produits) <= B, name="matieres_premieres")
m.addConstr(gp.quicksum(main_oeuvre[i] * x[i] for i in produits) <= D, name="main_oeuvre")
m.addConstr(gp.quicksum(x[i] for i in produits) <= capacite_stockage, name="capacite_stockage")

# Résolution
m.optimize()

# Affichage de la solution
if m.status == GRB.OPTIMAL:
    for i in produits:
        print(f"Quantité de produit {i + 1} à fabriquer : {x[i].x}")
    print(f"Profit total : {m.objVal}")
else:
    print("Aucune solution optimale trouvée.")
