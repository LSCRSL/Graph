import random as rand
from modules.node import *
from modules.matrice import *
import modules.get_set as gs
import modules.add_remove as arm
import modules.chemin as path
import modules.connectivity as connect
import graphviz
import os
          
class open_digraph(gs.get_set, arm.add_remove, path.chemin, connect.connectivity): # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
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
            mc= n.get_children_mult()
            if len(n.get_parent_mult())!=0 or len(mc)!=1 or mc[0]!=1:
                return False
        for o in outp : 
            if o not in n_id :
                return False
            n=self.get_node_by_id(o)
            mp=n.get_parent_mult()
            if len(n.get_children_mult())!=0 or len(mp)!=1 or mp[0]!=1:
                return False
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
                    child = noeud.get_children_ids()
                    mult = noeud.get_children_mult()
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
        ->genere un graphe aleatoire suivant les contraintes donnees par l'utilisateur
        '''
        G = cls.empty()
        mat = []
        if form=="free":
            mat = random_int_matrix(n, bound,False)
            G = cls.graph_from_adjacency_matrix(mat)
        elif form=="DAG":
            mat = random_triangular_int_matrix(n,bound)
            G = cls.graph_from_adjacency_matrix(mat)
        elif form=="oriented":
            mat = random_oriented_int_matrix(n, bound)
            G = cls.graph_from_adjacency_matrix(mat)
        elif form=="loop-free":
            mat = random_int_matrix(n, bound)
            G = cls.graph_from_adjacency_matrix(mat)
        elif form=="undirected":
            mat = random_symetric_int_matrix(n,bound,False)
            G = cls.graph_from_adjacency_matrix(mat)
        elif form=="loop-free undirected":
            mat = random_symetric_int_matrix(n,bound)
            G = cls.graph_from_adjacency_matrix(mat)
        affiche_matrix(mat)
        n = G.get_id_node_map()
        l = list(n.keys())       
        for i in range(inputs) : 
            G.add_input_node(l[rand.randrange(0,len(l))])
        for j in range(outputs) :
            G.add_output_node(l[rand.randrange(0,len(l))])
        return G

    def save_as_dot_file(self,path, filename='graph', verbose=False):
        '''
        input : string, bool, string ; lieu d'enregistrement, flag pour l'affichage du label et de l'id, nom du fichier sans ".dot" ("graph" par défaut)
        Enregistre le graphe en question en format .dot a l’endroit specifie par
        path avec l'affichage déterminé par verbose.
        Dans notre fct : 
        input=indice_input si entrée, -1 sinon
        output=indice_sortie si sortie, -1 sinon
        '''
        filepath = os.path.join(path, filename+'.dot')
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
                lab=n.get_label()
                if lab=='' or lab=='|' or lab=='&' or lab=='^' or lab=='~':
                    lab='"'+lab+'"'
                    f.write(f"{n.get_id()} [label={lab}, color={color}];\n")
                else:
                    f.write(f"{n.get_id()} [label={n.get_label()}, color={color}];\n")
        for n in self.get_node():
            cid=n.get_children_ids()
            cmul=n.get_children_mult()
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

    def display(self, filename='graph', verbose=False):
        '''
        input : bool ; affichage du label et de l'id
        ouvre le document pdf avec le graphe
        '''
        self.save_as_dot_file(os.getcwd(), filename, verbose)
        convert='dot -Tpdf {}.dot -o {}.pdf' .format(filename,filename)
        open_file='xdg-open {}.pdf' .format(filename)
        os.system(convert)
        os.system(open_file)

    @classmethod
    def identity(cls, n):
        g=open_digraph.empty()
        for i in range(n):
            ni=node(i,'{:}'.format(i),{},{})
            no=node(i+n,'{:}'.format(n+i),{},{})
            g.add_nodes(ni)
            g.add_input_id(i)
            g.add_nodes(no)
            g.add_output_id(i+n)
            g.add_edge(i,i+n)
        return g
    
    @classmethod
    def parallel(cls,g1,g2):
        ''' 
        input : open_digraph, open_digraph; graphes à fusionner
        output : open_digraph 

        renvoie un nouveau graphe qui est la composition parallele des graphes donnes
        '''     
        ge=g1.copy()
        ge.iparallel(g2)
        return ge
    
    @classmethod
    def compose(cls,g,f):
        '''
        input : open_digraph, open_digraph; graphes f et g à composer
        output : open_digraph 
        
        renvoie un nouveau graphe qui est la composition sequentielle des graphes donnes, ie f 'rond' g
        '''    
        compo=g.copy()
        compo.icompose(f.copy())
        return compo

    def connected_list(self):
        '''
        output : open_digraph list;

        renvoie une liste d'open_digraph, chacun correspondant à une composante connexe du graphe de départ
        '''
        (ctp, dict) = self.connected_components()
        l = [open_digraph.empty() for i in range(ctp)]
        for (k,v) in dict.items() : 
            l[v].add_nodes(self.get_node_by_id(k))
            if k in self.get_input_ids() : 
                l[v].add_input_id(k)

            if k in self.get_output_ids() : 
                l[v].add_output_id(k)
        return l
    
    @classmethod
    def graph_from_adjacency_matrix(cls, mat):
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
        return cls([],[],nodelist)
    
    def fusion(self,id1,id2, noloop=False, label='" "') : 
        '''
        input : int, int, bool, string
        fusion les noeuds donées en argument avec label ou non et supprime les boucles si le parametre noloop = True
        '''
        node1 = self.get_node_by_id(id1)
        node2 = self.get_node_by_id(id2)
        p1 = node1.get_parent_ids()
        p2 = node2.get_parent_ids()
        c1 = node1.get_children_ids()
        c2 = node2.get_children_ids()
    
        #fusion des parents
        for par2 in p2 : 
            #rajout du noeud ou augmentation de la multiplicité
            node1.add_parents_id(par2, node2.parents[par2])
            
            #on prend le noeud parent
            noeud_parent = self.get_node_by_id(par2)
            
            #rajout du noeud ou augmentation de la multiplicité
            noeud_parent.add_child_id(id1, node2.parents[par2])        
                
        #fusion des enfants       
        for child2 in c2 : 
            #rajout du noeud ou augmentation de la multiplicité
            node1.add_child_id(child2, node2.children[child2])
            
            #on prend le noeud enfant
            noeud_child = self.get_node_by_id(child2)
            
            #rajout du noeud ou augmentation de la multiplicité
            noeud_child.add_parents_id(id1, node2.children[child2])
            
        #on supprime le noeud doublon
        self.remove_node_by_id(id2)
        
        #on met le label        
        node1.set_label(label)

        if noloop : 
            if id1 in node1.get_parent_ids() :
                node1.remove_parent_id(id1)
            if id1 in node1.get_children_ids() : 
                node1.remove_child_id(id1)
                
