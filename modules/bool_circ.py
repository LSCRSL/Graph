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
        g=open_digraph.random(size,3,0,0,"DAG")
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
        
        
        '''
        f1,f2 = True, True
        while f1:
            linp=g.get_input_ids()
            if len(linp)>input and input>=1:
                n1=g.linp[0]
                n2=g.linp[1]
                g.fusion(n1,n2)
            elif len(linp)<input:
                g.add_input_node(g.get_node_ids()[0])
            else:
                f1=False
        while f2:
            lout=g.get_output_ids()
            if len(lout)>output and output>=1:
                n1=lout[0]
                n2=lout[1]
                g.fusion(n1,n2)
            elif len(lout)<output:
                g.add_input_node(g.get_node_ids()[0])
            else:
                f2=False
        '''
        return cls(g)
    
    def half_adder(self, n, registre1,registre2 ) : 
        '''
        input : n : int , registre1 : int, registre2 : int
        output : registre : int

        prend 2 registres de taille 2*{n+1} et renvoie le registre associe à la somme de ceux donnés en argument
        '''

        carry = 0

    
        return 0
    
    def adder(self, n, registre1,registre2 ,carry) : 
        '''
        input : n : int , registre1 : int, registre2 : int
        output : registre : int

        prend 2 registres de taille 2*{n+1} et renvoie le registre associe à la somme de ceux donnés en argument
        '''
        
        

    
        return 0


