import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)

    def test_init_node2(self):
        n1 = node (1, 'f', {0:1},{})
        self.assertEqual(n1.id, 1)
        self.assertEqual(n1.label, 'f')
        self.assertEqual(n1.parents, {0:1})
        self.assertEqual(n1.children, {})
        self.assertIsInstance(n1, node)

    def test_copy_node(self):
        x = node (1, 'f', {0:1},{})
        self.assertIsNot(x.copy(),x)

    def test_copy_od(self):
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1,1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertIsNot(G.copy(),G)

    def test_get_node(self) : 
        N = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        self.assertEqual(N.id, N.get_id())
        self.assertEqual(N.label, N.get_label())
        self.assertEqual(N.parents.keys(), N.get_parent_ids())
        self.assertEqual(N.children.keys(), N.get_children_ids())

    def test_set_node(self) : 
        N = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        N.set_id(1)
        N.set_label('f')
        N.set_children_ids({5:1,6:1,7:1})
        N.set_parent_ids({0:1,2:1})
        print(N.get_id())
        print(N.get_label())
        print(N.get_children_ids())
        print(N.get_parent_ids())
        N.add_child_id(9,1)
        N.add_parents_id(3,1)
        print('Après avoir rajouté un enfant : ')
        print(N.get_children_ids())
        print('Après avoir rajouté un parent : ')
        print(N.get_parent_ids())
    
    def test_get_dig(self) : 
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
        n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
        n1 = node(1, 'b', {0:1}, {2:2, 5:1})
        n2 = node(2, 'c', {0:1,1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        print (f'Nouvel ID trouvé : {G.new_id()}')
        print('Avant avoir rajouté une arête: ')
        print(n2.get_children_ids())
        print(n1.get_children_ids())
        print(n0.get_parent_ids())
        G.add_edges([(2,0),(1,0)] )
        print('Apres avoir rajouté une arête:')
        print(n2.get_children_ids())
        print(n1.get_children_ids())
        print(n0.get_parent_ids())
        print('L ID du nouveau noeud :')
        print(G.add_node('y', {2:1},{0:2} ))
        print(n2.get_children_ids())
        print(n0.get_parent_ids())


        
if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run