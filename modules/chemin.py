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

class chemin:
    '''Classe dans laquelle on regroupe toutes les méthodes
    relatives aux chemins dans un open_digraph
    '''
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
        
        renvoie la profondeur du graphe si le paramètre noeud est à None, sinon renvoie la profondeur du noeud
        Profondeur graphe vide : 0
        '''
        if noeud == None :
            return len(self.tri_topologique())
        tri = self.tri_topologique()
        #on cherche notre noeuds dans le tri topologique
        for i in range(len(tri)) : 
            for j in range(len(tri[i])) : 
                if tri[i][j] == noeud : 
                    return i+1
        #leve une erreur si le noeud n'est pas dans le graphe
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
        #on cherche dans quel ensemble l_i est le noeud u
        for i in range(taille) : 
            for j in range(len(Tri[i])) : 
                if Tri[i][j] == u :
                    pos = i
                    break
        dist = {u:0}
        prev = {}
        b = False
        #on parcourt les ensembles après l_i jusqu'à tomber sur le noeud v
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
        #on regarde si le chemin est possible
        if v not in prev.keys() : 
            if u != v : 
                return -1,[]
            else :
                return 0,[u]
        #on crée le chemin
        vv = v
        res = [vv]
        while u not in res : 
            vv = prev[vv]
            res.insert(0,vv)
        return dist[v],res
    
