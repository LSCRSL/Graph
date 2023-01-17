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
        n2 = node(2, 'c', {0:1, 1:2}, {6:1})
        i0 = node(3, 'i0', {}, {0:1})
        i1 = node(4, 'i1', {}, {0:1})
        o0 = node(5, 'o0', {1:1}, {})
        o1 = node(6, 'o1', {2:1}, {})
        G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
        self.assertIsNot(G.copy(),G)
    
        
if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run