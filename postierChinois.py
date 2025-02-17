from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import copy

#pip install networkx
#pip install matplotlib
#pip install numpy

#Création de la fenetre
fenetre = Tk()

#Définition de la plupart des variables globales
compteur_rep = 0
visible = False
listePoids = ""
alerte_var = ""
affiche_cycle_ou_erreur = StringVar()


############################################################################################################################################
# ZONE DE DEFINITION DU GRAPHE, modifiez son contenu à votre convenance (un graphe trop imposant ne sera pas pris en charge graphiquement) #
############################################################################################################################################


monGraphe =  {"A" : {"E" : 2, "F" : 3},
           "E" : {"C" : 3, "A" : 2},
           "C" : {"E" : 3, "D" : 1},
           "D" : {"C" : 1, "G" : 2},
           "F" : {"A" : 3, "B" : 1, "G" : 3, "H" : 2},
           "B" : {"F" : 1, "G" : 2},
           "G" : {"B" : 2, "D" : 2, "F" : 3, "H" : 2},
           "H" : {"F" : 2, "G" : 2}
}


#Un deuxième et un troisième graphe pour tester

# {"A" : {"E" : 2, "F" : 3},
#            "E" : {"C" : 3, "A" : 2, "I" : 1, "J": 4},
#            "C" : {"E" : 3, "D" : 1},
#            "D" : {"C" : 1, "G" : 2, "I" : 4, "J" : 1},
#            "F" : {"A" : 3, "B" : 1, "G" : 3, "H" : 2},
#            "B" : {"F" : 1, "G" : 2},
#            "G" : {"B" : 2, "D" : 2, "F" : 3, "H" : 2},
#            "H" : {"F" : 2, "G" : 2},
#            "I" : {"E" : 1, "D" : 4},
#            "J" : {"D" : 1, "E" : 3}
# }


# {"A" : {"B" : 2, "D" : 3, "F" : 5},
#            "B" : {"A" : 2, "C" : 2},
#            "C" : {"B" : 2, "E" : 3, "G" : 4, "F" : 3},
#            "D" : {"A" : 3, "E" : 1},
#            "E" : {"C" : 3, "D" : 1},
#            "F" : {"A" : 5, "C" : 3},
#            "G" : {"C" : 4}
# }


########################################################
# Définition de la classe GrapheSAE et de ses méthodes #
########################################################


import copy

""" Une classe Python pour creer et manipuler des graphes valués """
class GrapheSAE(object):
    
    def __init__(self, graphe_dict=None):
        """ initialise un objet graphe.
        Si aucun dictionnaire n'est
        créé ou donné, on en utilisera un
        vide
        """
        if graphe_dict == None:
            graphe_dict = {}
        self._graphe_dict = graphe_dict

    def aretes(self, sommet):
        """ retourne une liste de toutes les aretes d'un sommet"""
        return self._graphe_dict[sommet]

    def all_sommets(self):
        """ retourne tous les sommets du graphe """
        return self._graphe_dict.keys()

    def all_aretes(self):
        """ retourne toutes les aretes du graphe
        à partir de la méthode privée,_list_aretes, à définir
        plus bas.
        Ici on fera donc simplement appel à cette méthode.
        """
        return self.__list_aretes()


    def add_sommet(self, sommet):
        """ Si le "sommet" n'set pas déjà présent
        dans le graphe, on rajoute au dictionnaire
        une clé "sommet" avec une liste vide pour valeur.
        Sinon on ne fait rien.
        """
        if sommet not in self.all_sommets():
            self._graphe_dict[sommet] = set()


    def add_arete(self, arete, distance):
        """ l'arete est de type set, tuple ou list;
        Entre deux sommets il peut y avoir plus
        d'une arete (multi-graphe)
        """
        s1 = arete[0]
        s2 = arete[1]

        if s1 not in self._graphe_dict[s2] and s2 not in self._graphe_dict[s1]:
            self._graphe_dict[s2][s1] = distance
            self._graphe_dict[s1][s2] = distance


    def __list_aretes(self):
        """ Methode privée pour récupérers les aretes.
        Une arete est un ensemble (set)
        avec un (boucle) ou deux sommets.
        """
        aretes = []
        for som, in self._graphe_dict.keys():
            for art, dist in self.aretes(som).items():
                aretes.append([som, art, dist])
        return aretes

    def __iter__(self):
        """ on crée un itérable à partir du graphe"""
        self._iter_obj = iter(self._graphe_dict)
        return self._iter_obj

    def __next__(self):
        """ Pour itérer sur les sommets du graphe """
        return next(self._iter_obj)

    def __str__(self):
        res = "sommets: "
        for k in self._graphe_dict:
            res += str(k) + " "
        res += "\naretes: "
        for som, vois, dist in self.__list_aretes():
            res += str(som) + "-" + str(vois) + " : " + str(dist)
        return res
    
    def sommet_degre(self, sommet):
        return len(self.aretes(sommet))

    def list_degre(self):
        res = []
        liste_som = self.all_sommets()
        liste_tup = []
        for sommet in liste_som:
            liste_tup.append((sommet, self.sommet_degre(sommet)))

        for i in range(len(liste_som)):
            maxi = (None, -1)
            for tup in liste_tup:
                if tup[1] > maxi[1]:
                    maxi = tup
            
            liste_tup.remove(maxi)
            res.append(maxi)
        return res


    
    def verifie_connexe(self, s):

        pile = [s]
        dist = {}
        art_visites = []

        for i in (self.all_sommets()):
            dist[i] = (float('inf'))

        dist[s] = 0

        while(len(pile) > 0):
            #On dépile la pile on donnant a som la valeur sortante
            som = pile.pop(-1)

            voisins = self.aretes(som)

            for vois in voisins:
                if (som, vois) not in art_visites and (vois, som) not in art_visites:
                    art_visites.append((som, vois))

                    if dist[vois] == float('inf'):
                        dist[vois] = dist[som] + voisins[vois]
                        pile.append(vois)            

        return float('inf') not in dist



    def dijkstra(self, som):

        file = [som]
        dist = {}
        arbre = {}

        #on initialise toutes les distance à l'infini
        for i in (self.all_sommets()):
            dist[i] = (float('inf'))
            arbre[i] = []

        dist[som] = 0

        while len(file) > 0:

            #On commence par chercher le sommet le + proche
            som = None
            min_dist = float('inf')
            for s in file:
                if dist[s] < min_dist:
                    som = s
                    min_dist = dist[s]
            file.remove(som)

            for voisin, poids in self.aretes(som).items():
                if dist[voisin] > dist[som] + poids:
                    dist[voisin] = dist[som] + poids
                    arbre[voisin] = som
                    if voisin not in file:
                        file.append(voisin)

        return dist, arbre



    def relie_dijkstra(self, dep, arr):
        chemin = [arr]
        dist, arbre = self.dijkstra(dep)

        while chemin[-1] != dep:
            chemin.append(arbre[chemin[-1]])
        chemin.reverse()

        return chemin, dist[arr]



    def verifSiEulerien(self): # vérifie si graphe est eulérien
        estEulerien = True
        for i in self.list_degre():
            if i[1] % 2 != 0:
                estEulerien = False
        return estEulerien



    def verifSiSemiEulerien(self):
        estSemiEulerien = False
        nbNoeuds = 0
        for i in self.list_degre():
            if nbNoeuds <= 2:
                if i[1] % 2 == 1:
                    nbNoeuds = nbNoeuds + 1
        if(nbNoeuds == 2):
            estSemiEulerien = True
        return estSemiEulerien



    def rendreEulerien(self):

        nouveau_graphe = GrapheSAE(copy.deepcopy(self._graphe_dict))
        sommets_impairs = []

        for sommet in nouveau_graphe.all_sommets():
            if nouveau_graphe.sommet_degre(sommet) % 2 != 0:
                sommets_impairs.append(sommet)

        # On vérifie si le graphe est bien semi-eulerien (sinon le graphe de base sera renvoye)
        if len(sommets_impairs) == 2:
            # On ajoute les arêtes entre les deux sommets de degré impair, avec la distance la + courte possible
            sommet_depart = sommets_impairs[0]
            sommet_arrivee = sommets_impairs[1]

            distance = nouveau_graphe.relie_dijkstra(sommet_depart,sommet_arrivee)[1]
            nouveau_graphe.add_arete((sommet_depart, sommet_arrivee), distance)

            # Ajout graphique
            global listePoids
            if "'" + sommet_depart + "'" + " est lié à " + "'" + sommet_arrivee + "'" + " avec un poids de " + str(distance) + "\n\n" not in listePoids:
                listePoids += "'" + sommet_depart + "'" + " est lié à " + "'" + sommet_arrivee + "'" + " avec un poids de " + str(distance) + "\n\n"
            
            if "'" + sommet_arrivee + "'" + " est lié à " + "'" + sommet_depart + "'" + " avec un poids de " + str(distance) + "\n\n" not in listePoids:
                listePoids += "'" + sommet_arrivee + "'" + " est lié à " + "'" + sommet_depart + "'" + " avec un poids de " + str(distance) + "\n\n"
 
            global listeDefil
            listeDefil.pack_forget()
            listeDefil = Label(secondCadre, text=listePoids, fg="black", bg="white", font=("Arial", 12, "bold"))
            listeDefil.pack(side="left", padx=20)

            global alerte_var
            global compteur_rep
            if compteur_rep == 0:
                alerte_var += "⚠︎ Ce graphe est semi-eulérien, une arête entre " + sommet_depart + " et " + sommet_arrivee + " avec un poids de " + str(distance) + " a été rajoutée mais elle ne figure pas sur la représentation graphique."
                alerte = Label(espace_sous_bouton, text=alerte_var, fg="red", bg="white", font=("Arial",12,"bold"))
                alerte.pack_forget()
                alerte.pack()
                compteur_rep += 1
            



        return nouveau_graphe


    def fleury(self, som_dep):

        art_visites = [] #pour retrnir le chemin emprunté (et donc les aretes deja visitees)
        dist = 0 #pour calculer la distance parcourue sur le cycle
        som = som_dep
            
        while len(art_visites) < len(self.all_aretes())//2:#On s'arrete quand toutes les aretes ont été vsitées (sauf la derniere)
            vois, distance = self.meilleure_arete(som_dep, som, art_visites)

            if (distance == "BUG"):
                return "Le programme n'a pas trouvé de cycle eulerien", 0

            art_visites.append((som, vois))
            dist += distance
            som = vois

        return art_visites, dist
    

    
    def meilleure_arete(self, som_dep, som, art_vist):

        """création de trois listes, recensant respectivements les arêtes étant des ponts, 
        celles ramenant au départ et le reste. Il est préférable de ne pas utiliser les 
        ponts et de ne pas revenir au départ lors de l'algorithme, ces aretes seront 
        donc utilisées en cas de dernière necessité"""
        ponts = []
        depart = []
        valides = []

        #On crée une copie du graphe pour y faire des tests
        grCopie = copy.deepcopy(self._graphe_dict)

        #On supprime du graphe les arêtes déjà empruntées
        for art in art_vist:
            
            del grCopie [art[1]][art[0]]
            del grCopie [art[0]][art[1]]

        grCp = GrapheSAE(grCopie)

        #pour chaque voisin, on vérifie si il ramène au départ ou si c'est un isthme
        for vois, dist in list(grCp.aretes(som).items()):
            if (som, vois) not in art_vist and (vois, som) not in art_vist:
                if vois == som_dep:
                    depart.append((vois, dist))
                else:
                    grCopieCopie = copy.deepcopy(grCopie)
                    del grCopieCopie [vois][som]
                    del grCopieCopie [som][vois]
                    grCpCp = GrapheSAE(grCopieCopie)
                    if grCpCp.verifie_connexe(som) == False:
                        ponts.append((vois, dist))
                    else:
                        valides.append((vois, dist))

        if valides:
            meilleur = valides[0]
        elif ponts:
            meilleur = ponts[0]
        elif depart:
            meilleur = depart[0]
        else:
            meilleur = "BUG", "BUG"


        return meilleur


########################################################
# Main                                                 #
########################################################


def main(graphe, som_dep) : 

    assert type(graphe) == GrapheSAE

    if graphe.verifie_connexe(som_dep):

        graphe = graphe.rendreEulerien()

        if graphe.verifSiEulerien():
            euler = True

            return graphe.fleury(som_dep)

        else:
            print("Graphe impossible a traiter : il n'est pas eulerien")

    else:
        print("Graphe impossible a traiter : il n'est pas connexe")


def extraction(art, dist):
    nouv_chaine = ""
    for tup in art:
        nouv_chaine += tup[0] + " -> "
    nouv_chaine += art[0][0] +  "\nDistance totale parcouru: " + str(dist)
    return nouv_chaine


# Première fonction à être appelé
def pre_main():
    global affiche_cycle_ou_erreur
    global resultat
    graphe = monGraphe1
    som_dep = saisieDepart.get()
    som_dep = som_dep.capitalize()

    try:
        art, dist = main(graphe,som_dep)
        
    except KeyError:
        affiche_cycle_ou_erreur.set("Veuillez saisir un sommet valide")
        resultat.pack(side="top")
        fenetre.update()
        raise KeyError("Le sommet que vous avez désigné n'existe pas")
    
    except:
        raise ValueError("Une erreur inconnue de nos services de renseignement est survenue.")


    if art == "Le programme n'a pas trouvé de cycle eulerien" and dist == 0:
        affiche_cycle_ou_erreur.set("Le programme n'a pas trouvé de cycle eulerien")
        resultat.pack(side="top")
        fenetre.update()
    else:
        chaine = extraction(art, dist)
        affiche_cycle_ou_erreur.set(chaine)

        resultat.pack(side="top")
        fenetre.update()


monGraphe1 = GrapheSAE(monGraphe)


##########################################
# I. Définition de la fenetre et du menu #
##########################################



# Réglage de la taille de la fenetre et sa position
ecran_x = int(fenetre.winfo_screenwidth())
ecran_y = int(fenetre.winfo_screenheight())

fenetre_x = 1200
fenetre_y = 600

fenetre.minsize(1200, 700)

posX = (ecran_x // 2) - (fenetre_x // 2)
posY = (ecran_y // 2) - (fenetre_y // 2)

geo = "{}x{}+{}+{}".format(fenetre_x, fenetre_y, posX, posY)
fenetre.geometry(geo)



# Titre
fenetre.title("Odinewenzo 3000")
sous_titre = Label(fenetre, text="RÉSOLVEUR DU PROBLEME DU POSTIER CHINOIS", fg="black", bg="white", font=("Arial", 15, "bold"))

# Affichage du titre
sous_titre.pack(pady=20)

# Barre de menu
menu = Frame(fenetre, bg="black", relief="sunken")
menu.pack(side="top", fill="x")

espace_sous_menu = Frame(fenetre, bg="white")
espace_sous_menu.pack(side="top", fill="both")

# Contenu des boutons du menu
equipe = Label(espace_sous_menu, text="1A2 |  Ewen Jain \n1A2 |  Enzo Caz  \n1A2 |  Odin Rajic", fg="black", bg="white", font=("Arial",12,"bold"))
instructions = Label(espace_sous_menu, text="Ce problème remonte au début des années 1960, il fut créé par un mathématicien, Meigu Guan. \nCe problème consiste à trouver le plus court cycle qui passe au moins une fois par chaque sommet d'un graphe avant de revenir à son point d'origine.", fg="black", bg="white", font=("Arial",12,"bold"))
explications = Label(espace_sous_menu, text="1) On rend le graphe eulérien s'il est semi-eulérien \n2) On trouve le cycle eulérien à partir du sommet de départ ", fg="black", bg="white", font=("Arial",12,"bold"))

# Fonctions
def afficher_var(var):
        global visible

        if visible:
            # Si les éléments sont visibles, les retirer
            equipe.pack_forget()
            instructions.pack_forget()
            explications.pack_forget()
            visible = False
            fenetre.update()
        else:
            # Si les éléments ne sont pas visibles, les ajouter
            var.pack(side="left", pady=10, fill='y', expand=True)
            visible = True
            fenetre.update()

def quitter():
    fenetre.destroy()


# Definition des boutons du menu
b1 = Button(menu, text="LES MEMBRES DU GROUPE", relief="flat", fg="white", bg="black", command=lambda: afficher_var(equipe), font=("Arial",10,"bold"))
b1.pack(side="left", padx=50)

b2 = Button(menu, text="LE PROBLEME DU POSTIER CHINOIS", relief="flat", fg="white", bg="black", command=lambda: afficher_var(instructions), font=("Arial",10,"bold"))
b2.pack(side="left", padx=50)

b3 = Button(menu, text="QUITTER", relief="flat", fg="white", bg="black", command = quitter, font=("Arial",10,"bold"))
b3.pack(side="right", padx=50)

b4 = Button(menu, text="QU'AVONS-NOUS UTILISE ?", relief="flat", fg="white", bg="black", command=lambda: afficher_var(explications), font=("Arial",10,"bold"))
b4.pack(side="right", padx=50)


# Survol des boutons
def survol(event, widget):
    widget.config(fg="white", bg="grey")

def quitter(event, widget):
    widget.config(fg="white", bg="black")

b1.bind("<Enter>", lambda event: survol(event, b1))
b1.bind("<Leave>", lambda event: quitter(event, b1))

b2.bind("<Enter>", lambda event: survol(event, b2))
b2.bind("<Leave>", lambda event: quitter(event, b2))

b3.bind("<Enter>", lambda event: survol(event, b3))
b3.bind("<Leave>", lambda event: quitter(event, b3))

b4.bind("<Enter>", lambda event: survol(event, b4))
b4.bind("<Leave>", lambda event: quitter(event, b4))


fenetre.configure(bg="white")


############################################################################
# II. Affichage du cadre de saisie et du bouton de validation de la saisie #
############################################################################



cadreDepart = Frame(fenetre, bg="white")
espace_sous_bouton = Frame(fenetre, bg="white")


alerte = Label(espace_sous_bouton, text=alerte_var, fg="red", bg="white", font=("Arial",12,"bold"))
resultat = Label(espace_sous_bouton, textvariable=affiche_cycle_ou_erreur, fg="black", bg="white", font=("Arial",12,"bold"))
saisieDepart = Entry(cadreDepart, width=2, relief="groove", font=("Arial", 12, "bold"))
labelDepart = Label(cadreDepart, text="Saisir le point de départ: ", bg ="white", font=("Arial", 12, "bold"))
boutonDepart = Button(fenetre, text="Rechercher le cycle eulérien", bg = "black", fg="white", font=("Arial", 12, "bold"), relief="ridge", command=lambda: pre_main())

cadreDepart.pack(pady=(20,0))
labelDepart.pack(side="left")
saisieDepart.pack(side="left")
boutonDepart.pack(pady=(0,20))
espace_sous_bouton.pack(side="top", fill="both")


##########################################
# III. Définition et affichage du graphe #
##########################################


# 3.1) On définit les sommets à partir du graphe situé en ligne 12.
G = nx.Graph()
for sommet in monGraphe.keys():
    G.add_node(sommet)

# 3.2) On définit les arêtes à partir de ce même graphe, on créer aussi la liste des liaisons pondérées qui nous servira plus tard.

for sommet in monGraphe.keys():
    for arete in monGraphe[sommet]:
        p = monGraphe[sommet][arete] 
        G.add_edge(sommet, arete, Poids=p)
        listePoids += "'" + sommet + "'" + " est lié à " + "'" + arete + "'" + " avec un poids de " + str(p) + "\n\n"



# 3.3) Notre graphe est créé, à présent nous créons une figure Matplotlib et un canevas Tkinter pour l'afficher.
fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111)

nx.draw(G, with_labels=True, ax=ax, node_color="black", node_size = 1000, font_color="white", edge_color = "black", width = 2)

canvas = FigureCanvasTkAgg(fig, master=fenetre)
canvas.draw()


###########################################################################
# IV. Définition et affichage du cadre renseignant les liaisons pondérées #
###########################################################################


# 4.1) Définition d'un pré-cadre, le cadre le plus global.
preCadre = Frame(fenetre, bg="black")
preCadre.pack(side="left", padx=40)

presentationDefil = Label(preCadre, text="Consultez ici les liaisons (arêtes) et leur poids", fg="white", bg="black", font=("Arial", 12, "bold"))
presentationDefil.pack()

# 4.2) Définition de 2 cadres imbriqués qui permettent d'avoir une scrollbar.
cadrePoids = Frame(preCadre, bg="black")
cadrePoids.pack()

my_canva = Canvas(cadrePoids, bg="white")
my_canva.pack(side="left", fill="both")

scroll = ttk.Scrollbar(cadrePoids, orient=VERTICAL, command=my_canva.yview)
scroll.pack(side=RIGHT, fill=Y)

my_canva.configure(yscrollcommand=scroll.set)
my_canva.bind('<Configure>', lambda e: my_canva.configure(scrollregion = my_canva.bbox("all")))

secondCadre = Frame(my_canva, bg="white")
my_canva.create_window((0,0), window=secondCadre)

# Affichage des liaisons pondérées grâce à la liste créée précédemment.
listeDefil = Label(secondCadre, text=listePoids, fg="black", bg="white", font=("Arial", 12, "bold"))
listeDefil.pack(side="left", padx=20)

canvas.get_tk_widget().pack()

fenetre.mainloop()





