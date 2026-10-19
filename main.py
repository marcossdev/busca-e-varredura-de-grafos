import os
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

adj_dict = {
    "A": ["G"],
    "B": ["F", "K"],
    "C": ["F", "J", "D", "L"],
    "D": ["C", "J"],
    "E": ["G", "J", "K", "L"],
    "F": ["B", "C", "K", "H", "I"],
    "G": ["A", "E", "K", "L"],
    "H": ["F", "K"],
    "I": ["F"],
    "J": ["C", "D", "E"],
    "K": ["B", "E", "F", "G", "H"],
    "L": ["C", "E", "G"],
}

G = nx.from_dict_of_lists(adj_dict)

# Calculo da posição do grafo na representação
G_POS = nx.spring_layout(G, seed=47)
B_SOURCE = "A"

# edges das buscas
edges_dfs = list(nx.dfs_edges(G, source=B_SOURCE))
edges_bfs = list(nx.bfs_edges(G, source=B_SOURCE))

# Função para gerar imagens de 
def gerar_representacoes(output_path: str, edges: list):
    if not Path(os.getcwd(), output_path).exists():
        Path(os.getcwd(), output_path).mkdir()

    # Definindo cores padrões dos nós
    n_colors_dict = {}
    for n in G.nodes():
        n_colors_dict[n] = "lightblue"

    # Definindo cores padrões dos enlaces
    e_colors_dict = {}
    for e in G.edges():
        e_colors_dict[e] = "gray"

    num = 0

    for edge in edges:
        # Gerar imagem inicial destacando a Fonte (Source)
        if num == 0:
            n_colors_dict[B_SOURCE] = "lightgreen"
            nx.draw(G, G_POS, node_color=n_colors_dict.values(), edge_color=e_colors_dict.values(), with_labels=True, node_size=500)
            plt.savefig(f"{output_path}/grafo_{num}.png", bbox_inches="tight", dpi=640)
            plt.close()
            num = num + 1

        # Marcar os vertices varridos nessa iteração
        n_colors_dict[edge[0]] = "lightgreen"
        n_colors_dict[edge[1]] = "lightgreen"

        # Definindo a cor de destaque dos enlaces
        if edge not in e_colors_dict:
            e_colors_dict[(edge[1], edge[0])] = "lightgreen"
        else:
            e_colors_dict[edge] = "lightgreen"

        # Obtendo as cores dos nós e enlaces
        n_colors = n_colors_dict.values()
        e_colors = e_colors_dict.values()

        # Gerando a imagem corresponde da iteração
        nx.draw(G, G_POS, node_color=n_colors, edge_color=e_colors, with_labels=True, node_size=500)
        plt.savefig(f"{output_path}/grafo_{num}.png", bbox_inches="tight", dpi=640)
        plt.close()
        num = num + 1

# Processando as buscas executadas e gerando as imagens
gerar_representacoes("bfs_graph", edges_bfs)
gerar_representacoes("dfs_graph", edges_dfs)

# Gerar imagem do grafo (normal)
nx.draw(G, G_POS, node_color="lightblue", with_labels=True, edge_color="gray", node_size=500)
plt.savefig("grafo.png", bbox_inches="tight", dpi=640)
plt.close()