import networkx as nx
import matplotlib.pyplot as plt
import random
import json
from tkinter import *
from tkinter.filedialog import *

#===================================================================================================================================
#
#             ╭━━━╮╱╱╱╱╱╱╱╭╮╱╭━━━╮╱╱╱╱╱╱╱╱╱╱╭╮╱╭━━━━╮╱╱╱╱╱╭╮
#             ┃╭━╮┃╱╱╱╱╱╱╱┃┃╱┃╭━╮┃╱╱╱╱╱╱╱╱╱╱┃┃╱┃╭╮╭╮┃╱╱╱╱╱┃┃
#             ┃┃╱╰╋━┳━━┳━━┫╰━┫╰━━┳━━┳━━┳━┳━━┫╰━╋╯┃┃╰╋━━┳━━┫┃
#             ┃┃╭━┫╭┫╭╮┃╭╮┃╭╮┣━━╮┃┃━┫╭╮┃╭┫╭━┫╭╮┃╱┃┃╱┃╭╮┃╭╮┃┃
#             ┃╰┻━┃┃┃╭╮┃╰╯┃┃┃┃╰━╯┃┃━┫╭╮┃┃┃╰━┫┃┃┃╱┃┃╱┃╰╯┃╰╯┃╰╮
#             ╰━━━┻╯╰╯╰┫╭━┻╯╰┻━━━┻━━┻╯╰┻╯╰━━┻╯╰╯╱╰╯╱╰━━┻━━┻━╯
#             ╱╱╱╱╱╱╱╱╱┃┃
#             ╱╱╱╱╱╱╱╱╱╰╯
#
#   Projet réalisé dans le cadre de la seconde année de classe préparatoire intégrée de l'ISIMA
#
#   Intitulé du projet : Algorithme d’exploration en profondeur d'un réseau en présence de conflits entre plusieurs arêtes
#
#   Graph Search Tool © 2021 Théo Peuchlestrade and Loris Van Katwijk
#
#===================================================================================================================================

# Algorithme "Depth First Search"
#-------------- Code Récupéré, ou légerement modifié --------------
def dfs(graph, interdit, node, visited=[], closed=[], visited_edges=[]):
    visited.append(node) # On commence par rajouter le point actuel à la liste des points visités
    for k in sorted(graph[node]): # Pour chaque voisin du point

        #-------------- Code Personnel --------------
        if [node,k] not in closed and [k,node] not in closed: # si le lien avec ce voisin n'est pas fermé
            if k not in visited:            # Si le voisin n'a pas dejà été visité
                for (lien1,lien2) in interdit:
                    if node in lien1 and k in lien1:# Si le lien à une règle d'interdiction
                        closed.append(lien2)            # On ferme les liens qui deviennent incompatibles
                    elif node in lien2 and k in lien2:# Même chose pour que les interdictions soient symétriques
                        closed.append(lien1)
                visited_edges.append((node,k)) # On ajoute le lien aux liens visités

                #-------------- Code Récupéré, ou légerement modifié --------------
                dfs(graph, interdit, k, visited, closed, visited_edges) # On effectue le même algorithme pour le voisin.
    return visited_edges, closed

# Algorithme de génération aléatoire de graphes :
def randomGraph(nbNodes = 9):
    graph = {}  
    for i in range(1, nbNodes+1):   # On initialise le graphe
        graph[str(i)] = []
    for i in range(1, nbNodes+1):   # On génère alétoirement le voisinage de chaque noeud
        rge = list(range(1, nbNodes+1)) # On génère la liste des noeuds
        rge.remove(i) # On lui retire le noeud courant
        listeNoeudsAleatoires = random.sample(rge, random.randint(1, nbNodes//2)) # On prend un échantillon de noeuds parmi la liste de taille aleatoire
        for j in listeNoeudsAleatoires:
            if (str(j) not in graph[str(i)]): # si l'arete (i,j) n'existe pas on la rajoute a la liste des voisins de i
                graph[str(i)].append(str(j))
        for j in listeNoeudsAleatoires:
            if (str(i) not in graph[str(j)]): # si l'arete (j,i) n'existe pas on la rajoute a la liste des voisins de j
                graph[str(j)].append(str(i))
    for i in range(1, nbNodes+1):   # On trie les voisins
        graph[str(i)].sort()
    return graph

# Algorithme de génération aléatoire d'interdictions entre les noeuds :
def randomInterdits(graph, interditMin=1, interditMax=4):
    interdit = []
    for i in range(random.randint(interditMin,interditMax)):    # On génère une liste d'interdits de manière aléatoire
        noeudAleatoire = str(random.randint(1,len(graph))) # On prend un noeud aleatoire
        (a,b) = (noeudAleatoire,graph[noeudAleatoire][random.randint(0,len(graph[noeudAleatoire])-1)]) # On prend (a,b) une arête alétoire partant du noeud 
        (c,d) = (a,b) # On crée une deuxieme arête
        while (c,d)==(a,b) or (c,d)==(b,a): # On reprend une arête aléatoire tant que que les arêtes sont identiques
            noeudAleatoire = str(random.randint(1,len(graph)))
            (c,d) = (noeudAleatoire,graph[noeudAleatoire][random.randint(0,len(graph[noeudAleatoire])-1)])
        interdit.append( (sorted((str(a),str(b))), sorted((str(c),str(d))) )) # On trie les noeuds des arêtes et on les ajoute à la liste des incompatibilités
    return interdit

# Algorithme affichant un graphe pourvu de ses spécificités :
def afficheGraph(graph, debut=1):
    plt.figure()

    G = nx.Graph()  # Intégration du graphe dans NetworkX
    for i in graph:
        G.add_node(i) # On intègre les noeuds
    for i in graph:
        for j in graph[i]:
            G.add_edge(i,j) # On intègre les arêtes

    pos = nx.spring_layout(G, seed=6)  # Position des noeuds pour l'affichage
    
    nx.draw(G, with_labels=True, pos=pos, font_weight='bold', node_color='#309eff') # Affiche le graphe
    nx.draw_networkx_nodes( # Affiche le noeud de debut en vert
        G,
        pos,
        nodelist=[debut],
        node_color='g' # Vert
    )
    plt.show() # On affiche la fenetre


# Affiche le graph avec le chemin emprunté par l'algorithme DFS
def afficheDfs(graph, interdictions, debut, dfs):
    (visited_edges, closed) = dfs # On recupere les données du dfs
    plt.figure()

    G = nx.Graph()  # Intégration du graphe dans NetworkX
    for i in graph:
        G.add_node(i) # On intègre les noeuds
    for i in graph:
        for j in graph[i]:
            G.add_edge(i,j) # On intègre les arêtes

    pos = nx.spring_layout(G, seed=6) # Position des noeuds pour l'affichage

    nx.draw(G, with_labels=True, pos=pos, font_weight='bold', node_color='#309eff') # Affiche le graphe

    nx.draw_networkx_edges( # Affiche les arrêtes interdites en rouge
        G,
        pos,
        edgelist=closed, # Selection des arêtes interdites
        width=4,
        alpha=0.5,
        edge_color="r", # Couleur d'arête en rouge
    )

    nx.draw_networkx_edges( # Affiche les arrêtes visitées en vert
        G,
        pos,
        edgelist=visited_edges, # Selection des arêtes visités
        width=4,
        alpha=0.5,
        edge_color="g", # Couleur d'arête en vert
    )

    nx.draw_networkx_nodes( # Affiche les noeuds non visités en rouge
        G,
        pos,
        nodelist=[x for x in graph if (not x in [y for (a,y) in visited_edges] and x != debut)], # Selection des noeuds non visités
        node_color='r' # Couleur des noeuds en rouge
    )

    nx.draw_networkx_nodes( # Affiche le noeud de debut en vert
        G,
        pos,
        nodelist=[debut],
        node_color='g' # Vert
    )

    nx.draw_networkx_edge_labels( # Affiche les numero des liens
        G,
        pos,
        edge_labels={visited_edges[i]:i+1 for i in range(len(visited_edges))}, # Labels pour les arêtes
        rotate = False,
        horizontalalignment='right',
        bbox = {"alpha":0} # Pas de cadre
    )

    with open("result.json", 'w') as f: 
        f.write(json.dumps({"visited_edges":visited_edges,"closed":closed})) # On sauvegarde les resultat du dfs dans un fichier JSON
        f.close()
    plt.show()


# Algorithme récupérant les différentes informations d'un graphe écrites dans un fichier .json :
def graphFromJson(path):
    global graphSelect
    global interditSelect 
    global departSelect
    with open(path) as f: 
        x = json.loads(f.read().replace('\n', '')) # On ouvre le fichier JSON
    if ("depart" in x):
        (graphSelect,interditSelect, departSelect) = (x["graph"], x["interdits"], x["depart"]) # On récupère les données du graphe, les interdictions au sein de celui-ci ainsi que le point de départ de la résolution de ce dernier.
    else:
        (graphSelect,interditSelect, departSelect) = (x["graph"], x["interdits"], '1')


# Algorithme utilisant un graphe généré alétoirement en convertissant ses spécificités en texte inscrit dans un fichier .json et le charge : 
def loadRandomFunctions(nbNoeuds=9, interditMin=1, interditMax=4):
    with open("random.json", 'w') as f: # On ouvre le fichier JSON et on écrit les specificités du graphe aleatoire
        rgraph = randomGraph(nbNoeuds)
        f.write(json.dumps(({"graph":rgraph,"interdits":randomInterdits(rgraph,interditMin,interditMax),"depart":str(random.randint(1,nbNoeuds))})))
        f.close()
    graphFromJson("random.json") # On selectionne le graphe pour l'affichage
    buttonInterdits["state"] = "normal"
    buttonDfs["state"] = "normal"
    buttonGraph["state"] = "normal"
    plt.show()



#====================================================================================================================================================================
# Interface graphique créée en utilisant Tkinter

# Initialisation de la fenêtre principale de l'interface graphique
fenetre = Tk()
fenetre.resizable(width=False, height=False)
fenetre.title("GraphSearchTool")

# Ajout du titre du programme
labelTitre = Label(text="GST", font=("Lucida Calligraphy", 48, "bold"))
labelTitre.grid(row=2, column=1, columnspan=2, padx=120)

# Ajout d'un sous-titre accrocheur
labelPhraseAccroche = Label(fenetre, text="Promenons-nous dans les réseaux !", font = "Arial 8 italic")
labelPhraseAccroche.grid(row=3, column=1, columnspan=2, sticky=N)

tailleGrid=9

noms = Label(fenetre, text="© 2021 Théo Peuchlestrade et Loris Van Katwijk", font = "Arial 8 italic")
noms.grid(row=tailleGrid, column=1, columnspan=2, padx=10, pady=10)



# Algorithme permettant l'ouvrture de fichier afin de les utiliser dans les différents algorithmes précédents
def fileOpenerInterface():  
    filename = askopenfilename(title="Ouvrir votre .JSON", filetypes=[('json files','.json'),('all files','.*')])
    graphFromJson(filename)
    buttonInterdits["state"] = "normal"
    buttonDfs["state"] = "normal"
    buttonGraph["state"] = "normal"

    plt.show()
    
# Ouvre une fenetre sur laquel on donne la liste des incompatibilités
def afficheInterditsInterface(interdit):
    fenetreInterdit = Tk()
    fenetreInterdit.title("Liste des interdits")
    

    for (a,b) in interdit:
        Label(fenetreInterdit, text=f"{a} est incompatible avec {b}", font="Arial 12").pack(padx=10,pady=5)
    
    fenetreInterdit.mainloop()

# Ajout de boutons permettant l'utilisation de chacun des différents algorithmes
buttonDfs = Button(fenetre, text ='Afficher le DFS', command = lambda:afficheDfs(graphSelect, interditSelect, departSelect, dfs(graphSelect, interditSelect, departSelect, [], [],[])), state=DISABLED)
buttonDfs.grid(row=tailleGrid-1, column=2, padx=5, pady=5)

buttonInterdits = Button(fenetre, text ='Afficher les interdits', command = lambda:afficheInterditsInterface(interditSelect), state=DISABLED)
buttonInterdits.grid(row=tailleGrid-2, column=2, padx=5, pady=5)

buttonGraph = Button(fenetre, text ='Afficher le graphe', command = lambda:afficheGraph(graphSelect, departSelect), state=DISABLED)
buttonGraph.grid(row=tailleGrid-3, column=2, padx=5, pady=5)

Button(fenetre, text ='Utiliser un graphe existant', command = lambda:(fileOpenerInterface())).grid(row=tailleGrid-1, column=1, padx=5, pady=5)
value = IntVar()
Button(fenetre, text ='Générer aléatoirement un graphe', command = lambda:loadRandomFunctions(value.get(),1,value.get()//2)).grid(row=tailleGrid-2, column=1, padx=5, pady=5)

spin = Spinbox(fenetre, textvariable=value, from_=3, to=1000, width=4)
spin.grid(row=tailleGrid-3, column=1)
spin.delete(0,END)
spin.insert(0,9)



# Ajout de texte explicatif
label = Label(fenetre, text="Choisissez le nombre de noeuds")
label.grid(row=tailleGrid-4, column=1)

# Notice
def info():
    fenetreInfo = Tk()
    fenetreInfo.title("Infos")
    Label(fenetreInfo, text="Notice d'utilisation", font="Arial 16 bold").pack(padx=20, pady=10)
    with open("README.txt","r") as f: # Ouvre le fichier README.txt et affiche son contenu dans une fenetre
        lines = str(f.read()).split("\n")
    for l in lines:
        Label(fenetreInfo, text=l).pack()


imgInfo = PhotoImage(file="info.png") 
Button(image=imgInfo, command = info).grid(column=2,row=1,sticky=NE) # Bouton "i" en haut à droite de l'interface

fenetre.mainloop()

#====================================================================================================================================================================
