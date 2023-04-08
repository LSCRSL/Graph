class connectivity:
    '''Classe dans laquelle on regroupe toutes les méthodes
    relatives aux compositions et parallélisme entre deux graphes
    '''

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

    def connected_components(self) : 
        '''
        output: int -> int dict;
        méthode qui associe à chaque noeud du graphe un numéro de composante connexe
        '''
        cpt = 0
        dict = {}
        for node in self.get_node() :
            if node.get_id() not in dict.keys() :
                self.same_graph(node, cpt, dict)
                cpt += 1
        return (cpt,dict)
    
    def same_graph(self,node, cpt, dict) :
        '''
        input:node, int, int->int dict;
        Sous-fonction pour la méthode connected_components()
        '''
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