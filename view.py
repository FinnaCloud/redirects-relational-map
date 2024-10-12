import json
import networkx as nx
import matplotlib.pyplot as plt
import whois


def load_redirects_map(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def create_graph(redirects_map):
    G = nx.DiGraph()
    for redirect in redirects_map:
        url = redirect['url']
        status_code = redirect['status_code']
        whois_info = redirect['whois']
        provider = whois_info.get('provider', 'Unknown')
        if provider == 'Unknown': #let's try again, incase we can get the provider
            whois_result = whois.whois(url)
            provider = whois_result.registrar or whois_result.org or whois_result.name or "Unknown"

        dig_result = whois_info.get('dig_result', ['Unknown'])[0]

        G.add_node(url, status_code=status_code, provider=provider, dig_result=dig_result)

        if len(G.nodes) > 1:
            previous_url = list(G.nodes)[-2]
            G.add_edge(previous_url, url, status_code=status_code)

    return G


def draw_graph(G):
    pos = nx.spring_layout(G)
    labels = {node: f"{node}\n{G.nodes[node]['provider']}\n{G.nodes[node]['dig_result']}" for node in G.nodes}
    edge_labels = {(u, v): G.edges[u, v]['status_code'] for u, v in G.edges}

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=8,
            font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Redirects Relational Map')
    plt.show()


def main():
    file_path = 'redirects_map.json'
    redirects_map = load_redirects_map(file_path)
    G = create_graph(redirects_map)
    draw_graph(G)


if __name__ == "__main__":
    main()