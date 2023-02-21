# projet s4

Documentations

## TP2

- EX 1: Classe node
'''
input: int; id du parent pour lequel on retire une multiplicité
'''
'''
input: int; id de l'enfant pour lequel on retire une multiplicité 
'''
'''
input: int; id du parent pour lequel on retire toutes les multiplicités
'''
'''
input: int; id de l'enfant pour lequel on retire toutes les multiplicités
'''   

- EX 2: Classe open_digraph
fonction remove_node:   
'''
input: int; id du noeud à retirer
'''   
'''
inputs: int, int; id source et id cible de l'arête à retirer
'''
'''
inputs: int, int; id source et id cible des arêtes à retirer
'''
'''
input: int; id du noeud pour lequel on retire les arêtes associées
'''
'''
input: (int*int) list; liste des couples id source/id target qui caractérisent les arêtes à retirer pour une multiplicité
'''
'''
input: (int*int) list; liste des couples id source/id target qui caractérisent les arêtes à retirer pour toutes les multiplicités
'''
'''
input: int list; liste des id des noeuds à retirer
'''   

- EX 3: Classe open_digraph
'''
output: bool; true si le graphe est bien formé, false sinon
'''
'''
output: error_type; une erreur est levée si le graph est mal formé
'''   

- EX 4: Classe open_digraph
'''
input: int; id du noeud vers lequel le nouveau noeud ajoputé au graphe pointe
'''
'''
input: int; id du noeud qui pointe vers un nouveau noeud ajouté au graphe
'''




## TP3

- EX 4 : 
renvoie une matrice carree symétrique

- EX 5 :
renvoie la matrice d'adjacence d'un graphe oriente

- EX 6 : 
renvoie la matrice d'adjacence d'un graphe dirige cyclique

- EX 7 : 
renvoie un multigraphe à partir d'une matrice

- EX 8 : 
genere un graphe aleatoire suivant les contraintes donnees par l'utilisateur

- EX 9 : 
renvoie un dictionnaire, associant a chaque id de noeud un unique
entier 

- EX 10:
renvoie une matrice d'adjacence du graphe donne
- 


## TP4

save_as_dot_file(self, path, verbose=False)
- EX 1 : 
''' 
input : path; lieu d'enregistrement, bool ; affichage du label et de l'id

enregistrele graphe en question en format .dot `a l’endroit sp´ecifi´e par
path avec l'affichage déterminé par verbose.
'''

- EX 2 : 
'''
input : fichier.dot : fichier à lire

output : open_digraph ; le graphe associé au fichier

lit le fichier et crée/renvoie le graphe associé au fichier lu
'''

- EX 3 : 
'''
input : bool ; affichage du label et de l'id

ouvre le document pdf avec le graphe
'''
- 
- 
- 
- 

## TP5

- EX 1 :
'''
input : open_digraph; graphe à ajouter à notre graphe de départ

modifie notre graphe par l'ajout d'un graphe supplémentaire
'''

''' 
input : open_digraph; graphe à combiner avec notre graphe de départ
output : open_digraph 

renvoie un nouveau graphe qui est la composition parallele des graphes donnes
'''

- EX 2 : 
'''
input : open_digraph; graphe à combiner avec notre graphe de départ

modifie notre graphe en reliant les entrees de self et les sorties de l'open_digraph donne en argument
'''

'''
input : open_digraph; graphe à combiner avec notre graphe de départ
output : open_digraph 

renvoie un nouveau graphe qui est la composition sequentielle des graphes donnes
'''

- EX 3 :
'''
input : int; le nombre de fils
output : open_digraph 

cree et renvoie un open_digraph de l'identite sur n fils
'''

- EX 4 : 
'''
output : int; int->int dict;

renvoie le nombre de composantes connexes et un dictionnaire a associe à chaque id de noeud à une composante connexe
'''

- EX 5 : 
'''
output : open_digraph list;

renvoie une liste d'open_digraph, chacun correspondant à une composante connexe du graphe de départ
'''

- 
- 
- 

