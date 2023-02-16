import random as rand
import graphviz
import os

class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children
    def __str__(self):
        '''
        output: string; les attributs du noeud
        '''
        return "ID: "+str(self.id)+"  Label:"+self.label+"  Parents:"+str(self.parents)+"  Children:"+str(self.children) +"\n"
    def __repr__(self):
        '''
        output: string; appelle __str__
        '''
        return str(self)

    def copy(self):
        '''
        output: node; copie du noeud
        '''
        return (node(self.id, str(self.label), self.parents.copy(), self.children.copy()))

    #les getters
    def get_id(self):
        '''
        output: int; 
        '''
        return self.id

    def get_label(self) :
        '''
        output: string; label
        '''
        return self.label

    def get_parent_ids(self) : 
        '''
        output: int dict; 
        '''
        return self.parents.keys()

    def get_children_ids(self) : 
        '''
        output: int dict; 
        '''
        return self.children.keys()
    
    def get_parent_mult(self) : 
        '''
        output: int dict; 
        '''
        return self.parents.values()

    def get_children_mult(self) : 
        '''
        output: int dict; 
        '''
        return self.children.values()

    @classmethod
    def node_empty(cls) : 
        '''
        output : node

        crée un noeud vide
        '''
        return cls(-1, "", {}, {})

    #les setters
    def set_id (self,x) : 
        '''
        input: int ; 
        '''
        self.id = x

    def set_label(self, x) :
        '''
        input: string ; 
        '''
        self.label = x

    def set_parent_ids(self, l) : 
        '''
        input: int list; 
        '''
        dict={}
        lm=list(self.get_parent_mult())
        for i in range (len(l)):
            dict[l[i]]=lm[i]
        self.parents = dict

    def set_children_ids (self, l) : 
        '''
        input: int list; 
        '''
        dict={}
        lm=list(self.get_children_mult())
        for i in range (len(l)):
            dict[l[i]]=lm[i]
        self.parents = dict

    def add_child_id (self, id, mult) : 
        '''
        inputs: int, int; id, multiplicité
        '''
        if id in self.get_children_ids() :
            self.children[id] += mult
        else : 
            self.children[id] = mult

    def add_parents_id(self, id, mult) :
        '''
        inputs: int, int; id, multiplicité
        '''
        if id in self.get_parent_ids() :
            self.parents[id] += mult
        else : 
            self.parents[id] = mult

    def remove_parent_once(self, id) : 
        '''
        input: int; id du parent pour lequel on retire une multiplicité
        '''
        if id in self.get_parent_ids() : 
            self.parents[id] -= 1
            if self.parents[id] == 0 :
                #il faut l'enlever dans la section enfant du noeud du parent
                del self.parents[id]
        
    def remove_child_once(self, id) : 
        '''
        input: int; id de l'enfant pour lequel on retire une multiplicité 
        '''
        if id in self.get_children_ids() : 
            self.children[id] -= 1
            if self.children[id] == 0 :
                #ici on utilise .children c'est ok ?
                del self.children[id]

    def remove_parent_id(self, id) : 
        '''
        input: int; id du parent pour lequel on retire toutes les multiplicités
        '''
        if id in self.get_parent_ids() : 
            del self.parents[id]
    
    def remove_child_id(self, id) : 
        '''
        input: int; id de l'enfant pour lequel on retire toutes les multiplicités
        '''
        if id in self.get_children_ids() :
            del self.children[id]

    def indegree(self) : 
        """
        output : int; le degre entrant du noeud
        """
        mult = list(self.get_parent_mult())
        cpt = 0
        for i in mult : 
            cpt += i
        return cpt

    def outdegree(self) : 
        """
        output : int; le degre entrant du noeud
        """
        mult = list(self.get_children_mult())
        cpt = 0
        for i in mult : 
            cpt += i
        return cpt

    def degree(self) : 
        return self.indegree() + self.outdegree()
            
class open_digraph: # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        1
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict

    def __str__(self):
        '''
        output: string; les noeuds du graph et leurs attributs
        '''
        return self.nodes.__repr__()

    @classmethod
    def empty(cls):
        '''
        output: open_digraph; graph vide
        '''
        return cls([],[],[]) 

    def copy(self):
        """
        create a copy of the graph
        """
        i = self.inputs.copy()
        o = self.outputs.copy()
        l_n = [node.copy() for node in self.nodes.values()]
        return open_digraph(i, o, l_n)

    #les getters
    def get_input_ids(self) : 
        '''
        output: int list; ids des parents
        '''
        return self.inputs

    def get_output_ids(self) : 
        '''
        output: int list; ids des enfants
        '''
        return self.outputs

    def get_id_node_map(self) :
        '''
        output: int->node dict; dictionnaire id:node
        '''
        return self.nodes

    def get_node(self) : 
        '''
        output: node list; liste des noeuds
        '''
        return [n for (id,n) in self.nodes.items()]

    def get_node_ids(self) : 
        '''
        output: int dict; 
        '''
        return self.nodes.keys()

    def get_node_by_id(self,i) : 
        '''
        input: int; id
        output: node; 
        '''
        for (id,n) in self.get_id_node_map().items() :
            if id == i :
                return n

    def get_node_by_ids(self, l) :
        '''
        input: int list; liste d'ids
        output: node list; 
        '''
        return [n for i in l for (id,n) in self.get_id_node_map().items() if i == id ]

    #les setters
    def set_input_ids(self, ln) : 
        ''' 
        input: node list; ln une liste de noeuds
        '''
        self.inputs=[]
        for n in ln : 
            self.inputs.append(n.get_id())
            self.nodes[n.get_id()] = n

    def set_outputs_ids (self, ln) : 
        ''' 
        input: node list; ln une liste de noeuds
        '''
        self.outputs=[]
        for n in ln : 
            self.outputs.append(n.get_id())
            self.nodes[n.get_id()] = n

    def add_input_id(self, id) : 
        ''' 
        input: int ; id l'id du noeud
        '''
        self.inputs.append(id)

    def add_output_id(self, id) : 
        ''' 
        input: int ; id l'id du noeud
        '''
        self.outputs.append(id)

    def add_nodes(self, n ) : 
        ''' 
        input: node ; n un noeud
        '''
        self.nodes[n.get_id()] = n

    def new_id(self) : 
        '''
        output: int; méthode qui renvoie un indice non-utilisé dans le graphe
        '''
        def f(i) :
            '''
            input: int; id
            output: int; fonction récursive qui renvoie le prochain indice libre
            '''
            for (id,n) in self.nodes.items() : 
                if (i == id) : 
                    i+=1
                    f(i)
            return i
        return f(0)

    def add_edge(self,src,tgt) : 
        '''
        inputs: int, int ; id src, id tgt
        méthode qui rajoute une arête du noeud source au noeud cible
        '''
        self.get_node_by_id(src).add_child_id(tgt, 1)
        self.get_node_by_id(tgt).add_parents_id(src,1)
    
    def add_edges(self, edges) : 
        '''
        input: (int*int) list; list de couples d'id
        méthode qui rajoute une arête entre chacune des paires de edges
        '''
        for (src,tgt) in edges : 
            self.add_edge(src,tgt)

    def add_node(self, label,parents, children) : 
        ''' 
        inputs: string, int list,int list; 
        Méthode qui rajoute un noeud (avec label) au graphe (en utilisant un
        nouvel id), et le lie avec les noeuds d’ids parents et children (avec leurs mul-
        tiplicités respectives). Si les valeurs par défaut de parents et/ou children sont
        None, leur attribuer un dictionnaire vide.
        Output: id du nouveau noeud.
        '''
        if parents == None : 
            parents = {}
        if children == None :
            children = {}
        ID = self.new_id()  
        n = node(ID,label, {}, {})
        self.add_nodes(n)
        if parents != {} : 
            for (i,j) in parents.items() : 
                for k in range (j) :
                    self.add_edge(i, ID)
        if children != {} : 
            for (i,j) in children.items() : 
                for k in range(j) : 
                    self.add_edge(ID, i)
        return ID

    def remove_node(self, id) : 
        '''
        input: int; id du noeud à retirer
        '''
        if id in self.get_input_ids() : 
            self.inputs.remove(id)
        if id in self.get_output_ids() : 
            self.outputs.remove(id)
        del self.nodes[id]

    def remove_edge(self, src, tgt) : 
        '''
        inputs: int, int; id source et id cible de l'arête à retirer
        '''
        l = self.get_node_by_ids([src,tgt])
        SRC = l[0]
        TGT = l[1]
        SRC.remove_child_once(tgt)
        TGT.remove_parent_once(src)

    def remove_parallel_edges(self, src, tgt) : 
        '''
        inputs: int, int; id source et id cible des arêtes à retirer
        '''
        l = self.get_node_by_ids([src,tgt])
        SRC = l[0]
        TGT = l[1]
        SRC.remove_child_id(tgt)
        TGT.remove_parent_id(src)

    def remove_node_by_id(self, id) : 
        '''
        input: int; id du noeud pour lequel on retire les arêtes associées
        '''
        n = self.get_node_by_id(id)
    
        for p in list(n.get_parent_ids()) :
            self.remove_parallel_edges(p, id)
        for c in list(n.get_children_ids()) : 
            self.remove_parallel_edges(id, c)
        self.remove_node(id)

    def remove_edges(self, l_p_id) : 
        '''
        input: (int*int) list; liste des couples id source/id target qui caractérisent les arêtes à retirer pour une multiplicité
        '''
        for (src,tgt) in l_p_id : 
            self.remove_edge(src, tgt)
    
    def remove_several_parallel_edges(self, l_p_id) : 
        '''
        input: (int*int) list; liste des couples id source/id target qui caractérisent les arêtes à retirer pour toutes les multiplicités
        '''
        for (src,tgt) in l_p_id : 
            self.remove_parallel_edges(src,tgt)
    
    def remove_nodes_by_id(self, l_id) : 
        '''
        input: int list; liste des id des noeuds à retirer
         
        '''
        for id in l_id : 
            self.remove_node_by_id(id)
    
    def is_well_formed(self) : 
        '''
        output: bool; renvoie true si le graphe est bien formé, false sinon
        '''
        inp = self.get_input_ids()
        outp = self.get_output_ids()
        n_id = self.get_node_ids() 
        NODE = self.get_id_node_map()
        for i in inp : 
            if i not in n_id : 
                return False
            n=self.get_node_by_id(i)
            mc= list(n.get_children_mult())
            if len(n.get_parent_mult())!=0 or len(mc)!=1 or mc[0]!=1:
                return False
        for o in outp : 
            if o not in n_id :
                return False
            n=self.get_node_by_id(o)
            mp=list(n.get_parent_mult())
            if len(n.get_children_mult())!=0 or len(mp)!=1 or mp[0]!=1:
                return False
        #4e point
        for (k,v) in NODE.items(): 
            if k != v.get_id() :
                return False
            try:
                for i in n.get_children_ids():
                    mj=v.children[i]
                    mi=i.parent[v.get_id()]
                    if mi!=mj :
                        return False
            except:
                return False
        return True
            
    def assert_is_well_formed(self) :
        '''
        output: error_type; une erreur est levée si le graph est mal formé
        '''
        if not(self.is_well_formed()) :
            raise ValueError
        
    def add_input_node(self,tgt) :
        '''
        input: int; id du noeud vers lequel le nouveau noeud ajoputé au graphe pointe

        Vérifie si l'ajout de l'input est possible, si oui effectue l'ajout, si non renvoie une erreur
        '''
        if (tgt in self.get_input_ids() or (tgt in self.get_output_ids())) :
            raise ValueError
        else : 
            x = self.add_node('', {}, {tgt:1})
            self.add_input_id(x)
            
        
    def add_output_node(self,src) :
        '''
        input: int; id du noeud qui pointe vers un nouveau noeud ajouté au graphe

        Vérifie si l'ajout de l'output est possible, si oui effectue l'ajout, si non renvoie une erreur
        '''
        if (src in self.get_input_ids() or (src in self.get_output_ids())) : 
            raise ValueError
        else : 
            x = self.add_node('', {src:1}, {})
            self.add_output_id(x)


    def dict_of_graph(self):
        '''
        input: open_digraph; graph à n noeuds
        output: int->int dict; dictionnaire qui à chaque id de noeud associe un entier entre 0 et n-1

        renvoie un dictionnaire, associant a chaque id de noeud un unique
        entier
        '''
        nlist= self.get_id_node_map().keys()
        cpt=0
        dict={}
        for (id) in nlist :
            dict[id] = cpt
            cpt=cpt+1
        return dict

    def adjacency_matrix(self):
        '''
        output: int list list; matrice du graph

        renvoie une matrice d'adjacence du graphe donne
        '''
        sc = self.copy()
        n= sc.get_node()
        inp = list(sc.get_input_ids())
        out = list(sc.get_output_ids())
        int_out = inp + out
        sc.remove_nodes_by_id(int_out)
        d = sc.dict_of_graph()
        idlist=list(d.keys())
        size_l = len(idlist)
        mat = []
        for i in range(size_l):
            for (k,v) in d.items() : 
                if v == i : 
                    ll = []
                    noeud = sc.get_node_by_id(k)
                    child = list(noeud.get_children_ids())
                    mult = list(noeud.get_children_mult())
                    for j in range (size_l) : 
                        b = False
                        for c in range(len(child)) :
                            if (d[child[c]] == j) :
                                ll.append(mult[c])
                                b = True
                        if not(b) : 
                            ll.append(0)
                    mat.append(ll)       
        return mat


    @classmethod
    def random(cls,n, bound, inputs=0, outputs=0, form="free"):
        '''
        inputs: int, int, int list, int list, string;
        taille, nb arrêtes max par noeud, v inputs, outputs, option parmis:
        free, DAG, oriented, loop-free, unidrected et loop-free undirected
        outputs: open_digraph: graphe à n noeuds respectant l'option choisie

        genere un graphe aleatoire suivant les contraintes donnees par l'utilisateur

        '''
        G = cls.empty()
        mat = []
        if form=="free":
            mat = random_int_matrix(n, bound,False)
            G = graph_from_adjacency_matrix(mat)
        elif form=="DAG":
            mat = random_triangular_int_matrix(n,bound)
            G = graph_from_adjacency_matrix(mat)
        elif form=="oriented":
            mat = random_oriented_int_matrix(n, bound)
            G = graph_from_adjacency_matrix(mat)
        elif form=="loop-free":
            mat = random_int_matrix(n, bound)
            G = graph_from_adjacency_matrix(mat)
        elif form=="undirected":
            mat = random_symetric_int_matrix(n,bound,False)
            G = graph_from_adjacency_matrix(mat)
        elif form=="loop-free undirected":
            mat = random_symetric_int_matrix(n,bound)
            G = graph_from_adjacency_matrix(mat)
        affiche_matrix(mat)
        n = G.get_id_node_map()
        l = list(n.keys())       
        for i in range(inputs) : 
            G.add_input_node(l[rand.randrange(0,len(l))])

        for j in range(outputs) :
            G.add_output_node(l[rand.randrange(0,len(l))])

        return G

    def save_as_dot_file(self,path, verbose=False):
        '''
        input : string, bool ; lieu d'enregistrement, flag pour l'affichage du label et de l'id

        enregistre le graphe en question en format .dot a l’endroit specifie par
        path avec l'affichage déterminé par verbose.

        dans notre fct : 
        input=indice_input si entrée, -1 sinon
        output=indice_sortie si sortie, -1 sinon
        '''
        filepath = os.path.join(path, 'graph.dot')
        f = open(filepath, "w")
        f.write("digraph G{\n")
        inp = self.get_input_ids()
        out = self.get_output_ids()
        for n in self.get_node():
            color = "black"
            if n.get_id() in inp :
                color = "purple"
            if n.get_id() in out :
                color = "blue"
            if verbose:
                f.write(f"{n.get_id()} [label=\"{n.get_label()}\\n{n.get_id()}\", color={color}];\n")
            else:
                f.write(f"{n.get_id()} [label={n.get_label()}, color={color}];\n")
        for n in self.get_node():
            cid=list(n.get_children_ids())
            cmul=list(n.get_children_mult())
            for c in range (len(cid)):
                for m in range (0,cmul[c]):
                    f.write(f"{n.get_id()} -> {cid[c]};\n")
        f.write("}\n")
        f.close()
    
    @classmethod
    def from_dot_file(cls,filename):
        '''
        input : fichier.dot : fichier à lire

        output : open_digraph ; le graphe associé au fichier

        lit le fichier et crée/renvoie le graphe associé au fichier lu
        '''

        G=cls.empty()
        f = open(filename, 'r')
        for line in f:
            if "{" in line or "}" in line:
                continue
            first_split = line.split('->')
            if len(first_split) == 1 : 
                second_split = line.split('[')
                if len(second_split) == 2 : 
                    third_split = second_split[1].split(',')
                    color = third_split[1].split('=')[1].split(']')[0]
                    id = second_split[0]
                    label = third_split[0].split('=')[1]
                    N_ode = node(int(id),label , {}, {})
                    if color == "purple":
                        G.set_input_ids([N_ode])
                    elif color == "blue" : 
                        G.set_outputs_ids([N_ode])
                    else :
                        G.add_nodes(N_ode)
            else :
                G.add_edge(int(first_split[0]), int(first_split[1].split(';')[0]))
        f.close()
        return G

    def display(self,verbose=False):
        '''
        input : bool ; affichage du label et de l'id

        ouvre le document pdf avec le graphe
        '''
        self.save_as_dot_file(os.getcwd(), verbose)
        convert='dot -Tpdf graph.dot -o graph.pdf'
        open_file='xdg-open graph.pdf'
        os.system(convert)
        os.system(open_file)

    def shift_indices(self,n):
        '''
        input: int; valeur à ajouter à tous les id des noeuds du graph
        '''
        plin=self.get_input_ids()
        plout=self.get_output_ids()
        nlin=[]
        nlout=[]
        map=self.get_id_node_map()
        for id in plin:
            nlin.append(map[id])
        for id in plout:
            nlout.append(map[id])
        ndlist=self.get_node()
        for k in range (len(ndlist)):
            nd=ndlist[k]
            p_id=nd.get_id() #on recupère l'ancien id du noeud et on le met à jour
            n_id=p_id+n
            nd.set_id(n_id)
            #on modifie les ids des parents du noeud
            pplist=list(nd.get_parent_ids())
            nplist=[]
            for i in pplist:
                nplist.append(i+n)
            nd.set_parent_ids(nplist)
            #on modifie les ids des enfants du noeud
            pclist=list(nd.get_children_ids())
            nclist=[]
            for i in pclist:
                nclist.append(i+n)
            nd.set_children_ids(nclist)
        self.set_input_ids(nlin)
        self.set_outputs_ids(nlout)

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

def graph_from_adjacency_matrix(mat):
    '''
    input: int list list; matrice à convertir en graphe
    output: open_digraph; graphe obtenu à partir de la matrice

    renvoie un multigraphe à partir d'une matrice

    '''
    nodelist=[]
    for i in range(len(mat)): #il y a n noeuds
        nwnd=node(i, '', {}, {}) #on init le ième noeud
        for j in range(len(mat)):  #on parcourt les colonnes d'une même ligne
            if mat[i][j]!=0: #si !=0 alors le noeud a un enfant d'id le num de colonne
                nwnd.add_child_id(j,mat[i][j])  #on ajoute l'enfant
            if j==i: #on se place dans la ième colonne pour parcourir les parents
                for l in range(len(mat)):  #on parcourt les lignes de cette colonne
                    if mat[l][j]!=0: #si !=0 alors l est l'id du parent du noeud i
                        nwnd.add_parents_id(l,mat[l][j]) #on ajoute le parent
        nodelist.append(nwnd)
    return open_digraph([],[],nodelist)

class bool_circ(open_digraph):

    def __init__(self,g) :
        super().__init__(g.get_input_ids(), g.get_output_ids(), g.get_node())
        if not self.is_well_formed():
            raise ValueError
    
    def is_cyclic(self) : 
        '''
        output : bool;
        renvoie vrai si le graphe est acyclique
        '''

        def is_cycle(g) : 
            if g.get_id_node_map() == {} : 
                return True
            else : 
                l_oupt = g.get_output_ids()
                if l_oupt == [] : 
                    return False
                else :
                    g.remove_node(l_oupt.pop(0))
                    return is_cycle(g)
        return is_cycle(self.copy())

    def is_well_formed(self):
        if self.is_cyclic() : 
            print('ici')
            return False 
        else : 
            n = self.get_node()
            outp = self.get_input_ids()
            inp = self.get_input_ids()
            for node in n : 
                l = node.get_label()
                if  l == '' : 
                    if node.get_id() in outp or node.get_id() in inp :
                        continue 
                    elif node.indegree() != 1 :
                        print('ici1')
                        return False
                elif l == '&' or l == '|' : 
                    if node.outdegree() != 1 :
                        print(node.outdegree())
                        print('ici2')
                        return False
                elif l == '~' :
                    if node.indegree() != 1 and node.outdegree() != 1 :
                        print('ici3') 
                        return False
                elif l != '0' and l != '1' and l != '^' :
                    print('ici4')
                    print(l)
                    return False
            return True

    def min_id(self):
        '''
        output : int; le plus petit id porté dans le graph
        '''
        n_list=self.get_node()
        min=n_list[0].get_id()
        for n in n_list:
            id=n.get_id()
            if id<min :
                min=id
        return min

    def max_id(self):
        '''
        output : int; le plus grand id porté dans le graph
        '''
        n_list=self.get_node()
        max=n_list[0].get_id()
        for n in n_list:
            id=n.get_id()
            if id>max :
                max=id
        return max






                     
                

    


