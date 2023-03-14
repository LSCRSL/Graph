import random as rand
from modules.node import *
from modules.matrice import *
import modules.get_set as gs
import modules.add_remove as arm
import modules.chemin as path
import modules.connectivity as connect
import graphviz
import os
          
class open_digraph: # for open directed graph
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
        output: int list; 
        '''
        return list(self.nodes.keys())

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

    def set_output(self, l_id) : 
        '''
        input : int list; l_id liste d'id
        '''
        self.outputs = l_id

    def set_input(self, l_id) : 
        '''
        input : int list; l_id liste d'id
        '''
        self.inputs = l_id

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

    def add_nodes_list(self,nn):
        '''
        input: node list, node list;
        nn les noeuds à rajouter au debut du dict de nodes de self
        '''
        sn=self.get_node()
        self.nodes={}
        for n in nn:
            self.add_nodes(n)
        for n in sn:
            self.add_nodes(n)

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
    
        for p in n.get_parent_ids() :
            self.remove_parallel_edges(p, id)
        for c in n.get_children_ids() : 
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
        input: int; id du noeud vers lequel le nouveau noeud ajouté au graphe pointe

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

        genere un graphe aleatoire suivant les contraintes donnees par l'utilisateur

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

        enregistre le graphe en question en format .dot a l’endroit specifie par
        path avec l'affichage déterminé par verbose.

        dans notre fct : 
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

    def shift_indices(self,n):
        '''
        input: int; valeur à ajouter à tous les id des noeuds du graph
        '''
        plin=self.get_input_ids()
        plout=self.get_output_ids()
        map=self.get_id_node_map()

        nlin=[]
        nlout=[]
        nnode = []

        for id in plin:
            nlin.append(map[id])
        for id in plout:
            nlout.append(map[id])
        ndlist = list(map.values())

        for k in range (len(ndlist)):
            nd=ndlist[k]
            p_id=nd.get_id() #on recupère l'ancien id du noeud et on le met à jour
            pplist = nd.get_parent_ids() #id des parents
            ppmlist = nd.get_parent_mult() #mult des parents 
            pclist = nd.get_children_ids() #id des enfants
            pcmlist = nd.get_children_mult() #mult des enfants
            n_id=p_id+n
            self.remove_node(p_id)
            nd.set_id(n_id)
            dictc = {}
            for i in range(len(pclist)) : 
                dictc[pclist[i]+n] = pcmlist[i]
            nd.set_children_ids(dictc)
            dictp = {}
            for j in range(len(pplist)) : 
                dictp[pplist[j]+n] = ppmlist[j]
            nd.set_parent_ids(dictp)
            nnode.append(nd)
            
        for node in nnode :
            self.add_nodes(node)
        self.set_input_ids(nlin)
        self.set_outputs_ids(nlout)


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
    
    def iparallel(self,g):
        '''
        input : open_digraph; graphe à ajouter à notre graphe de départ
        
        modifie notre graphe par l'ajout d'un graphe supplémentaire
        '''
        minId=g.min_id()
        maxId=g.max_id()
        self.shift_indices(maxId-minId+1)
        inpId=g.get_input_ids()
        for i in inpId:
            self.add_input_id(i)
        outId=g.get_output_ids()
        for o in outId:
            self.add_output_id(o)
        noeuds=g.get_node()
        for n in noeuds:
            self.add_nodes(n)
        
    def icompose(self,f):
        '''
        input : open_digraph; graphe à combiner avec notre graphe de départ
        
        modifie notre graphe en reliant les entrees de self et les sorties de l'open_digraph donne en argument
        '''
        if (len(self.get_input_ids())!=len(f.get_output_ids())):
            raise ValueError
        else:
            minId=f.min_id()
            maxId=f.max_id()
            self.shift_indices(maxId-minId+1)
            inpId=f.get_input_ids()
            outId=f.get_output_ids()
            selfInpId = self.get_input_ids()
            self.set_input(inpId)
            noeuds=f.get_node()
            self.add_nodes_list(noeuds)
            for k in range(len(selfInpId)):
                ii=outId[k]
                oi=selfInpId[k]
                self.add_edge(ii,oi)
        
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
    
    def connected_components(self) : 
        cpt = 0
        dict = {}
        for node in self.get_node() :
            if node.get_id() not in dict.keys() :
                self.same_graph(node, cpt, dict)
                cpt += 1
        return (cpt,dict)
    
    def same_graph(self,node, cpt, dict) :
        if node.get_id() in dict.keys() : 
            for parent in node.get_parent_ids() : 
                if parent not in dict.keys() : 
                    self.same_graph(self.get_node_by_id(parent), cpt,dict)
            
            for child in node.get_children_ids() :
                if child not in dict.keys() : 
                    self.same_graph(self.get_node_by_id(child), cpt,dict)
        else : 
            dict[node.get_id()] = cpt
            for parent in  node.get_parent_ids():
                self.same_graph(self.get_node_by_id(parent), cpt,dict)

            for child in node.get_children_ids() :
                dict[child] = cpt
                self.same_graph(self.get_node_by_id(child), cpt,dict)

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
    
    def dijkstra(self,src, direction=None, tgt=None): #testée dans worksheet
            '''
            input: node, int, node;
            output: node->int dict, node->int dict;
            Algorithme de Dijkstra qui calcule les distances à partir du noeud src
            dans les parents si direction=-1, dans les enfants si direction=1 et les 2 si direction=None
            Renvoie dist le dictionnaire qui à chaque noeud associe sa distance à src 
            et prev le dictionnaire qui à chaque enfant et/ou parent associe le noeud précédent par lequel il passe en empruntant le plus court chemin
            '''
            Q=[src]
            dist={src:0}
            prev={}
            while Q!=[]:
                u=min(Q,dist)
                Q.remove(u)
                children=[]
                parents=[]
                for cid in u.get_children_ids():
                    children.append(self.get_node_by_id(cid))
                for pid in u.get_parent_ids():
                    parents.append(self.get_node_by_id(pid))
                if direction==1:
                    neighbours=children
                else:
                    neighbours=parents
                    if direction==None :
                        neighbours.extend(children)
                for v in neighbours:
                    if v not in dist.keys():
                        Q.append(v)
                    if (v not in dist.keys()) or (dist[v]>dist[u]+1):
                        dist[v]=dist[u]+1
                        prev[v]=u
                if tgt==u:
                    return dist, prev
            return dist, prev
        
        
    def shortest_path(self, src, tgt, direction=None):
        '''
        input: node, node, int; noeud source et noeud d'arrivé, direction optionnel
        output: list; liste des noeuds qui forment le chemin le plus court du noeud source au noeud d'arrivé
        '''
        res=[tgt]
        while src not in res:
            d1,d2=self.dijkstra(src,direction)
            try : 
                tgt=d2[tgt]
            except : 
                return []
            res.insert(0,tgt)
        return res
    
    def dist_ancetre(self, n1, n2):
        '''
        input: node, node;
        output: int->(int*int) dict; dictionnaire qui associe à chaque id d'un ancêtre 
        commun aux 2 noeuds un tuple des distances resoectives de l'ancêtre à chacun des noeuds
        '''
        d1,p1=self.dijkstra(n1,-1)
        d2,p2=self.dijkstra(n2,-1)
        dict={}
        for a in list(d1.keys()):
            if a in list(d2.keys()) :
                dict[a.get_id()]=(d1[a],d2[a])
        return dict

    def tri_topologique(self):
        '''
        output: (int list) list; liste de listes de noeuds triés topologiquement
        '''
        g=self.copy()
        res=[]
        cofeuilles=[]
        nl=g.get_node()
        for n in nl:
            if n.get_parent_ids()==[]:
                cofeuilles.append(n.get_id())
        while cofeuilles!=[] :
            pocol=[]
            for c in cofeuilles:
                n=g.get_node_by_id(c)
                for child in n.get_children_ids():
                    if child not in cofeuilles and child not in pocol:
                        pocol.append(child)
            res.append(cofeuilles)
            g.remove_nodes_by_id(cofeuilles)
            cofeuilles=[]
            for i in pocol:
                n=g.get_node_by_id(i)
                if n.get_parent_ids()==[]:
                    cofeuilles.append(i)
        if g.get_node()!=[]:
            raise ValueError #Cycle détecté
        else:
            return res
        
    def profondeur(self, noeud=None):
        '''
        input : int ;id du noeud
        output : profondeur
        
        si le noeud est à None on renvoie la profondeur du graphe, sinon la profondeur du noeud
        '''
        if noeud == None :
            return len(self.tri_topologique())
        tri = self.tri_topologique()
        for i in range(len(tri)) : 
            for j in range(len(tri[i])) : 
                if tri[i][j] == noeud : 
                    return i+1

        raise ValueError


    def plusLongChemin(self,u,v) : 
        '''
        input : node, node
        output : int, node list
        
        renvoie la distance et le plus long chemin entre deux noeuds d'un même graphe
        '''
        Tri = self.tri_topologique()
        taille = len(Tri)
        pos = 0
        #on récupère l'ensemble dans lequel est le noeud u
        for i in range(taille) : 
            for j in range(len(Tri[i])) : 
                if Tri[i][j] == u :
                    pos = i
                    break
                    
        #on déclare et initialise nos dictionnaires
        dist = {u:0}
        prev = {}

        b = False
        
        #on parcourt les ensembles suivants
        for ens in range(pos+1, taille):
            if b :
                break
            for elt in Tri[ens] :
                dist[elt] = 0
                
                for p in self.get_node_by_id(elt).get_parent_ids() :
                    if p in dist.keys() and dist[p] >= dist[elt] : 
                        dist[elt] = dist[p] + 1
                        prev[elt] = p
                        
                if elt == v : 
                    b = True
                    break
                    
        #on crée le chemin
        vv = v
        res = [vv]
        while u not in res : 
            vv = prev[vv]
            res.insert(0,vv)
        print(dist)
        return dist[v],res
    
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
#classmethod
def parallel(g1,g2):
    ''' 
    input : open_digraph, open_digraph; graphes à fusionner
    output : open_digraph 
    renvoie un nouveau graphe qui est la composition parallele des graphes donnes
    '''     
    ge=g1.copy()
    ge.iparallel(g2)
    return ge
#classmethod
def compose(g,f):
    '''
    input : open_digraph, open_digraph; graphes f et g à composer
    output : open_digraph 
    
    renvoie un nouveau graphe qui est la composition sequentielle des graphes donnes, ie f 'rond' g
    '''    
    compo=g.copy()
    compo.icompose(f.copy())
    return compo

def min(l, f):
    '''
    input:node list, node->int dict;
    output: node; l'élément de la liste qui est associé au plus petit entier
    '''
    u=l[0]
    for v in l:
        if f[v]>f[u]:
            u=v
    return u
            

