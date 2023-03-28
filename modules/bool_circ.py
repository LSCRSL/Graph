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
    
    def half_adder(self, n, registre1,registre2 ) : 
        '''
        input : n : int , registre1 : int, registre2 : int
        output : registre : int

        prend 2 registres de taille 2*{n+1} et renvoie le registre associe à la somme de ceux donnés en argument
        '''
        #appel de la fonction adder

        carry = 0
        
    
        return 0
    
    @classmethod
    def adder(cls, n) : 
        '''
        input : n : int , registre1 : int, registre2 : int
        output : registre : int

        prend 2 registres de taille 2*{n+1} et renvoie le registre associe à la somme de ceux donnés en argument
        '''
        if n == 0 : 
            a=node(1,'',{},{4:1, 6:1})
            b=node(2,'',{},{4:1,6:1})
            c=node(3,'',{},{8:1,7:1})
            d=node(4,'^', {1:1, 2:1},{5:1})
            e=node(5,'',{4:1},{8:1,7:1})
            f=node(6,'&',{2:1,1:1},{9:1})
            g=node(7,'&',{3:1,5:1},{9:1})
            h=node(8,'^',{3:1,5:1},{})
            i=node(9,'|',{6:1, 7:1},{})

            g = open_digraph([1,2,3],[8,9], [a,b,c,d,e,f,g,h,i] )
            return cls(g)
        else :
            return open_digraph.compose(open_digraph.parallel(open_digraph.identity(n),cls.adder(n-1)), open_digraph.parallel(cls.adder(n-1), open_digraph.identity(n)))
        
        



