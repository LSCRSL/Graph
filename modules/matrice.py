import random as rand
'''
Fichier contenant toutes les fonctions relatives aux matrices.
'''

def random_int_list(n,bound,j) :
    '''
    input : int, int, int
    renvoie une liste de taille n de nombres aléatoires entre 0 et bound
    ''' 
    l = []
    for i in range(n) : 
        if i == j: 
            l.append(0)
        else :
            l.append(rand.randrange(0,bound))
    return l

def random_int_matrix(n,bound,null_diag=True) : 
    '''
    input : int , int, bool
    matrice carrée de taille n d'entiers tirés aléatoirement entre 0 et
    bound
    '''
    l = []
    if null_diag :
        for j in range(n) :
            l.append(random_int_list(n,bound,j))
    else :
        for j in range(n) :
            l.append(random_int_list(n,bound,-1))
    return l

def affiche_matrix(mat) : 
    '''
    input : int list list
    affiche une matrice carrée
    '''
    t = len(mat)
    print('[')
    for i in range(t) : 
        print(mat[i])
    print(']')

def random_symetric_int_matrix(n, bound,null_diag=True) : 
    '''
    input: int, int, bool; taille de la matrice, limite, paramètre indiquant si la diagonale est nulle
    output: int list list; matrice symetrique de taille n contenant des entiers compris entre 0 et n

    renvoie une matrice carree symétrique

    '''
    l = []
    if null_diag : 
        l.append(random_int_list(n,bound,0))
        for i in range(1,n) : 
            t = []
            taille = len(l)
            for j in range(1,taille+1) : 
                t.append(l[j-1][taille])
            t.append(0)
            for k in range(taille+1, n) :
                t.append(rand.randrange(0,bound))
            l.append(t)
    else : 
        l.append(random_int_list(n,bound,-1))
        for i in range(1,n) : 
            t = []
            taille = len(l)
            for j in range(1,taille+1) : 
                t.append(l[j-1][taille])
            for k in range(taille, n) :
                t.append(rand.randrange(0,bound))
            l.append(t)
    return l

def random_oriented_int_matrix(n, bound, null_diag=True):
    '''
    input: int, int, bool; taille, valeur max, diagonale nulle
    ouput: int list list; 

    renvoie la matrice d'adjacence d'un graphe oriente

    '''
    l = random_int_matrix(n,bound, null_diag)
    for i in range(n):
        for k in range(n):
            if l[i][k]!=0:
                l[k][i]=0
    return l

def random_triangular_int_matrix(n, bound, null_diag=True):
    '''
    input: int, int, bool; taille, valeur max, diagonale nulle
    ouput: int list list; 

    renvoie la matrice d'adjacence d'un graphe dirige cyclique

    '''
    l = random_oriented_int_matrix(n,bound, null_diag=True)
    for i in range(n):
        for j in range(n):
            if i>j:
                l[i][j]=0
    return l