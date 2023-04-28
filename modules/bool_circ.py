from modules.open_digraph import *
import math

class bool_circ(open_digraph):
    '''
    Classe des circuits booléens
    '''
    def __init__(self,g) :
        super().__init__(g.get_input_ids(), g.get_output_ids(), g.get_node())
        '''if not self.is_well_formed():
            raise ValueError'''
    
    def is_cyclic(self) : 
        '''
        output : bool;
        renvoie vrai si le graphe est acyclique
        '''
        def is_cycle(g) : 
            if g.get_id_node_map() == {} : 
                return True
            else : 
                l_oupt = g.get_output_ids()
                if l_oupt == [] : 
                    return False
                else :
                    g.remove_node(l_oupt.pop(0))
                    return is_cycle(g)
        return is_cycle(self.copy())

    def is_well_formed(self):
        '''
        output:bool; renvoie vrai si les propriétés d'un circuit booléen sont respectées
        '''
        if self.is_cyclic() :
            return False 
        else : 
            n = self.get_node()
            outp = self.get_input_ids()
            inp = self.get_input_ids()
            for node in n : 
                l = node.get_label()
                if  l == '' : 
                    if node.get_id() in outp or node.get_id() in inp :
                        continue 
                    elif node.indegree() != 1 :
                        return False
                elif l == '&' or l == '|' : 
                    if node.outdegree() != 1 :
                        return False
                elif l == '~' :
                    if node.indegree() != 1 and node.outdegree() != 1 :
                        return False
                elif l == '0' or l == '1':
                    if node.indegree() != 0 and node.outdegree() != 1 : 
                        return False
                elif  l != '^' :
                    return False
            return True
    
    @classmethod
    def formule_arbre(cls,*args) : #également appelée "parse_parenthese()"
        '''
        input: *args
        Méthode de class qui construit un circuit booléen à l'aide de la chaîne de 
        caractères donnée en argument
        '''
        g = open_digraph.empty()
        for s in args : 
            current_node= g.add_node('', {}, {})
            g.add_output_node(current_node)
            s2=''
            for char in s:
                if char=='(':
                    cn=g.get_node_by_id(current_node)
                    cn.set_label(cn.get_label()+s2)
                    newn=g.add_node('',None,{current_node:1})
                    current_node=newn
                    s2=''
                elif char==')':
                    cn=g.get_node_by_id(current_node)
                    cn.set_label(cn.get_label()+s2)
                    current_node=cn.get_children_ids()[0]
                    
                    s2=''
                elif char=='0' or char=='1':
                    s2=s2+char
                elif char!='&' and char!='|' and char!= '~' and char!='^' and char!='':
                    s2=s2+char
                else:
                    s2=char
        trouve ={}
        for noeud in g.get_node():
            label=noeud.get_label()
            id=noeud.get_id()
            char=label
            if char!='&' and char!='|' and char!= '~' and char!='^' and char!='' and char!='0' and char!='1':
                if label in trouve.keys():
                    g.fusion(trouve[label], id, label)
                else:
                    trouve[label] = id
                g.add_input_id(id)
                noeud.set_label('')
        return (cls(g),list(trouve.keys()))
    
    @classmethod
    def random(cls,size,input=1,output=1):
        '''
        input: int, int, int; taille (en nb de noeuds), nb d'input, nb d'output
        output: bool_circ; circuit booléen généré aléatoirement
        '''
        if size<input+output:
            raise ValueError
        g=open_digraph.random(size,2,0,0,"DAG")
        g.display("g",True)
        iln=[]
        oln=[]
        for node in g.get_node():
            if len(node.get_parent_ids())==0:
                iln.append(node)
            if len(node.get_children_ids())==0:
                oln.append(node)
        g.set_input_ids(iln)
        g.set_outputs_ids(oln)
        binaire = ['|', '&', '^']
        nb_bin = len(binaire)
        for noeud in g.get_node() : 
            if noeud.indegree() == 1 and noeud.outdegree() == 1 : 
                noeud.set_label('~')
            elif noeud.indegree() > 1 and noeud.outdegree() == 1 :
                u = rand.randrange(0,nb_bin)
                noeud.set_label(binaire[u])
            elif noeud.indegree() > 1 and noeud.outdegree() > 1 :
                parents = noeud.get_parent_ids()
                mult_parents = noeud.get_parent_mult()
                #noeud parent
                u = rand.randrange(0,nb_bin)
                dic_parent = {}
                for i in range(len(parents)):
                    dic_parent[parents[i]] = mult_parents[i]
                new_node_id = g.add_node(binaire[u], dic_parent, {noeud.get_id():1})
                #nouveau noeud seul parent
                for p in parents : 
                    g.remove_parallel_edges(p,noeud.get_id())
                noeud.set_parent_ids(new_node_id)
        while len(g.get_input_ids())!=input or len(g.get_output_ids())!=output:
            linp=g.get_input_ids()
            if len(linp)>input:
                n1=linp[0]
                n2=linp[1]
                g.fusion(n1,n2)
            elif len(linp)<input:
                for id in g.get_node_ids():
                    if id not in g.get_input_ids():
                        g.add_input_node(id)
                        break
            lout=g.get_output_ids()
            if len(lout)>output:
                n1=lout[0]
                n2=lout[1]
                g.fusion(n1,n2)
            elif len(lout)<output:
                for id in g.get_node_ids():
                    if id not in g.get_output_ids() and id not in g.get_input_ids():
                        g.add_output_node(id)
                        break
        return cls(g)
    
    @classmethod
    def half_adder(cls, n ) : 
        '''
        input : int 
        output : bool_circ

        renvoie adder n avec le carry = 0
        '''
        #appel de la fonction adder
        g = cls.adder(n).copy()
        for ID in g.get_input_ids() : 
            if g.get_node_by_id(ID).get_label() == 'c' : 
                g.get_input_ids().remove(ID)
                g.get_node_by_id(ID).set_label('0')
        return g
    
    @classmethod
    def adder(cls, n) : 
        '''
        input : int
        output : bool_circ

        renvoie le registre de taille n
        '''
        if n == 0 : 
            i0 = node(10, 'a', {}, {1:1})
            i1 = node(11, 'b', {}, {2:1})
            i2 = node(12, 'c', {}, {3:1})
            a=node(1,"",{10:1},{4:1, 6:1})
            b=node(2,"",{11:1},{4:1,6:1})
            c=node(3,"",{12:1},{8:1,7:1})
            d=node(4,'^', {1:1, 2:1},{5:1})
            e=node(5,"",{4:1},{8:1,7:1})
            f=node(6,'&',{2:1,1:1},{9:1})
            g=node(7,'&',{3:1,5:1},{9:1})
            h=node(8,'^',{3:1,5:1},{14:1})
            i=node(9,'|',{6:1, 7:1},{13:1})
            o0 = node(13, "cp", {9:1}, {})
            o1 = node(14, 'r', {8:1}, {})
            g = open_digraph([10,11,12],[13,14], [a,b,c,d,e,f,g,h,i, i0, i1,i2, o0,o1] )
            return cls(g)
        else :
            g1 = cls.adder(n-1)
            g2 = cls.adder(n-1)
            c = -1
            c_prime = -1
            #on récupère l'id noeud d'input c
            for id in g1.get_input_ids() : 
                if g1.get_node_by_id(id).get_label() == 'c' : 
                    c = id + g2.max_id() -g2.min_id() + 1
            #on recupere l'id noeud output c'
            for id in g2.get_output_ids() : 
                if g2.get_node_by_id(id).get_label() == "cp" : 
                    c_prime = id
            g3 = open_digraph.parallel(g1, g2)
            #on fusionne les noeuds
            g3.fusion(c,c_prime,"")
            g3.get_input_ids().remove(c)
            return g3

    @classmethod  
    def registre(cls,n, taille) : 
        '''
        inputs : int, int
        ouputs : bool_circ 

        retourne un circuit booleen qui représente le registre instancié en l'entier
        '''
        s = bin(n)[2:]
        if len(s) > taille : 
            raise ValueError
        else : 
            for i in range(len(s),taille) : 
                s = "0" + s
        graph = open_digraph.empty()
        for i in range(0,taille) : 
            id = graph.add_node(s[i])
            graph.add_output_node(id)
        
        return cls(graph)
    
    def copies(self, idH, idB) : 
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation copie dans le graphe
        '''
        noeudH = self.get_node_by_id(idH)
        l = noeudH.get_label()
        #print(l)
        noeudB = self.get_node_by_id(idB)
        childNB = noeudB.get_children_ids()
        self.add_edge(idH,childNB[0])
        for i in range(1,len(childNB)) : 
            id2 = self.add_node(l, {},{childNB[i]:1})
            self.add_input_id(id2)
            
            #print("new :")
            #print(n.get_label())
        self.remove_node_by_id(idB)

    def porte_Non(self,idH,idB ) : 
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation porte NON dans le graphe
        '''
        noeudH = self.get_node_by_id(idH)
        l = noeudH.get_label()
        self.fusion(idH,idB,True,str(1-int(l)))

    def porte_Et(self, idH, idB) :
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation porte ET dans le graphe
        '''
        noeudH = self.get_node_by_id(idH)
        if noeudH.get_label() == "1" : 
            self.remove_node_by_id(idH)
        else : 
            nodeB=self.get_node_by_id(idB)
            for parent in nodeB.get_parent_ids():
                if parent!=idH:
                    self.add_node('x',{parent:1},{})
                    self.remove_edge(parent,idB)
            self.fusion(idH,idB,True,"0")
                
        
    def porte_OU(self, idH, idB) : 
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation porte OU dans le graphe
        '''
        noeudH = self.get_node_by_id(idH)
        if noeudH.get_label() == "0" : 
            self.remove_node_by_id(idH)
        else : 
            nodeB=self.get_node_by_id(idB)
            for parent in nodeB.get_parent_ids():
                if parent!=idH:
                    self.add_node("",{parent:1},{})
                    self.remove_edge(parent,idB)
            self.fusion(idH,idB,True, "1")

    def porte_OU_EX(self, idH, idB) : 
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation porte OU EXCLUSIF dans le graphe
        '''
        print(self.get_node())
        noeudH = self.get_node_by_id(idH)
        if noeudH.get_label() == "0" : 
            self.remove_node_by_id(idH)
        else : 
            self.remove_node_by_id(idH)
            c_node = self.get_node_by_id(idB).get_children_ids()
            id = self.add_node("~", {idB:1}, {})
            for i in range(0,len(c_node)) : 
                #self.remove_edge(idH, c_node[i])
                self.add_edge(id, c_node[i])
            self.remove_edge(idB, self.get_node_by_id(id).get_children_ids()[0])

    def elmt_neutres(self, id) : 
        '''
        inputs : int : id noeud à modifier
        
        effectue la transformation elements neutres dans le graphe
        '''
        noeud = self.get_node_by_id(id)
        if noeud.get_label()== "&"  or noeud.get_label()=="1": 
            noeud.set_label("1")
        else : 
            noeud.set_label("0")

    def transformations(self, id_noeud) : 
        '''
        input : int ; id du noeud
        output: bool; true si la transformation a eu lieu

        regarde si l'on peut appliquer une transformation et si oui, l'effectue
        '''
        a_lieu = False
        noeud = self.get_node_by_id(id_noeud)
        enf = noeud.get_children_ids()
        nb_enf = len(enf)
        if (noeud.get_label() != 0 and noeud.get_label() != 1) : 
            self.elmt_neutres(id_noeud)
            a_lieu = True 
        elif nb_enf == 1 and (noeud.get_label() == '0' or noeud.get_label() == '1'): #la 2ème condition est redondante puisque c'est elif
                    id_enf = enf[0]
                    label_enf = self.get_node_by_id(id_enf).get_label()
                    if  label_enf == "" : 
                        self.copies(id_noeud,id_enf)
                        a_lieu = True
                    elif label_enf == "^" : 
                        print(id_noeud)
                        self.porte_OU_EX(id_noeud,id_enf)
                        a_lieu = True
                    elif label_enf == "~" : 
                        self.porte_Non(id_noeud,id_enf)
                    elif label_enf == "|" : 
                        self.porte_OU(id_noeud,id_enf)
                        a_lieu = True
                    elif label_enf == "&" : 
                        self.porte_Et(id_noeud,id_enf)
                        a_lieu = True
        return a_lieu

    def evaluate(self):
        '''
        évalue le cicruit booléen en appliquant les règles
        "ET", "OU", "OU EXCLUSIF", "NON", "Copies" et "éléments neutres"
        '''
        '''
        self.display("graphbis", True)
        
        cofeuilles=[]
        nl=self.get_node()
        for n in nl:
            if n.get_parent_ids()==[] and n.get_children_ids()!=[]:
                cofeuilles.append(n.get_id())

        while cofeuilles!=[] and self.profondeur()>2:
            for c in cofeuilles:
                n=self.get_node_by_id(c)
                for child in n.get_children_ids():
                    cnode=self.get_node_by_id(child)
                    lab=cnode.get_label()
                    if lab=='' and cnode.get_children_ids()!=[]:
                        self.copies(c,child)
                    elif lab=='~':
                        self.porte_Non(c,child)
                    elif lab=='&':
                        self.porte_Et(c,child)
                    elif lab=="|":
                        self.porte_OU(c,child)
                    elif lab=='^':
                        self.porte_OU_EX(c,child)
            self.evaluate()
        gl=self.connected_list()
        for g in gl:
            rml=[]
            for n in g.get_node():
                if n.get_label()=='x':
                    for nb in g.get_node_ids():
                        rml.append(nb)
            if rml !=[]:
                self.remove_nodes_by_id(rml)
        for nid in self.get_node_ids():
            self.elmt_neutres(nid)
        '''
        #pb d'indices
        transform = True
        while transform : 
            transform = False
            for node in self.get_node():
                if node != None and node.get_parent_ids() == [] and node in self.get_node() : #la dernière condition est redondante non? puisqu'on prend déjà les node qui sont dans self.get_node()...
                    if self.transformations(node.get_id()) : 
                        transform = True

    def asso_xor(self, idh, idb):
        '''
        inputs: int, int ; id du noeud '^' en amont et de son fils de label '^'

        effectue l'associativité de XOR
        '''
        nh, nb = self.get_node_by_id(idh), self.get_node_by_id(idb)
        if nh.get_label()!='^' or nb.get_label()!='^':
            raise ValueError
        else:
            parents=nh.get_parent_ids()
            for pid in parents:
                self.add_edge(pid,idb)
                self.remove_edge(pid,idh)
            self.remove_edge(idh,idb)
            self.remove_node(idh)

    def asso_copie(self,idh,idb):
        '''
        inputs: int, int ; id du noeud copie ' ' en aval et de son parent de label ' '

        effectue l'associativité de la copie
        '''
        nh, nb = self.get_node_by_id(idh), self.get_node_by_id(idb)
        labh, labb = nh.get_label(), nb.get_label()
        if (labh!='' and labh!=' ') or (labb!='' and labb!=' ') :
            raise ValueError
        else:
            children=nb.get_children_ids()
            for cid in children:
                self.add_edge(idh,cid)
                self.remove_edge(idb, cid)
            self.remove_edge(idh,idb)
            self.remove_node(idb)

    def invol_xor(self, idOE, idC):
        '''
        inputs: int, int ; id du noeud OU exclusif '^' et d'un des parents de label ''

        effectue l'involution de XOR
        '''
        no, nc = self.get_node_by_id(idOE), self.get_node_by_id(idC)
        labo, labc = no.get_label(), nc.get_label()
        if (labo!='^') or (labc!='' and labc!=' ') :
            raise ValueError
        else:
            i=0
            tab=no.get_parent_ids()
            while tab[i]!=idC:
                i+=1
            mult=no.get_parent_mult()[i]
            self.remove_parallel_edges(idC, idOE)
            if mult%2==1: #on laisse une arrête si le nombre d'arrête est impair
                self.add_edge(idC,idOE)

    def effacement(self, idh, idb):
        '''
        inputs: int, int ; id du noeud d'operation ou valeur quelconque en amont et de son fils copie de label ' '

        effectue l'effacement
        '''
        nh, nb = self.get_node_by_id(idh), self.get_node_by_id(idb)
        labh, labb = nh.get_label(), nb.get_label()
        if (labb!='' and labb!=' ') :
            raise ValueError
        else:
            parents=nh.get_parent_ids()
            self.remove_node_by_id(idb)
            self.remove_node_by_id(idh)
            for pid in parents:
                id = self.add_node('', {pid:1}, {})
    

    def non_xor(self, idh,idb) : 
        '''
        inputs: int, int ; id du noeud d'operation ou valeur quelconque en amont et de son fils copie de label ' '

        effectue le non à travers xor
        '''
        noeudH = self.get_node_by_id(idh)
        noeudB = self.get_node_by_id(idb)
        parentH = noeudH.get_parent_ids()
        #on enleve l'arete entre les deux noeuds
        self.remove_edge(idh,idb)
        #on enleve l'arete entre ~ et son parent
        self.remove_edge(parentH[0], idh)
        self.add_edge(parentH[0], idb)
        childrenB = noeudB.get_children_ids()
        self.remove_edge(idb, childrenB[0])
        self.add_edge(idh,childrenB[0])
        self.add_edge(idb,idh)
        

    def non_copie(self, idh,idb) : 
        '''
        inputs: int, int ; id du noeud d'operation ou valeur quelconque en amont et de son fils copie de label ' '

        effectue le non à travers copie
        '''
        noeudH = self.get_node_by_id(idh)
        noeudB = self.get_node_by_id(idb)
        parentH = noeudH.get_parent_ids()
        self.add_edge(parentH[0],idb)
        self.remove_node_by_id(idh)
        for child in noeudB.get_children_ids() : 
            self.remove_edge(idb, child)
            id = self.add_node("~", {idb:1}, {child:1})
                
    def invol_non(self,idh,idb) : 
        '''
        inputs: int, int ; id du noeud d'operation ou valeur quelconque en amont et de son fils copie de label ' '

        effectue l'involution de non
        '''
        noeudH = self.get_node_by_id(idh)
        noeudB = self.get_node_by_id(idb)
        parentH = noeudH.get_parent_ids()
        childB = noeudB.get_children_ids()
        self.add_edge(parentH[0], childB[0])
        self.remove_node_by_id(idh)
        self.remove_node_by_id(idb)

    def eval(self) : 
        '''
        méthode qui évalue le cicruit booléen 
        '''
        #ne pas utiliser les cofeuilles, avoir une liste de noeud (au depart tous les noeuds)  (OK)
        # et regarder si l'on peut appliquer une transformation (OK)
        #si ce n'est pas le cas on enleve le noeud de la liste, (OK)
        # lorsqu'il y a un transformation de faite on ajoute à la liste les noeuds voisins (s'ils ne sont pas deja dedans) (OK)
        #et on regarde si l'on peut effectuer une transformation, dans la cad contraire on enleve le noeud de la liste etc ... 
        #on repete ce processus tant que la liste n'est pas vide.
        #pb le graphe ne se modifie pas
        noeuds = self.get_node()
        while noeuds != [] : 
            for n in noeuds : 
                transf = False
                enf = n.get_children_ids()
                if n.get_label() == "^" and len(enf) == 1 and self.get_node_by_id(enf[0]).get_label() == "^" :
                    ne = self.get_node_by_id(enf[0])
                    self.asso_xor(n.get_id(), enf[0])
                    transf = True
                    #faire nouveau voisinage
                    if ne not in noeuds : 
                        noeuds.append(ne)
                elif n.get_label() == '' : 
                    i = 0
                    for e in enf : 
                        ne = self.get_node_by_id(e)
                        if ne.get_label() == '' : 
                            self.asso_copie(n.get_id(), e)
                            transf = True
                            if ne not in noeuds : 
                                noeuds.append(ne)
                        if ne.get_label() == '^' and n.get_children_mult()[i] > 1 : 
                            self.invol_xor(n.get_id(), e)
                            transf = True
                            if ne not in noeuds : 
                                noeuds.append(ne)
                        i+=1
                elif n.get_label() == '~' :
                    ne = self.get_node_by_id(enf[0])
                    if ne.get_label() == "^" : 
                        self.non_xor(n.get_id(), enf[0])
                        transf = True
                        if ne not in noeuds : 
                            noeuds.append(ne)
                    if ne.get_label() == '' : 
                        self.non_copie(n.get_id(), enf[0])
                        transf = True
                        if ne not in noeuds : 
                            noeuds.append(ne)
                    if ne.get_label() == '~' : 
                        self.invol_non(n.get_id(), enf[0])
                        transf = True
                        if ne not in noeuds : 
                                noeuds.append(ne)
                elif n.get_label() != ''  and len(enf) == 1 :
                    ne = self.get_node_by_id(enf[0])
                    if ne.get_label() == '' and len(ne.get_children_ids()) == 0 :
                        #il y a plus l enfant dans le graphe
                        self.effacement(n.get_id(), enf[0])
                        transf = True
                        if ne not in noeuds : 
                            noeuds.append(ne)
                if not transf : 
                    noeuds.remove(n)
        self.display("ok")

    
    @classmethod
    def encodeur(cls):
        '''
        input: int, int, int, int; des bits à encoder
        renvoie le cicruit booléen correspondant à l'encodeur
        '''
        i0=node(0,'',{},{4:1})
        i1=node(1,'',{},{5:1})
        i2=node(2,'',{},{6:1})
        i3=node(3,'',{},{7:1})
        a=node(4,'',{0:1},{8:1,12:1,13:1})
        b=node(5,'',{1:1},{9:1,12:1,14:1})
        c=node(6,'',{2:1},{10:1,13:1,14:1})
        d=node(7,'',{3:1},{11:1,12:1,13:1,14:1})
        o0=node(8,'',{4:1},{})
        o1=node(9,'',{5:1},{})
        o2=node(10,'',{6:1},{})
        o3=node(11,'',{7:1},{})
        n1=node(12,'^',{4:1,5:1,7:1},{15:1})
        n2=node(13,'^',{4:1,6:1,7:1},{16:1})
        n3=node(14,'^',{5:1,6:1,7:1},{17:1})
        o4=node(15,'',{12:1},{})
        o5=node(16,'',{13:1},{})
        o6=node(17,'',{14:1},{})
        g=open_digraph([0,1,2,3],[8,9,10,11,15,16,17],[i0,i1,i2,i3,a,b,c,d,o0,o1,o2,o3,o4,o5,o6,n1,n2,n3])
        return cls(g)

    @classmethod
    def decodeur(cls):
        '''
        input: int * 7; bits à évaluer
        renvoie le circuit booléen correspondant au décodeur
        '''
        b=bool_circ.encodeur()
        for i in range (0,3):
            b.add_nodes(node(18+i,'',{},{12+i:1}))
            b.add_input_id(18+i)
        for i in range(4,8):
            n=node(17+i,'^',{i:1},{i+4:1})
            b.add_nodes(n)
            b.add_edge(i,17+i)
            b.remove_edge(i,i+4)
        n1=node(25,'&',{15:1,16:1,26:1},{21:1})
        n2=node(26,'~',{17:1},{25:1})
        b.add_nodes_list([n1,n2])
        b.add_edge(15,25)
        b.add_edge(16,25)
        b.add_edge(17,26)
        n3=node(27,'&',{15:1,17:1,28:1},{22:1})
        n4=node(28,'~',{16:1},{27:1})
        b.add_nodes_list([n3,n4])
        b.add_edge(15,27)
        b.add_edge(17,27)
        b.add_edge(16,28)
        n5=node(29,'&',{16:1,17:1,30:1},{23:1})
        n6=node(30,'~',{15:1},{29:1})
        b.add_nodes_list([n5,n6])
        b.add_edge(16,29)
        b.add_edge(17,29)
        b.add_edge(15,30)
        n7=node(31,'&',{16:1,17:1,15:1},{24:1})
        b.add_nodes(n7)
        b.add_edge(15,31)
        b.add_edge(16,31)
        b.add_edge(17,31)
        return cls(b)

        
def calcul(a,b,taille) :
    '''
    input:int,int,int;
    output: bool_circ
    
    Fonction pour tester la méthode evaluate() sur l'additionneur
    '''
    n = math.log(taille,2)
    #if type(n) != int : 
        #raise ValueError
    g1 = bool_circ.registre(a,taille)
    g1.display("g1",True)
    g2 = bool_circ.registre(b,taille) 
    g2.display("g2",True)
    g = bool_circ.parallel(g1,g2)
    g.display("g",True)
    ha = bool_circ.half_adder(n)
    ha.icompose(g)
    ha.display("ha",True)
    for n in g.get_node() : 
        c_id = n.get_parent_ids()
        if (c_id == []) & ( (n.get_label() == "0") | (n.get_label() == "1")): 
            ha.fusion(n.get_id(),n.get_children_ids()[0],True,n.get_label())
            ha.fusion(n.get_id(),n.get_children_ids()[0],True,n.get_label()) 
            ha.add_input_id(n.get_id()) 
    bc = bool_circ(ha)

    bc.display("G_final",True)
    bc.evaluate()
    bc.display("G_eval", True)
    return bc

