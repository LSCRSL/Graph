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
        return "ID: "+str(self.id)+"  Label:"+self.label+"  Parents:"+str(self.parents)+"  Children:"+str(self.children) +"\n"
    def __repr__(self):
        return str(self)
    def copy(self):
        return (node(self.id, self.label, self.parents, self.children))

    '''les getters'''
    def get_id(self):
        return self.id
    def get_label(self) :
        return self.label
    def get_parent_ids(self) : 
        return self.parents.keys()
    def get_children_ids(self) : 
        return self.children.keys()

    '''les setters'''
    def set_id (self,x) : 
        self.id = x
    def set_label(self, x) :
        self.label = x
    def set_parent_ids(self, l) : 
        self.parents = l
    def set_children_ids (self, l) : 
        self.children = l
    def add_child_id (self, id, mult) : 
        if id in self.get_children_ids() :
            self.children[id] += mult
        else : 
            self.children[id] = mult
    def add_parents_id(self, id, mult) :
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
        return self.nodes.__repr__()
    @classmethod
    def empty(cls):
        return cls([],[],[])     
    def copy(self):
        return (open_digraph(self.inputs, self.outputs, self.nodes.values()))
    '''les getters'''
    def get_input_ids(self) : 
        return self.inputs
    def get_output_ids(self) : 
        return self.outputs
    def get_id_node_map(self) :
        return self.nodes
    def get_node(self) : 
        return [n for (id,n) in self.nodes.items()]    
    def get_node_ids(self) : 
        return self.nodes.keys()
    def get_node_by_id(self,i) : 
        for (id,n) in self.get_id_node_map().items() :
            if id == i :
                return n
    def get_node_by_ids(self, l) :
        return [n for i in l for (id,n) in self.get_id_node_map().items() if i == id ]

    '''les setters'''
    ''' ln une liste de noeuds'''
    def set_input_ids(self, ln) : 
        for n in ln : 
            self.inputs.append(n.get_id())
            self.nodes[n.get_id()] = n

    def set_outputs_ids (self, ln) : 
        for n in ln : 
            self.outputs.append(n.get_id())
            self.nodes[n.get_id()] = n

    '''n un noeud'''
    def add_input_id(self, n) : 
        self.inputs.append(n.get_id())
        self.nodes[n.get_id()] = n

    def add_output_id(self, n) : 
        self.outputs.append(n.get_id())
        self.nodes[n.get_id()] = n

    def add_nodes(self, n ) : 
        self.nodes[n.get_id()] = n

    '''fonction récursive qui renvoie le prochain indice libre'''
    def f(self,i) :
        for (id,n) in self.nodes.items() : 
            if (i == id) : 
                i+=1
                self.f(i)
        return i

    '''méthode qui renvoie un indice non-utilisé dans le graphe'''
    def new_id(self) : 
        return self.f(0)

    '''méthode qui rajoute une arête du noeud source au noeud cible'''
    def add_edge(self,src,tgt) : 
        self.get_node_by_id(src).add_child_id(tgt, 1)
        self.get_node_by_id(tgt).add_parents_id(src,1)

    '''méthode qui rajoute une arête entre chacune des paires de edges'''
    def add_edges(self, edges) : 
        for (src,tgt) in edges : 
            self.add_edge(src,tgt)

    

    def add_node(self, label,parents, children) : 
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






    