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

G.save_as_dot_file(os.getcwd(), True)

#%% TP1 tests
print(str(G))
H = open_digraph.empty()
print(str(H))
G.assert_is_well_formed()

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
# %% TP4 display

def display(self, verbose=False):
    G.save_as_dot_file(os.getcwd(), verbose)
    convert='dot -Tpdf graph.dot -o graph.pdf'
    open_file='xdg-open graph.pdf'
    os.system(convert)
    os.system(open_file)
    
    