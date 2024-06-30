import networkx as nx
from pyvis.network import Network

# Create a networkx graph
G = nx.Graph()

# Add nodes
G.add_node(1, label='Node 1')
G.add_node(2, label='Node 2')

# Add an edge with a label and hover info
G.add_edge(1, 2, label='Edge from 1 to 2', title="This is an edge info, that is a longer paragraph describing the interaction between these two nodes.")

# Initialize Pyvis network with notebook mode turned on
nt = Network(notebook=True)

# Add networkx graph to pyvis network
nt.from_nx(G)

# Generate and show the network graph
nt.show('test_net.html')
