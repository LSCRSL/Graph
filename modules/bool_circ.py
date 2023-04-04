from modules.open_digraph import *

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
    def formule_arbre(cls,*args) : 
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
        print(g)
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
                
                #nv noeud seul parent
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
        input : n : int , 
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
        input : n : int
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
            graph.add_node(s[i])
        return cls(graph)
    
    def copies(self, idH, idB) : 
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation copie dans le graphe
        '''
        noeudH = self.get_node_by_id(idH)
        l = noeudH.get_label()
        noeudB = self.get_node_by_id(idB)
        childNB = noeudB.get_children_ids()
        self.add_edge(idH,childNB[0])
        for i in range(1,len(childNB)) : 
            id2 = self.add_node(l, {},{childNB[i]:1})

        self.remove_node_by_id(idB)
        print(self.get_node_by_id(idH))

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
            self.fusion(idH,idB,True, "0")
            p_node = noeudH.get_parent_ids()
            print(idH)
            print(p_node)
            for i in range(len(p_node)) : 
                self.remove_edge(p_node[i], idH)
                id = self.add_node(" "" ", {p_node[i]:1}, {})
                print(id)
                
        
    def porte_OU(self, idH, idB) : 
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation porte OU dans le graphe
        '''
        noeudH = self.get_node_by_id(idH)
        if noeudH.get_label() == "0" : 
            self.remove_node_by_id(idH)
        else : 
            self.fusion(idH,idB,True, "1")
            p_node = noeudH.get_parent_ids()
            for i in range(0,len(p_node)) : 
                id = self.add_node(" ", {p_node[i]:1}, {})
                self.remove_edge(idH, p_node[i])

    def porte_OU_EX(self, idH, idB) : 
        '''
        inputs : int : id noeud haut, int : id noeud bas
        
        effectue la transformation porte OU EXCLUSIF dans le graphe
        '''
        noeudH = self.get_node_by_id(idH)
        if noeudH.get_label() == "0" : 
            self.remove(idH)
        else : 
            self.remove(idH)
            c_node = self.get_node_by_id(idB).get_children_ids()
            id = self.add_node("~", {idB:1}, {})
            for i in range(0,len(c_node)) : 
                self.remove_edge(idH, c_node[i])
                self.add_edge(id, c_node[i])

    def elmt_neutres(self, id) : 
        '''
        inputs : int : id noeud à modifier
        
        effectue la transformation elements neutres dans le graphe
        '''
        noeud = self.get_node_by_id(id)
        if noeud.get_label() == "&" : 
            noeud.set_label("1")
        else : 
            noeud.set_label("0")

    

            



    

        
            

        

        
     
    
        



