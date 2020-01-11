from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
import re


def visualize_tohtml_globalmap(graphmap_inter):
    sources = graphmap_inter['source']
    targets = graphmap_inter['target']
    weights = graphmap_inter['weight']
    colours = graphmap_inter['color']


    edge_data = zip(sources, targets, weights,colours)


    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]
        c = e[3]

        net.add_node(src, src, title=src)
        net.add_node(dst, dst, title=dst,color=c)
        net.add_edge(src,dst, value=0.1)

    neighbor_map = net.get_adj_list()

    # add neighbor data to node hover data
    for node in net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    net.show_buttons()
    net.show("c:/workspace/msc/cookie_visualizer/cookiesvis.html")
    return net

def visualize_tohtml_audit(graphmap_inter):
    sources = graphmap_inter['source']
    targets = graphmap_inter['target']
    weights = graphmap_inter['weight']
    profiletypes = graphmap_inter['profile_type']
    domains = graphmap_inter['domain']

    edge_data = zip(sources, targets, weights,profiletypes,domains)


    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white",directed=True)

    for i,e in enumerate(edge_data):
        src = e[0]
        dst = e[1]
        w = e[2]
        prf = e[3]
        dom = e[4]
        dom_annotated=dom+"("+prf+")"
        if dst==dom:
            dst=dom_annotated
        if src==dst:
            c="green"
        elif src!=dst:
            c="red"
        net.add_node(dom_annotated, dom_annotated, title="<font size='4'>%s</font>"%(src),color="blue")
        #make distinct nodes per audit profile
        net.add_node(dst, dst, title=dst)
        net.add_edge(dom_annotated, dst, value=0.1,color=c)

    neighbor_map = net.get_adj_list()

    # add neighbor data to node hover data
    for node in net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    net.show_buttons()
    net.show("c:/workspace/msc/cookie_visualizer/cookiesvis.html")
    return net
