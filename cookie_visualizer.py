from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
import re
import matplotlib, matplotlib.pyplot as plt



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

    unique_profiles=list(set(profiletypes))
    #get edge colors unique for each profiletype
    n = len(unique_profiles)
    from_list = matplotlib.colors.LinearSegmentedColormap.from_list
    cm = from_list('Set15', plt.cm.Set2(range(0,n)), n)

    map_profile_toint={key:val for key, val in zip(unique_profiles,range(n))}

    edge_data = zip(sources, targets, weights,profiletypes,domains)


    net = Network(height="750px", width="100%", bgcolor="#011936", font_color="white",directed=True)

    for i,e in enumerate(edge_data):
        src = e[0]
        dst = e[1]
        w = e[2]
        prf = e[3]
        dom = e[4]
        dom_annotated=dom+"("+prf+")"
        if src==dom:
            src=dom_annotated
        if dst==dom:
            dst=dom_annotated
        if src==dst and src!=dom:
            c="green"
        elif src!=dst:
            c=matplotlib.colors.to_hex(cm(map_profile_toint[prf]))

        if src==dom_annotated:
            net.add_node(dom_annotated, dom_annotated, title="<font size='4'>%s</font>"%(src),color="#F9DC5C",size=3,physics=False)
            net.add_node(dst, dst, title=dst)
            net.add_edge(dom_annotated, dst, value=w,color=c)
        elif dst==dom_annotated:
            net.add_node(src, src, title="<font size='4'>%s</font>"%(src),color="#F9DC5C",size=3,physics=False)
            net.add_node(dom_annotated, dom_annotated, title=dst)
            net.add_edge(src, dom_annotated, value=w,color=c)
        else:
            net.add_node(src, src, title="<font size='4'>%s</font>"%(src),physics=False)
            net.add_node(dst, dst, title=dst,color="#D81159",physics=False)
            net.add_edge(src, dst, value=w,color="#7A6C5D")

    net.force_atlas_2based(gravity=-161,spring_length=100,damping=0.27,overlap=1)


    neighbor_map = net.get_adj_list()

    # add neighbor data to node hover data
    for node in net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    net.show_buttons()
    net.show("c:/workspace/msc/cookie_visualizer/cookiesvis.html")
    return net
