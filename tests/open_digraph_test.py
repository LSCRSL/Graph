import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *
from modules.bool_circ import *
from modules.matrice import *

class InitTest(unittest.TestCase):
    '''
    Classe pour tester les fonctions init
    '''
    def test_init_node(self):
        '''
        Méthode  pour tester la méthode
        __init__ de la classe node
        '''
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)

    def test_init_open_digraph(self):
        '''
        Méthode pour tester la méthode
        __init__ de la classe open_digraph
        '''
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1, 1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertIsInstance(G, open_digraph)
        self.assertListEqual(G.inputs, [3,4])
        self.assertListEqual(G.outputs, [5,6])


class NodeTest(unittest.TestCase):
    '''
    Classe pour tester les méthodes de 
    la classe node
    '''
    def test_copy_node(self):
        '''
        Méthode pour tester la fonction copy 
        de la classe node 
        '''
        x = node (1, 'f', {0:1},{})
        self.assertIsNot(x.copy(),x)

    def test_get_node(self) : 
        '''
        Méthode pour tester les getters de la classe node
        '''
        N = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        self.assertEqual(N.id, N.get_id())
        self.assertEqual(N.label, N.get_label())
        self.assertEqual(list(N.parents.keys()), N.get_parent_ids())
        self.assertEqual(list(N.children.keys()), N.get_children_ids())
    
    def test_set_node(self) : 
        '''
        Méthode pour tester les setters de la classe node
        '''
        N = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        N.set_id(1)
        N.set_label('f')
        N.set_children_ids({5:1,6:1,7:1})
        N.set_parent_ids({0:1,2:1})
        print(N.get_children_ids())
        print(N.get_parent_ids())
        N.add_child_id(9,1)
        N.add_parents_id(3,1)
        print('Après avoir rajouté un enfant : ')
        print(N.get_children_ids())
        print('Après avoir rajouté un parent : ')
        print(N.get_parent_ids())

class OpenDigraphTest (unittest.TestCase):
    '''
    Classe pour tester les méthodes de la classe open_digraph
    '''
    def test_copy_od(self):
        '''
        Méthode pour tester la fonction copy de la classe open_digraph 
        '''
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1,1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertIsNot(G.copy(),G)
    
    def test_get_dig(self) : 
        '''
        Méthode pour tester les getters de la classe open_digraph
        '''
        n0 = node(0, 'a', {2:1}, {1:1})
        n1 = node(1, 'b', {0:1}, {})
        i0 = node(2, 'c', {}, {0:1})
        G = open_digraph([2], [1], [n0,n1,i0])
        self.assertEqual(G.inputs, G.get_input_ids())
        self.assertEqual(G.outputs, G.get_output_ids())
        self.assertEqual(G.nodes, G.get_id_node_map())
        self.assertEqual([n0,n1,i0], G.get_node())
        self.assertEqual(n0, G.get_node_by_id(0))
        self.assertEqual([n0,n1,i0], G.get_node_by_ids([0,1,2]))

    def test_set_dig(self) : 
        '''
        Méthode pour tester les setters de la classe open_digraph
        '''
        G = open_digraph.empty()
        n0 = node(0, 'a', {2:1}, {1:1})
        n1 = node(1, 'b', {0:1}, {})
        i0 = node(2, 'c', {}, {0:1})
        G.set_input_ids([i0])
        G.set_outputs_ids([n1])
        self.assertEqual(G.inputs, G.get_input_ids())
        self.assertEqual(G.outputs, G.get_output_ids())
        self.assertEqual(G.nodes, G.get_id_node_map())
        self.assertEqual([i0,n1], G.get_node())

    def test_init_dig(self) : 
        '''
        Méthode pour tester les fonctions générales de la class open_digraph
        fonction TP1
        '''
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1,1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        
        print('L ID du nouveau noeud rajouté:')
        print(G.add_node('y', {2:1},{0:2} ))
        print(n2.get_children_ids())
        print(n2.get_children_mult())
        print(n0.get_parent_ids())
        print(n0.get_parent_mult())
        n = G.get_node_by_id(7)
        print(n.get_children_ids())
        
        print('On enlève toutes les aretes du n 7 au n 0 : ')
        G.remove_several_parallel_edges([(7,0)])
        print(n.get_children_ids())

        print('On enleve le n 7 et 6')
        G.remove_nodes_by_id([7,6])
        print(n2.get_children_ids())
        print(n0.get_parent_ids())


    def test_dig_well_formed(self) : 
        '''
        Méthode pour tester la fonction is_well_formed, 
        et vérifier que l'ajout d'inputs et d'outputs
        est correct
        
        '''
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1,1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        G.assert_is_well_formed()
        G.add_input_node(1)
        G.assert_is_well_formed()
        o1.add_parents_id(2,1)
        self.assertEqual(False, G.is_well_formed())
        G.remove_edge(2,6)
        G.assert_is_well_formed()
        G.add_output_node(2)
        G.assert_is_well_formed()

    def test_matrice(self) : 
        '''
        Méthode pour tester les fonctions de matrices
        '''
        
        print(random_int_list(2,1,-1))
        affiche_matrix(random_int_matrix(4,8,False))
        affiche_matrix(random_int_matrix(4,8))
        x = random_symetric_int_matrix(4,8,False)
        affiche_matrix(x)
        j = open_digraph.graph_from_adjacency_matrix(x)
        print(str(j))
        affiche_matrix(random_symetric_int_matrix(4,8))
        affiche_matrix(random_oriented_int_matrix(4,3,False))
        print("ex 6:")
        affiche_matrix(random_triangular_int_matrix(5,4,False))

        n0 = node(8, 'a', {2:1, 3:1, 4:1, 6:1}, {2:1, 7:1})
        n1 = node(1, 'o0', {6:1}, {})
        n2 = node(6, 'c', {2:1}, {1:1,8:1})
        i0 = node(3, 'i0', {}, {8:1})
        i1 = node(4, 'i1', {}, {8:1})
        o0 = node(2, 'b', {8:1}, {6:1, 8:1})
        o1 = node(7, 'o1', {8:1}, {})
        G = open_digraph([3,4], [1,7], [n0,n1,n2,i0,i1,o0,o1])
        G.assert_is_well_formed()
        print(G.dict_of_graph())
        affiche_matrix(G.adjacency_matrix())
        rmat = random_triangular_int_matrix(5,4,False)
        affiche_matrix(rmat)
        G = open_digraph.graph_from_adjacency_matrix(rmat)
        affiche_matrix(G.adjacency_matrix())

        print("exo 8 et 10 :")
        x = ["free", "DAG", "oriented", "loop-free", "undirected", "loop-free undirected"]

        for i in range(len(x)) :
            print(f'graph {x[i]} : ')
            print('La matrice générée aléatoirement :')
            G = open_digraph.random(4,2,2,1,x[i])
            print('La matrice trouvée à partir du graphe :')
            affiche_matrix(G.adjacency_matrix())
            G.assert_is_well_formed()


    def test_connected_components(self):
        #GRAPH GO sans composantes connexe (1)
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1, 1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        #G0.save_as_dot_file(os.getcwd(), 'graphG0')
        #G0.display()
        G0C = G0.connected_components()
        self.assertEqual(G0C[0],1)
        self.assertEqual(G0C[1][0],0)
        self.assertEqual(G0C[1][6],0)
        
        #GRAPH Gb sans composantes connexe (1)
        x1 = node(10, 'x1', {}, {0:1} )
        x2 = node(11, 'x2', {}, {2:1} )
        a0 = node(0, 'x3', {10:1}, {1:1, 2:1})
        a1 = node(1, 'x4', {0:1}, {4:1})
        a2 = node(2, 'x5', {0:1, 11:1}, {3:1} )
        a3 = node(3, 'x6', {2:1}, {4:1} )
        a4 = node(4, 'x7', {1:1, 3:1}, {20:1})
        x4 = node(20, 'x8', {4:1}, {})
        Gb = open_digraph([10,11],[20], [a0,a1,a2,a3,a4, x1, x2,x4] )
        #Gb.save_as_dot_file(os.getcwd(), 'graphGb')
        #Gb.display()
        GbC = Gb.connected_components()
        self.assertEqual(GbC[0],1)
        self.assertEqual(GbC[1][0],0)
        self.assertEqual(GbC[1][20],0)
        #GRAPH GC avec 2 composantes connexes (2)
        vSI=Gb.max_id()-Gb.min_id()+1 #les indices de G0 sont modifiés de +vSI
        GC = parallel(G0, Gb)
        GC.save_as_dot_file(os.getcwd(),'GC')
        GCC = GC.connected_components()
        nb=GCC[0]
        self.assertEqual(nb,2)
        self.assertEqual(GCC[1][0],1)
        self.assertEqual(GCC[1][0+vSI],0)
        
        #GRAPH Gd avec 3 composantes connexes (3)
        vSI1=G0.max_id()-G0.min_id()+1 #les indices de GC sont modifiés de +vSI1
        Gd = parallel(GC, G0)
        GdC = Gd.connected_components()
        self.assertEqual(GdC[0],3)
        self.assertEqual(GdC[1][0],2)
        self.assertEqual(GdC[1][0+vSI+vSI1],0)
        self.assertEqual(GdC[1][0+vSI1],1)
        self.assertEqual(len(Gd.connected_list()),GdC[0]) #TEST fonction connected_list()
        #On rajoute une arrête pour revenir à 2 composantes connexes
        Gd.add_edge(29,9)
        Gd.save_as_dot_file(os.getcwd(), 'graphGD', True)
        affiche_matrix(Gd.adjacency_matrix())
        self.assertEqual(Gd.connected_components()[0],2)
        #GRAPH Ge d'une composition de GO et Gb donc sans composantes connexes
        Ge= compose(Gb,G0)
        #Ge.display()
        Ge.save_as_dot_file(os.getcwd(),'graphGe', True)
        self.assertEqual(Ge.connected_components()[0],1)


class BoolCircTest (unittest.TestCase):
    def test_id(self):
        x1 = node(10, '', {}, {0:1} )
        x2 = node(11, '', {}, {2:1} )
        x3 = node(12, '', {}, {1:1} )
        a0 = node(0, '', {10:1}, {1:1, 2:1})
        a1 = node(1, '&', {0:1}, {4:1})
        a2 = node(2, '|', {0:1}, {3:1} )
        a3 = node(3, '~', {2:1}, {4:1} )
        a4 = node(4, '|', {1:1, 3:1}, {20:1})
        x4 = node(20, '', {4:1}, {})
        
        Ga = open_digraph([10,11,12],[20], [a0,a1,a2,a3,a4, x1, x2, x3, x4] )

        GCa = bool_circ(Ga)
        self.assertEqual(0, GCa.min_id())
        self.assertEqual(20, GCa.max_id())
        GCa.shift_indices(10)
        self.assertEqual(10, GCa.min_id())
        self.assertEqual(30, GCa.max_id())
        GCa.shift_indices(-5)
        self.assertEqual(5, GCa.min_id())
        self.assertEqual(25, GCa.max_id())

        
if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run