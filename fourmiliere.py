import random
from enum import Enum
from matplotlib import pyplot as plt

from individu import Fourmi, Oeuf, Reine
from colorama import Fore,Style,init
init(autoreset=True)
class Colonie:
    def __init__(self, nb_fourmi_debut):
        self.population = []
        self.fourmi_mortes = []
        self.reine = Reine()

        for _ in range(int(nb_fourmi_debut)):
            self.population.append(Fourmi())

    def naissance(self):
        self.population.append(Fourmi())
        print("naissance")

    def mort(self):
        self.fourmi_mortes.append(self.population.pop(0))

    def reine_morte(self):
        self.reine = None

    def pop(self):
        return (len(self.population)+1)


class Saison(Enum):
    HIVER = 1
    ETE = 2
    PRINTEMPS = 3
    AUTOMNE = 4

# --------------------------------PARAMÈTRES------------------------------------------------------------------------
DUREE_HIVER = 92
DUREE_PRINTEMPS = 91
DUREE_ETE = 91
DUREE_AUTOMNE = 90

ANNEE = (
        DUREE_HIVER
        + DUREE_PRINTEMPS
        + DUREE_ETE
        + DUREE_AUTOMNE
)



DECALAGE_ANNEE = -183  # commencer en été


jours_famine = 0  # compteur de famine consécutive

tau_famine_oeufs = 7  # seuil après lequel les œufs meurent
reine_active = True  # True si la reine peut pondre


k = 10000
r = 0
tau = random.randint(21, 42)
j = 0
E_max = 10
mortalite = 0.00136

ini = 4

# --------------------------------JOURS------------------------------------------------------------------------
jours =6000
# -----------------------------------------------------------------------------------------------------------------




P = [0] * (jours + 1)
P[0] = ini + 1
oeufs = []

# ------------------------------------------GESTION DE LA NOURRITURE PAR SAISON-----------------------------------------------------------------------------------------------
stock_nourriture = 50 # mg, réserve initiale
colonie = Colonie(ini)
limite = True

def saison_actuelle(jour):
    j = (jour + DECALAGE_ANNEE) % ANNEE  # appliquer le décalage

    if j < DUREE_HIVER:
        return Saison.HIVER
    j -= DUREE_HIVER
    if j < DUREE_PRINTEMPS:
        return Saison.PRINTEMPS
    j -= DUREE_PRINTEMPS
    if j < DUREE_ETE:
        return Saison.ETE
    return Saison.AUTOMNE



def decision_apport(saison):
    """
    Retourne la quantité de nourriture donnée et la conommation par fourmi pour le jour 'jour'.
    Tu peux personnaliser selon la saison, stock, ou stratégie.
    """
    # Exemple : pas de nourriture en hiver, 2000 mg en été

    if saison == Saison.HIVER:
        return [10,1]  # hiver rude
    elif saison == Saison.ETE:
        return [150,2]  # été
    else:
        return [150,2]  # printemps/automne


def ponte_par_saison(saison):
    if saison == Saison.HIVER:
        return 0.0
    elif saison == Saison.PRINTEMPS:
        return 0.065
    elif saison == Saison.ETE:
        return 1.0
    else:  # AUTOMNE
        return 0.3



def ponte(oeufs):
    E_t = round(E_max * f_espace * ponte_par_saison(saison))
    nouveaux_oeufs = []
    for i in range(E_t):
        oeufs.append(Oeuf())
    for oeuf in oeufs:
        if oeuf.vieillir():
            colonie.naissance()
        else:
            nouveaux_oeufs.append(oeuf)
    return nouveaux_oeufs


# Boucle des jours
for t in range(jours):
    try:
      if not saison ==saison_actuelle(t):
          print(f"NOUVELLE SAISON {saison_actuelle(t)} jours: {t}")
    except:
        pass
    saison = saison_actuelle(t)

    # --- Nourriture totale disponible ---

    apport = decision_apport(saison)[0]
    conso_par_fourmi = decision_apport(saison)[1]
    nourriture_total = stock_nourriture  + apport
    # Calcul la quantité de nourriture qui doit être stocké pour l'hiver
    consommation_hiver = DUREE_HIVER* (decision_apport(Saison.HIVER)[1] * (colonie.pop() + len(oeufs) ))

    # --- Population maximale supportée par la nourriture ---
  #  P_max_nourriture = nourriture_totale / CONSO_PAR_FOURMI

    f_espace = max(0, 1 - colonie.pop() / k)



# Vérifie si la reine est encore en vie pour pondre les oeufs et ne pond pas d'oeuf si elle est affamé
    if colonie.reine is not None:
        if colonie.reine.f_vieillir() is None and colonie.reine.jours_sans_manger == 0:


    # Si la colonie à asser en réserve pour pouvoir survivre a l'hiver sans apport quotidien alors on peut pondre sionon non

          if stock_nourriture >= consommation_hiver:
            oeufs = ponte(oeufs)






        else:
            colonie.reine_morte()
    # -----------------------------------------------GESTION DE NOURRITURE-----------------------------------------------------------------
    consommation_possible = int(nourriture_total / conso_par_fourmi) # correspond au nombre dee fourmi qui peuvent manger
    if consommation_possible >= colonie.pop():

        stock_nourriture = nourriture_total - (colonie.pop() * conso_par_fourmi)
        for fourmi in colonie.population:
            fourmi.manger()

   #elif stock_nourriture ==0:
   #    mortes =[]
   #    colonie.population.sort(key=lambda f: f.jours_sans_manger, reverse=True)
   #    for i in range(colonie.pop() - 1):
   #        # Vérifie si les fourmis qui ne mange pas aujourd'hui meurt
   #        morte = colonie.population[i].affamer()
   #        if morte is not None:
   #            mortes.append(morte)
   #
   #        # Tue les fourmis affamées depuis 7 jours
   #
   #    for m in mortes:
   #        colonie.population.remove(m)

    else:




       # k = colonie.pop()
       # limite = False
        fourmi_nourries = consommation_possible

        #trie la colonie pour nourrir les plus affamées en premier
        colonie.population.sort(key=lambda f: f.jours_sans_manger, reverse = True)


        # Fait manger les fourmis affamées en commencent par la reine
        if colonie.reine is not None:
          if consommation_possible >= 1:
            colonie.reine.manger()
          else:
              colonie.reine.affamer()
        for i in range(int(fourmi_nourries - conso_par_fourmi)):
            colonie.population[i].manger()
        # Gestion des fourmies mortes
        mortes = []
        # Boucle dans la population a partir de la derniere fourmi nourrie jusqu'à la dernière fourmi
        for i in range(fourmi_nourries,colonie.pop() - 1):
            #Vérifie si les fourmis qui ne mange pas aujourd'hui meurt
            morte = colonie.population[i].affamer()
            if morte is not None:
                mortes.append(morte)

        # Tue les fourmis affamées depuis 7 jours

        for m in mortes:
            colonie.population.remove(m)


        stock_nourriture = 0
        if len(mortes) > 0:

            print(f"{Fore.RED}Morts par manque de nourriture jour: {t} nombre: {len(mortes)}  saison {saison} {k}{Style.RESET_ALL}")

    # --- Mortalité naturelle ---
    compteur1 = 0
    for fourmi in colonie.population:
        fourmi_morte = fourmi.f_vieillir()
        if fourmi_morte is not None:
            colonie.population.remove(fourmi_morte)
            compteur1+=1
    if compteur1 > 0:
      print(f"Morts naturels: {t} nombre: {compteur1} saison {saison}")


    # --- Mise à jour population ---
    P[t + 1] = max(0, colonie.pop())


plt.plot(P)
plt.xlabel("Jours")
plt.ylabel("Population")
plt.title("Simulation de croissance d'une fourmilière")
plt.grid()
plt.show()
