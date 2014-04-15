"""
Utility function to compute the confidence of a given finite representation. This is separate from the actual FR module 
"""

import numpy as np


def confidence( mvm1, mvm2 ):
    """
    Given gamma, compute the following:

        1 - Pr( f(|G|) \subset |F(G)| ).

    Report whether this is >= gamma, the confidence that we want to
    attain.

    mvm* : a directed graph on the nodes (grid elements) of the tree.

    mvm1 is assumed to come from the 'true', or rigorous, map. 
    """
    print "mvm1: ", len(mvm1)
    print "mvm2: ", len(mvm2)
    
    # check the containment condition
    for u in mvm1:
        print "u = ", u
        # find the image, F(|u|)
        succ_true = set( mvm1.successors( u ) )
        print succ_true
        succ_approx = set( mvm2.successors( u ) )
        print succ_approx
        print ""
        


if __name__ == "__main__":

    from finite_representation import BoxTree,FiniteRepresentation
    from rads.enclosure import CombEnc,Tree
    from rads.maps.henon import HenonMapper
    from rads.graphs.algorithms import graph_mis
    from rads.misc import gfx
    import networkx as nx

    npts = 2000

    # initial compact region X, anchored at (-2.0,2), w x h = 4 x 4
    box = np.array([[-2.0,-2],[4,4]])

    print box

    # init the tree
    depth = 7 # AKA resolution, 2^{-depth/2} boxes 
    tree = BoxTree( box, depth )

    print tree

    # boxes defined by lower corner followed by width and height. So
    # np.array( [[1,2.],[1,3]] ) is anchored at (1,2), has width 1 and
    # height 3. Definition extends for higher dimensions (row 0 == anchor,
    # row 1 == size in j'th dimension).
    all_data = np.loadtxt( '../sandbox/squareNoiseHenonLong.txt' )
    data = all_data[:npts,:2]
    noise = all_data[:npts,2]
    print "Read data and noise arrays"
    # print "data", data
    # print ""
    # print "noise", noise
    # print ""
    FR = FiniteRepresentation( data, tree, noise )
    #FR.add_error_boxes()
    # print "Constructed tree and error boxes"

    FR.construct_mvm_simple()
    FR.graph_mis()
    FR.tree.remove( list(set(range(FR.tree.tree.size))-set(FR.mis)) )

    # convert nodes to integers starting at 0
    H = nx.convert_node_labels_to_integers( FR.mvm.graph, first_label=0 )
    
    # True Henon
    # our tree, mapper, enclosure
    tree = Tree(box,full=True)
    m = HenonMapper()
    ce = CombEnc(tree,m)

    for d in range(depth):
        print 'at depth', d
        ce.tree.subdivide()
        print 'subdivided:', ce.tree.size, 'boxes'
        ce.update()
        #print 'enclosure updated'
        I = graph_mis(ce.mvm)
        #print 'len(I) = ', len(I)
        print ''
        # now remove all boxes not in I (the maximal invariant set)
        ce.tree.remove(list(set(range(ce.tree.size))-set(I)))

    # now display the tree!
    boxes = ce.tree.boxes()
    gfx.show_uboxes(boxes, col='c', ecol='b')

    print "Plotting boxes... "
    fig = FR.show_boxes()
    fig = FR.show_error_boxes( color='r', fig=fig )

    confidence( ce.mvm, H )
