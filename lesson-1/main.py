import graphLoad as gl
import connectivity as cn
import createGraphs as cg
import visualize as vis
import get_graph


if __name__ == "__main__":
    ###CREATE GRAPHS DEMO###
    # G_un = cg.create_undirected_graph()
    # G_di = cg.create_directed_graph()
    # G_w = cg.created_weighted_graph()
    # G_attr = cg.create_graph_with_edge_attributes()
    # G_multi = cg.create_multigraph()
    # cg.edge_node_attributes(G_attr)
    # B = cg.create_bipartite_graph()
    # P, P2, P3 = cg.create_projection(B)
    # vis.draw_graph(P3)


    G = gl.load_karate_club()
    # cn.clus_coef_v1(G, True)
    # cn.clus_coef_v2(G)
    # cn.create_tree(G)
    # print (cn.find_shortest_path(G))
    # cn.find_avg_distance(G)
    # cn.find_diameter(G)
    # cn.find_eccentricity(G)
    # cn.find_periphery(G)
    # cn.find_central(G)
    # cn.find_radius(G)
    # print (len(cn.find_central(G)))
    # cn.get_smallest_number_of_nodes_to_disconnect(G)
    # cn.get_edges_to_remove_to_disconnect(G)
    # vis.draw_graph(G)
