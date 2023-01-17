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
        return (self.values())
    
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
        return (self.values())