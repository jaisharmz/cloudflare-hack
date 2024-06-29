import networkx as nx
from pyvis.network import Network
import json

def get_graph_html(author_name, ID):

    graph_file = f'./{author_name}_graph_data.json'
    id_file = f'./{author_name}_id_data.json'
    save_file = author_name + '_network.html'

    # Load the JSON data from a file
    with open(graph_file) as f:
        adjacency_list = json.load(f)

    with open(id_file) as f:
        info_list = json.load(f)

    # Create a NetworkX graph from the adjacency list
    G = nx.Graph()
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Create a Pyvis network
    net = Network(notebook=True)

    # Add nodes and edges to the Pyvis network, including URLs for each node
    for node in G.nodes():
        if node == ID:
            net.add_node(
                node,
                label=info_list[node]['name'],
                title=f"Affiliation: {info_list[node]['affiliation']}",
                url=f"https://scholar.google.com/citations?user={node}",
                shape="diamond",
                size=info_list[node].get('size', 50),
                image=f'https://scholar.googleusercontent.com/citations?view_op=small_photo&user={node}',
                broken_image='https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'
            )
        else:
            net.add_node(
                node,
                label=info_list[node]['name'],
                title=f"Affiliation: {info_list[node]['affiliation']}",
                url=f"https://scholar.google.com/citations?user={node}",
                shape="circularImage",
                image=f'https://scholar.googleusercontent.com/citations?view_op=small_photo&user={node}',
                broken_image='https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'
            )

    # Add edges
    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    # Customize options for interaction
    net.set_options("""
    var options = {
    "nodes": {
        "shape": "circularImage",
        "brokenImage": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png",
        "size": 30,
        "borderWidth": 2
    },
    "interaction": {
        "hover": true,
        "clickToUse": true
    },
    "physics": {
        "enabled": true
    }
    }
    """)

    # Generate and show the interactive visualization
    net.show(save_file)

    # Manually add JavaScript to handle click events for nodes
    with open(save_file, "r") as file:
        data = file.readlines()

    # Find the line to insert the JavaScript for click event
    for i, line in enumerate(data):
        if "network = new vis.Network(container, data, options);" in line:
            break

    # JavaScript to handle click events
    js_code = """
    network.on("click", function (params) {
        params.event = "[original event]";
        var nodeId = params.nodes[0];
        if (nodeId) {
            var node = network.body.data.nodes.get(nodeId);
            if (node.url) {
                window.open(node.url, "_blank");
            }
        }
    });
    """

    # Insert the JavaScript code after the line found
    data.insert(i + 1, js_code)

    # Write the modified content back to the HTML file
    with open(save_file, "w") as file:
        file.writelines(data)
        
        
if __name__ == '__main__':
    author_name = 'Ilya Sutskever'
    get_graph_html(author_name, 'x04W_mMAAAAJ')