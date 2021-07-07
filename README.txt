Une zone de saisie vous permet de choisir le nombre de noeuds que vous souhaitez avoir pour votre graphe genere aleatoirement. La valeur maximale est 1000.

Le bouton "Generer aleatoirement un graphe" vous permet de generer un graphe de maniere aleatoire en ayant prealablement specifie le nombre de noeuds que vous souhaitez dans celui-ci a l'aide de la zone de saisie.

Le bouton "Utiliser un graphe existant" vous permet de recuperer un fichier JSON contenant les specificites de votre graphe.

Le fichier JSON contenant votre graphe doit avoir l'organisation suivante :

{"graph": *dictionnaire contenant les voisins de chacun des noeuds* (obligatoire)
"interdits": *liste contenant les incompatibilites entre aretes* (obligatoire mais peut etre vide)
"depart": *entier representant le point de depart de la resolution du graphe a l'aide de l'algorithme DFS* (optionnel)}

Exemple de fichier JSON valide : 

{"graph": {"1": ["2", "9"], "2": ["1", "4"], "3": ["4", "5", "6", "9"], "4": ["2", "3"], "5": ["3", "8"], "6": ["3", "7"], "7": ["6", "8", "9"], "8": ["5", "7"], "9": ["1", "3", "7"]},
 "interdits": [[["1", "2"], ["2", "4"]], [["1", "2"], ["3", "4"]]],
 "depart": "3"}

Le bouton "Afficher le graphe" vous permet d'afficher le graphe actuellement selectionne : soit grace a "Generer aleatoirement un graphe", soit grace a "Utiliser un graphe existant".

Le bouton "Afficher les interdits" vous permet d'afficher les differentes incompatibilites entre aretes au sein de votre graphe.

Le bouton "Afficher le DFS" vous permet d'afficher la resolution de votre graphe par notre algorithme de Depth-first search.