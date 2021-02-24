""" This is the demo to be run.
"""


# imports here
import pandas as pd
import json
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
    points_list = []
    get_single_point_from_coords_list(coords_list, points_list)
    return points_list


def get_single_point_from_coords_list(coords_list, points_list, polygon=False):
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
            points_list.append(coord)
            if polygon == True:
                break
        else:
            get_single_point_from_coords_list(coord, points_list, polygon=True)


def assign_points_to_nodes(points_list, nodes):
    """Method to assign points of interest to nodes.
    In order to assign points to nodes the coordinates are used.
    For each point the node nearest to it (according to the coordinates) is found.

    Args:
        points_list (list): List of coordinates (points coordinates)
        nodes (Dataframe): dataframe of nodes.
    """
    pass


def main():
    # declare all variables (may be input vars later)
    POIs_fpath = 'data/butchershops-attiki.geojson'
    graph_fpath = ''
    algorithm = ''
    # read points of interest (data)
    create_pois_df(POIs_fpath)
    pdb.set_trace()
    # read/download network of interest
    # merge network to point of interest
    # run algorithms to network
    # visualize the results

# call it

if __name__ == '__main__':
    main()

