from graphviz import Source
import sys

if __name__ == '__main__' : 

    if len(sys.argv) != 3 : 
        sys.exit('Please give exactly one input file to the commande.')
    if sys.argv[1].split(".")[-1] != 'dot' : 
        sys.exit('Please give a file with .dot extension')

    path = sys.argv[1]

    s = Source.from_file(path)
    s.render(directory = sys.argv[2])
