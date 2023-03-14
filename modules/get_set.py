class get_set:
    '''Classe dans laquelle on regroupe toutes les méthodes
    'getter' et 'setter' de la classe open_digraph
    '''
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