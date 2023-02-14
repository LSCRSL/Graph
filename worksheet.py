from modules.open_digraph import *
import inspect 

# Déclaration et initialisation des noeuds
n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
n1 = node(1, 'b', {0:1}, {2:2, 5:1})
n2 = node(2, 'c', {0:1, 1:2}, {6:1})
i0 = node(3, 'i0', {}, {0:1})
i1 = node(4, 'i1', {}, {0:1})
o0 = node(5, 'o0', {1:1}, {})
o1 = node(6, 'o1', {2:1}, {})
# Déclaration et initialisation du graph
G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])


G.save_as_dot_file(os.getcwd())
G1 = open_digraph.from_dot_file('graph.dot')
print(str(G1))

G1.display()

#%% TP1 tests
print(str(G))
H = open_digraph.empty()
print(str(H))
G.assert_is_well_formed()
'''
# %% TP1 exercice 9
print("\nMéthodes de la classe 'node':")
print(dir(node))
print("\nMéthodes de la classe 'open_digraph':")
print(dir(G))
print("\nFichier contenant la méthode 'add_node' de 'open-digraph': *")
print(inspect.getfile(open_digraph.add_node))
print("\nDocumentation de la méthode 'add_node' de 'open-digraph': *")
print(inspect.getdoc(open_digraph.add_node))
print("\nCode source de la méthode 'add_node' de 'open-digraph': *")
print(inspect.getsource(open_digraph.add_node))
# %% TP3 tests
n0 = node(8, 'a', {3:1, 4:1}, {1:1, 2:1})
n1 = node(1, 'b', {0:1}, {2:2, 5:1})
n2 = node(6, 'c', {0:1,1:2}, {6:1})
i0 = node(3, 'i0', {}, {0:1})
i1 = node(4, 'i1', {}, {0:1})
o0 = node(5, 'o0', {1:1}, {})
o1 = node(0, 'o1', {2:1}, {})
G = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
print(G.dict_of_graph())
'''

print('ici :')
GC = bool_circ(G1)
print(GC.is_cyclic())
print(GC.is_well_formed())

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
print(GCa.is_well_formed())
