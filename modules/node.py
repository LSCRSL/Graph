class node:
    '''
    Classe node
    '''
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
        output: int list; 
        '''
        return list(self.parents.keys())

    def get_children_ids(self) : 
        '''
        output: int list; 
        '''
        return list(self.children.keys())
    
    def get_parent_mult(self) : 
        '''
        output: int list; 
        '''
        return list(self.parents.values())

    def get_children_mult(self) : 
        '''
        output: int list; 
        '''
        return list(self.children.values())

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
        input: int-> int dict; 
        '''
        self.parents = l

    def set_children_ids (self, l) : 
        '''
        input: int-> int dict; 
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

    def remove_parent_once(self, id) : 
        '''
        input: int; id du parent pour lequel on retire une multiplicité
        '''
        if id in self.get_parent_ids() : 
            self.parents[id] -= 1
            if self.parents[id] == 0 :
                del self.parents[id]
        
    def remove_child_once(self, id) : 
        '''
        input: int; id de l'enfant pour lequel on retire une multiplicité 
        '''
        if id in self.get_children_ids() : 
            self.children[id] -= 1
            if self.children[id] == 0 :
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
        mult = self.get_parent_mult()
        cpt = 0
        for i in mult : 
            cpt += i
        return cpt

    def outdegree(self) : 
        """
        output : int; le degre entrant du noeud
        """
        mult = self.get_children_mult()
        cpt = 0
        for i in mult : 
            cpt += i
        return cpt

    def degree(self) : 
        '''
        output: int; la somme des degrés entrant et sortant du noeud
        '''
        return self.indegree() + self.outdegree()