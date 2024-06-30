import networkx as nx
from pyvis.network import Network

file_path = "./example.txt"

try:
    with open(file_path, "r") as file:
        file_contents = file.read()
except FileNotFoundError:
    print("File not found.")
except IOError:
    print("Error reading the file.")

edges = []

temp = False
for i in file_contents.split('\n'):
    if (';' in i) and not temp:
        A = i.split(';')[0]
        B = i.split(';')[1]
        
        print(A[:-1], B[1:])
        
        A = A[:-1]
        B = B[1:]
        
        edges.append([A, B])
        temp = True
        continue
        
    if temp:
        last = edges[-1]
        
        edges = edges[:-1]
                
        edges.append([last[0], last[1], i])
        
        temp = False
        
        
# Create a networkx graph
G = nx.Graph()

# Add nodes and edges from input list
for connection in edges:
    person1, person2, edge_info = connection
    G.add_node(person1, label=person1)
    G.add_node(person2, label=person2)
    # G.add_edge(person1, person2, label=f'Edge Summary', title=edge_info)
    G.add_edge(person1, person2, label=f'', title=edge_info)

# Initialize Pyvis network with notebook mode turned on
nt = Network(notebook=True)

# Add networkx graph to pyvis network
nt.from_nx(G)

# Generate and show the network graph
nt.show('test_net.html')