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
        return (node(self.id, self.label, self.parents, self.children))

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
        self.parents = l

    def set_children_ids (self, l) : 
        '''
        input: int list; 
        '''
        self.children = l

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
        '''
        output: open_digraph; copie du graph
        '''
        return (open_digraph(self.inputs, self.outputs, self.nodes.values()))

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
        for n in ln : 
            self.inputs.append(n.get_id())
            self.nodes[n.get_id()] = n

    def set_outputs_ids (self, ln) : 
        ''' 
        input: node list; ln une liste de noeuds
        '''
        for n in ln : 
            self.outputs.append(n.get_id())
            self.nodes[n.get_id()] = n

    def add_input_id(self, n) : 
        ''' 
        input: node ; n un noeud
        '''
        self.inputs.append(n.get_id())
        self.nodes[n.get_id()] = n

    def add_output_id(self, n) : 
        ''' 
        input: node ; n un noeud
        '''
        self.outputs.append(n.get_id())
        self.nodes[n.get_id()] = n

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
        n = node(ID,label, parents, children)
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






    