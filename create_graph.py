import os
import json
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import rcParams
import matplotlib.font_manager as fm
from matplotlib import rc

font_path = "assets/NanumSquareR.ttf"
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()

plt.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False

with open('results/person_relation_result/person_40_roberta.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

os.makedirs('results/graph_result', exist_ok=True)

for part_num in range(1, 4):  # part
    G = nx.DiGraph()
    part_relations = [relation for relation in data['relations'] if relation['part'] == part_num]

    for relation in part_relations:
        source = relation['node']
        target = relation['target']
        label = relation['edge']
        G.add_node(source)
        G.add_node(target)
        G.add_edge(source, target, label=label)

    pos = nx.spring_layout(G, k=0.5, iterations=50)

    def wrap_label(text, width=15):
        import textwrap
        return "\n".join(textwrap.wrap(text, width))

    edge_labels = nx.get_edge_attributes(G, 'label')
    wrapped_edge_labels = {key: wrap_label(value) for key, value in edge_labels.items()}


    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
            node_size=2000, font_size=10, font_family=font_name)

    edge_label_pos = {}
    for edge, (x, y) in pos.items():
        edge_label_pos[edge] = (x + 0.05, y + 0.05)  # 각 엣지에 대해 위치 약간 조정

    nx.draw_networkx_edge_labels(G, pos=edge_label_pos, edge_labels=wrapped_edge_labels, font_size=8, font_family=font_name)


    plt.title(f"등장인물 간 관계 그래프 (Part {part_num})")
    plt.axis('off')
    plt.savefig(f"results/graph_result/person_relation_graph_part_{part_num}.png", dpi=300, bbox_inches='tight')
    plt.close()  # 메모리