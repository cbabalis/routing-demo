""" This is the demo to be run.
"""


# imports here
import pandas as pd
import json
import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'osm_project/src')))
import network_operations as net_ops
import network_scenarios as net_scens
import pdb

# methods here
def create_pois_df(POIs_fpath):
    """Method to create a dataframe containing points of interest.

    Args:
        POIs_fpath (str): path where the data is found.
    """
    # list with coordinates of points of interest
    coords_list = []
    POIs = pd.read_json(POIs_fpath)
    # get a random (the first) coordinates pair from the complex dictionary.
    # following is hardcoded but also the only way to get it.
    pois_list = POIs['features']
    for coord in pois_list:
        coords = coord['geometry']['coordinates']
        coords_list.append(coords)
    point_coords_list = []
    get_single_point_from_coords_list(coords_list, point_coords_list)
    return point_coords_list


def get_single_point_from_coords_list(coords_list, point_coords_list, polygon=False):
    """Method to examine a list of points/polygons coords and to return
    a single point for each point/polygon.
    
    If the list contains a point, then return it.
    If list contains a list of coordinates, then get the first one and
    return it.

    Args:
        coords_list (list): List of coordinate lists or lists of lists.
    """
    # Algorithm explanation:
    # If list contains only a set of coordinates, then the length of the list should be 2.
    # So save the point and exit.
    # If list contains more coordinates (hence it's a polygon) then set polygon=True
    # and make a recursion call until the first point is met. If it is AND it is a polygon,
    # then just break and exit the recursion.
    # break is necessary for the recursion to work.
    for coord in coords_list:
        if len(coord) == 2:
            point_coords_list.append(tuple(coord))
            if polygon == True:
                break
        else:
            get_single_point_from_coords_list(coord, point_coords_list, polygon=True)


def assign_points_to_nodes(point_coords_list, graph):
    """Method to assign points of interest to nodes.
    In order to assign points to nodes the coordinates are used.
    For each point the node nearest to it (according to the coordinates) is found.

    Args:
        point_coords_list (list): List of coordinates (points coordinates)
        graph (graph object): graph representation of the network.
    """
    del point_coords_list[0]
    X, Y = zip(*point_coords_list)
    nearest_node_id_list = ox.distance.get_nearest_nodes(graph, X, Y)
    return nearest_node_id_list.tolist()


def update_graph_nodes_with_POIs(nodes, assigned_nodes_list, new_col='supermarket'):
    """Method to update the nodes df with new fields and nodes.

    Args:
        nodes (dataframe): pandas dataframe that represents the nodes of
        the network.
        assigned_nodes_list (list): list of network nodes nearest to the
        points of interest.
    """
    nodes[new_col] = False
    for node in assigned_nodes_list:
        nodes.loc[nodes['osmid'] == node, new_col] = True


def plot_graph_and_points(graph, points_list):
    fig, ax = ox.plot_graph(graph, show=False, close=False)
    for point_coords in points_list:
        point_a, point_b = point_coords
        ax.scatter(point_a, point_b, c='red')
        plt.show()


def main():
    # declare all variables (may be input vars later)
    POIs_fpath = 'data/attica-supermarket.geojson'
    graph_fpath = 'data/attica_graph.graphml'
    algorithm = ''
    # read points of interest (data)
    point_coords_list = create_pois_df(POIs_fpath)
    graph = net_ops.load_graph_from_disk(graph_fpath)
    assigned_nodes_list = assign_points_to_nodes(point_coords_list, graph)
    nodes, edges = net_ops.get_nodes_edges(graph)
    update_graph_nodes_with_POIs(nodes, assign_nodes_list)
    pdb.set_trace()
    # read/download network of interest
    # merge network to point of interest
    # run algorithms to network
    # visualize the results

# call it

if __name__ == '__main__':
    main()

