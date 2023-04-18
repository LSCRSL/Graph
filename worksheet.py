from modules.open_digraph import *
from modules.bool_circ import *
import inspect 

#%% TP1 tests
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

#G1.display()

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
# %% TP5 tests
try:
    GC = bool_circ(G1)
    print(GC.is_cyclic())
    print(GC.is_well_formed())
except:
    print("Erreur levée comme prévu")

x1 = node(10, '', {}, {0:1} )
x2 = node(11, '', {}, {2:1} )
x3 = node(12, '0', {}, {1:1} )
a0 = node(0, '', {10:1}, {1:1, 2:1})
a1 = node(1, '&', {0:1, 12:1}, {4:1})
a2 = node(2, '|', {0:1, 11:1}, {3:1} )
a3 = node(3, '~', {2:1}, {4:1} )
a4 = node(4, '|', {1:1, 3:1}, {20:1})
x4 = node(20, '', {4:1}, {})
    
Ga = open_digraph([10,11,12],[20], [a0,a1,a2,a3,a4, x1, x2, x3, x4] )

GCa = bool_circ(Ga)
print(GCa.is_well_formed())

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

print("\nID de base:")
GCa = bool_circ(Ga)
print(GCa.min_id())
print(GCa.max_id())
print(GCa.get_node_ids())
print(GCa.get_input_ids())
print(GCa.get_output_ids())
print(str(GCa))

print("\nID +10:")
GCa.shift_indices(10)
print(GCa.min_id())
print(GCa.max_id())
print(GCa.get_node_ids())
print(GCa.get_input_ids())
print(GCa.get_output_ids())
print(str(GCa))
print("\nID -5:")
GCa.shift_indices(-5)
print(GCa.min_id())
print(GCa.max_id())
print(GCa.get_node_ids())
print(GCa.get_input_ids())
print(GCa.get_output_ids())

n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
n1 = node(1, 'b', {0:1}, {2:2, 5:1})
n2 = node(2, 'c', {0:1, 1:2}, {6:1})
i0 = node(3, 'i0', {}, {0:1})
i1 = node(4, 'i1', {}, {0:1})
o0 = node(5, 'o0', {1:1}, {})
o1 = node(6, 'o1', {2:1}, {})
G0 = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])

x1 = node(10, 'x1', {}, {0:1} )
x2 = node(11, 'x2', {}, {2:1} )
a0 = node(0, 'x3', {10:1}, {1:1, 2:1})
a1 = node(1, 'x4', {0:1}, {4:1})
a2 = node(2, 'x5', {0:1, 11:1}, {3:1} )
a3 = node(3, 'x6', {2:1}, {4:1} )
a4 = node(4, 'x7', {1:1, 3:1}, {20:1})
x4 = node(20, 'x8', {4:1}, {})
    
Gb = open_digraph([10,11],[20], [a0,a1,a2,a3,a4, x1, x2,x4] )

GC = open_digraph.parallel(G0, Gb)
Gd = open_digraph.parallel(GC, G0)
#Gd.display("G1",True)
Gd.add_edge(9,29)
#Gd.display("G2",True)
Graph_list=Gd.connected_list()
print(len(Graph_list))
for i in range (len(Graph_list)):
    g=Graph_list[i]
    #g.display("Gd"+str(i), True)
'''G0.display('G01')
GCC = compose(Gb, G0)
Gb.display('Gb')
G0.display('G0')
GCC.display()'''
#GT = open_digraph.identity(4)
'''
GC.save_as_dot_file(os.getcwd())
GCC.save_as_dot_file(os.getcwd())
GT.save_as_dot_file(os.getcwd())
'''

# %% TP7 TESTS DIJKSTRA

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
G.add_edge(2,5)

print("\n\nAlgo Dijkstra à partir de 'a' quand direction=1, ie les enfants:\n")
print(G.dijkstra(n0,1))
print("\n\nAlgo Dijkstra à partir de 'b' quand direction=-1, ie les parents:\n")
print(G.dijkstra(n1,-1))
print("\n\nAlgo Dijkstra à partir de 'o0' quand direction=None, ie les parents et les enfants:\n")
print(G.dijkstra(o0,None))
print("\n\nAlgo Dijkstra à partir de 'a' quand direction=1, dès qu'on est sûr que c'est le plus court chemin pour aller à 'b':\n")
print(G.dijkstra(n0,1,n1))
print("\n\nChemin le plus court pour aller de 'a' à 'o0':\n")
print(G.shortest_path(n0,o0))
print("Distance avec ancetre : \n")
print(G.dist_ancetre(o0,o1))

x1 = node(10, 'x1', {}, {0:1} )
x2 = node(11, 'x2', {}, {2:1} )
a0 = node(0, 'x3', {10:1}, {1:1, 2:1})
a1 = node(1, 'x4', {0:1}, {4:1})
a2 = node(2, 'x5', {0:1, 11:1}, {3:1} )
a3 = node(3, 'x6', {2:1}, {4:1} )
a4 = node(4, 'x7', {1:1, 3:1}, {20:1})
x4 = node(20, 'x8', {4:1}, {})
Gb = open_digraph([10,11],[20], [a0,a1,a2,a3,a4, x1, x2,x4] )
GC = open_digraph.parallel(G, Gb)

print("\nChemin le plus court pour aller de 'a' à 'o0':")
print(GC.shortest_path(GC.get_node_by_id(21),GC.get_node_by_id(26)))
print("\nChemin le plus court pour aller de 'x5' à 'x4':")
print(GC.shortest_path(GC.get_node_by_id(2),GC.get_node_by_id(1)))
print("\nChemin le plus court pour aller de 'x2' à 'x7':")
print(GC.shortest_path(GC.get_node_by_id(11),GC.get_node_by_id(4)))
print("\nChemin le plus court pour aller de 'x2' à 'b':")
print(GC.shortest_path(GC.get_node_by_id(11),GC.get_node_by_id(22)))
print("\nDistance avec ancetre : \n")
print(GC.dist_ancetre(GC.get_node_by_id(26),GC.get_node_by_id(27)))
print("\nDistance avec ancetre de 2 noeuds qui ne sont pas dans la même composante : ")
print(GC.dist_ancetre(GC.get_node_by_id(20),GC.get_node_by_id(27)))

#%% TP8 TESTS

ai=node(21,'iO',{},{0:1})
ci=node(20,'i2',{},{2:1})
a=node(0,'0',{21:1},{3:1})
b=node(1,'1', {},{5:1,8:1,4:1})
c=node(2,'2',{20:1},{4:1})
d=node(3,'3',{0:1},{7:1,5:1,6:1})
e=node(4,'4',{1:1,2:1},{6:1})
f=node(5,'5',{3:1,1:1},{7:1})
g=node(6,'6',{3:1,4:1},{8:1,9:1})
h=node(7,'7',{3:1,5:1},{10:1})
i=node(8,'8',{1:1,6:1},{})
j=node(9,'9',{6:1},{})
k=node(10,'10',{7:1},{})
    
G8 = open_digraph([21,20],[10], [ai,ci,a,b,c,d,e,f,g,h,i,j,k] )
'''
#G8.fusion()
G8.display('G8')

print(G8.profondeur(5))

print(G8.plusLongChemin(0,5))

G8.fusion(0,2)
G8.fusion(0,3, True)
G8.fusion(6,7)
G8.display('G8après')

'''

s3="((x0)&(x1)&(x2))|((x1)&(~(x2)))"
#G9encore, inputs3 = bool_circ.formule_arbre(s3)
#G9encore.display('G9encore')

#%% TP10
#G10=bool_circ.random(5,3,1)
g = bool_circ.adder(2)
g1 = bool_circ.half_adder(0)
#g.display("G10",True)
#%%TP11
g2 = bool_circ.registre(11,8)
#g2.display("TP11", False)

a = node(0, "1", {}, {1:1})
b = node(1 , "|", {0:1,2:1,3:1}, {4:1})
c = node(2, " 1", {}, {1:1})
d = node(3, " 1", {}, {1:1})
e = node(4, " ", {1:1}, {})
g = open_digraph([],[], [a,b,c,d,e])
g2 = bool_circ(g)

'''
g2.display("avant")
g2.porte_OU(0,1)
g2.evaluate()
g2.display("apres")

#%%TP11 evaluate
a = node(0, "0", {}, {1:1})
b = node(1 , "|", {0:1,2:1,3:1}, {4:1})
c = node(2, "0", {}, {1:1})
d = node(3, "0", {}, {1:1})
e = node(4, "", {1:1}, {})
g = open_digraph([],[], [a,b,c,d,e])
Geval= bool_circ(g)
Geval.display('G_av_eval')
Geval.evaluate()
Geval.display("GG_ap_eval1")
'''
#g = calcul(2,2,2)
#g.display("ADD")


#%% TP12 TESTS encodeur et decodeur
encodeur=bool_circ.encodeur()
#encodeur.display('encodeur') #testé
decodeur=bool_circ.decodeur()
#decodeur.display("decodeur", True) #testé


#%% TP12 TESTS règles de réécriture
i1=node(0,'1',{},{5:1})
i2=node(1,'0',{},{5:1})
i3=node(2,'0',{},{6:1})
i4=node(3,'1',{},{6:1})
a=node(5,'^',{0:1,1:1},{6:1})
b=node(6, '^', {5:1,2:1,3:1},{7:1})
o1=node(7,'',{6:1},{})
baxor=bool_circ(open_digraph([0,1,2,3],[7],[i1,i2,i3,i4,a,b,o1]))
#baxor.display("avant_asso_XOR")
baxor.asso_xor(5,6)
#baxor.display("apres_asso_XOR") #test ok

i1=node(0,'1',{},{1:1})
a=node(1,'',{0:1},{2:1,3:1,4:1})
b=node(2,'',{1:1},{5:1,6:1})
o1=node(3,'',{1:1},{})
o2=node(4,'',{1:1},{})
o3=node(5,'',{2:1},{})
o4=node(6,'',{2:1},{})
bac=bool_circ(open_digraph([0],[3,4,5,6],[i1,a,b,o1,o2,o3,o4]))
#bac.display("av_asso_copie")
bac.asso_copie(1,2)
#bac.display("ap_asso_copie") #test ok

i1=node(0,'1',{},{5:1})
i2=node(1,'0',{},{5:1})
i3=node(2,'0',{},{6:1})
a=node(5,'^',{0:1,1:1,6:2},{7:1})
b=node(6, '', {2:1},{5:2,8:1,9:1})
o1=node(7,'',{5:1},{})
o2=node(8,'',{6:1},{})
o3=node(9,'',{6:1},{})
binvol=bool_circ(open_digraph([0,1,2],[7,8,9],[i1,i2,i3,a,b,o1,o2,o3]))
#binvol.display("av_invol")
binvol.invol_xor(5,6)
#binvol.display("ap_invol")  #test ok

i1=node(0,'1',{},{5:1})
i2=node(1,'0',{},{5:1})
i3=node(2,'0',{},{5:1})
a=node(5,'^',{0:1,1:1,2:1},{7:1})
o1=node(7,'',{5:1},{})
eff=bool_circ(open_digraph([0,1,2],[7],[i1,i2,i3,a,o1]))
#eff.display("av_eff",True)
eff.effacement(5,7)
#eff.display("ap_eff", True)  #test ok

i1=node(0,'1',{},{5:1})
i2=node(1,'0',{},{5:1})
i3=node(2,'0',{},{5:1})
i4 =node(3,'1',{},{6:1})
a=node(5,'^',{0:1,1:1,2:1,6:1},{7:1})
b=node(6, '~', {3:1},{5:1})
o1=node(7,'',{5:1},{})
nxor=bool_circ(open_digraph([0,1,2,3],[7],[i1,i2,i3,i4,a,b,o1]))
#nxor.display("av_xor",True)
nxor.non_xor(6,5)
#nxor.display("ap_xor",True)  #test ok

i1=node(0,'1',{7:1},{})
i2=node(1,'0',{7:1},{})
i3=node(2,'0',{7:1},{})
i4 =node(3,'1',{},{6:1})
b=node(6, '~', {3:1},{7:1})
o1=node(7,'',{6:1},{0:1,1:1,2:1})
ncop=bool_circ(open_digraph([3],[0,1,2],[i1,i2,i3,i4,b,o1]))
#ncop.display("av_cop",True)
ncop.non_copie(6,7)
#ncop.display("ap_cop",True)  #test ok

i1=node(0,' ',{7:1},{})
i2=node(1,' ',{},{6:1})
b=node(6, '~', {1:1},{7:1})
o1=node(7,'~',{6:1},{0:1})
ninv=bool_circ(open_digraph([1],[0],[i1,i2,b,o1]))
ninv.display("av_ninv",True)
ninv.invol_non(6,7)
ninv.display("ap_ninv",True)  #test ok

g = bool_circ(open_digraph.compose(decodeur,encodeur))
g.display("edec")
g.eval()
g.display("enc-dec")



