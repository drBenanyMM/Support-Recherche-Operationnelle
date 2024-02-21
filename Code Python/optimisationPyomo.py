from pyomo.environ import *

# Données du problème
usines = range(3)
produits = range(2)
capacite_usine = [10, 20, 15]
matieres_premieres = [7, 9]
main_oeuvre = [5, 8]
capacite_stockage = 50
profit_unitaire = [10, 12]

# Création du modèle Pyomo
model = ConcreteModel()

# Variables de décision
model.x = Var(produits, domain=NonNegativeReals)

# Fonction objectif
model.obj = Objective(expr=sum(profit_unitaire[i] * model.x[i] for i in produits), sense=maximize)

# Contraintes
model.capacity_constraints = ConstraintList()
for j in usines:
    model.capacity_constraints.add(sum(a[i, j] * model.x[i] for i in produits) <= capacite_usine[j])

model.matieres_premieres_constraint = Constraint(expr=sum(matieres_premieres[i] * model.x[i] for i in produits) <= B)

model.main_oeuvre_constraint = Constraint(expr=sum(main_oeuvre[i] * model.x[i] for i in produits) <= D)

model.capacity_stockage_constraint = Constraint(expr=sum(model.x[i] for i in produits) <= capacite_stockage)

# Résolution du modèle avec Gurobi
# solver = SolverFactory('gurobi')
# Résolution du modèle avec glpk
solver = SolverFactory('glpk')
results = solver.solve(model)

# Affichage de la solution
if 'ok' == str(results.Solver.status):
    for i in produits:
        print(f"Quantité de produit {i + 1} à fabriquer : {model.x[i].value}")
    print(f"Profit total : {model.obj()}")
else:
    print("Aucune solution optimale trouvée.")
