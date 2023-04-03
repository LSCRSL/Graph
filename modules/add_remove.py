from modules.node import *

class add_remove:
    '''Classe dans laquelle on regroupe toutes les méthodes
    pour ajouter et retirer un ou des éléments d'un open_digraph
    '''
    #ADD
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

    def add_node(self, label="",parents=None, children=None) : 
        ''' 
        inputs: string, int->int dict,int ->int dict; 
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

    #REMOVE
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

    #Méthode pour add
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