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
    def formule_arbre(cls,s):
        '''
        input: string; formule propositionnelle à traduire en arbre
        output: bool_circ * (string list); tuple composé du circuit bolléen et de la liste des noms des variables
        '''
        en=node(0,'',{},{})
        g=open_digraph([],[0],[en])
        current_node=0
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
                noeud.set_label('')
        return (cls(g),list(trouve.keys()))
