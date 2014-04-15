import cPickle as pkl
import networkx as nx


def pickle_tree( tree, fname ):
        """
        Extact necessary information to create a persistent object.

	fname : full path where you'd like to save the tree

	tree : a Tree object
        """
        b = tree.boxes()
        tree_dict = { 'corners' : b.corners,
                      'width' : b.width,
                      'dim' : b.dim,
                      'size' : b.size
                      }
        with open( fname, 'wb' ) as fh:
            pkl.dump( tree_dict, fh )

def write_dot( graph, fname ):
    """
    Just wraps NX's version.
    """
    nx.write_dot( graph, fname )
