from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
import re
import matplotlib, matplotlib.pyplot as plt
from utils import levenshtein
from utils import memoize
from utils import get_cookie_info,get_tracker_info
from time import time

def colorizer_factory(n,colorset=plt.cm.Set2):
    from_list = matplotlib.colors.LinearSegmentedColormap.from_list
    cm = from_list('blabla', colorset(range(0,n+1)), n+1)
    return lambda x: matplotlib.colors.to_hex(cm(x))

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
    values = graphmap_inter["value"]

    unique_profiles=list(set([dom+"("+prf+")" for dom,prf in zip(domains,profiletypes)]))
    #get edge colors unique for each profiletype
    n = len(unique_profiles)
    colorizer=colorizer_factory(n)


    map_profile_toint={key:val for key, val in zip(unique_profiles,range(n))}
    value_mapper={source:{} for source in list(set(sources))}
    for key,_ in value_mapper.items():
        for src,dom,prf,value in zip(sources,domains,profiletypes,values):
            if src==key:
                dom_annotated=dom+"("+prf+")"
                if not value:
                    value=""
                value_mapper[key][dom_annotated]=value

    edge_data = zip(sources, targets, weights,profiletypes,domains,values)


    net = Network(height="750px", width="100%", bgcolor="#011936", font_color="white",directed=True)

    for i,e in enumerate(edge_data):
        src = e[0]
        dst = e[1]
        w = e[2]
        prf = e[3]
        dom = e[4]
        val = e[5]
        dom_annotated=dom+"("+prf+")"
        if src==dom:
            src=dom_annotated
        if levenshtein(dst,dom)/(max(len(dst),len(dom)))<0.2:
            dst=dom_annotated
        if src==dst and src!=dom:
            c="green"
        elif src!=dst:
            c=colorizer(map_profile_toint[dom_annotated])

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
    cookie_informer=memoize(get_cookie_info)
    tracker_informer=memoize(get_tracker_info)

    # add neighbor data to node hover data
    for i,node in enumerate(net.nodes):
        perc_complete=round(i/len(net.nodes)*100)
        if round(time())%10==0:
            print("\r","processed: ",perc_complete,"%")
        if node["id"] in value_mapper.keys():
            unique_hashes=list(set([val for _,val in value_mapper[node["id"]].items()]))
            colorizer_hash=colorizer_factory(len(unique_hashes),plt.cm.Set1)
            map_hash_toint={key:val for key, val in zip(unique_hashes,range(len(unique_hashes)))}
            if len(unique_hashes)>1:
                node["color"]="#ABFF4F"
            values=["<font color='%s'>"%(colorizer(map_profile_toint[key]))+key+"</font>"+":>"+\
            "<font color='%s'>"%(colorizer_hash(map_hash_toint[val]))+val+"</font>" for key,val in value_mapper[node["id"]].items()]
            node["title"] += "<br>Values:<br>"+ "<br>".join(values)
        neighbors=neighbor_map[node["id"]]
        colored_neighbors=[]
        for neighbor in neighbors:
            if neighbor in unique_profiles or node["id"] in unique_profiles:
                if neighbor in unique_profiles:
                    colored_neighbors.append("<font color='%s'>"%(colorizer(map_profile_toint[neighbor]))+neighbor+"</font>")
                else:
                    colored_neighbors.append("<font color='%s'>"%(colorizer(map_profile_toint[node["id"]]))+neighbor+"</font>")
            else:
                colored_neighbors.append("<font color='#7A6C5D'>"+neighbor+"</font>")
        neighbor_map[node["id"]]=colored_neighbors
        node["title"] += "<br>Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

        ######### cookie meta
        cookie_meta=cookie_informer(node["id"])
        if any(cookie_meta):
            description ="<br>description" +"<br>"+"¯"*10+"<br>"+ "<br>".join(cookie_meta[0].split("."))
            purpose = "<br>purpose"+"<br>"+"¯"*7+"<br>"+ "<br>".join(cookie_meta[1].split("."))
            node["title"] += "<br>"+"-"*len(max(description,purpose))
            node["title"] += description
            node["title"] += purpose

        ########## tracker meta
        tracker_meta=tracker_informer(node["id"][1:])
        if tracker_meta:
            description ="<br>description" +"<br>"+"¯"*10+"<br>"+ "<br>".join(tracker_meta.split("."))
            node["title"] += "<br>"+"-"*len(max(description))
            node["title"] += description


    net.show_buttons()
    net.show("c:/workspace/msc/cookie_visualizer/cookiesvis.html")
    return net
