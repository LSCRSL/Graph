from modules.open_digraph import *
class bool_circ(open_digraph):
    '''
    Classe des circuits booléens
    '''
    def __init__(self,g) :
        super().__init__(g.get_input_ids(), g.get_output_ids(), g.get_node())
        if not self.is_well_formed():
            raise ValueError
    
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