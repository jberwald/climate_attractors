import numpy as np
import numpy.random as nprand
import matplotlib.pylab as plt
from rads.enclosure import UBoxSet,Tree
from rads.misc import gfx
from rads.graphs import DiGraph
from rads.graphs import algorithms as alg
from itertools import izip
import cPickle as pkl
from networkx import write_dot, write_gpickle


class BoxTree( Tree ):
    """
    Inherits from Tree. Local wrapper for functionality. Making
    it a separate object in case it has to do new and exciting things
    (like stretch boxes in odd ways).
    """
    def __init__( self, region, depth=6 ):
        """
        Initialize BoxTree with (compact) 'region'. Specify depth if
        desired. Number of boxes will equal (dim^depth)/2.
        """
        self.tree = Tree( region, full=True )
        for i in range( depth ):
            self.tree.subdivide()

    def insert( self, box ):
        return self.tree.insert( box )

    def search( self, box ):
        return self.tree.search( box )

    def boxes( self ):
        return self.tree.boxes()

    def remove( self, boxes ):
        self.tree.remove( boxes )

class FiniteRepresentation( object ): 
    """
    """
    def __init__( self, data, tree, noise, expansion=1. ):
        """
        Created a finite representation of the dynamics of a system
        from a collection of temporally ordered data points.

        data -- list or array of points in R^d. Index order specifies
        temporal order.

        tree -- BoxTree object initialized with the compact region
        containing the data. (See BoxTree class.)

        noise -- array of tuples or real numbers specifying the noise
        in each dimension of each data point. Hence, if data contains
        points in R^2, data[0] <--> noise[0] == ((a1,a2),(b1,b2)) or
        (a1, b1) if data[0] is centered within the error box
        determined bythe noise.  Note: This scheme assume (for the
        time being) that noise if uniform about each data point.
        """
        self.data = np.asarray( data, dtype=float )
        self.noise = noise
        self.tree = tree
        self.dim = data.ndim

        # x_i |--> {grid elements} mapping
        self.data_hash = {}
        
        self.expansion = expansion # constant expansion rate (very
                                   # crude approximation of dynamics)
  
    def _add_box( self, box ):
        """
        box -- lower left anchor in box[0], widths across dimensions
        in box[1].

        data point center in noise box, and width in j'th dimension
        specified by 2*noise[j].
        """
        # shift center to lower left corner anchor
        bx = self._make_box( box )
        self.tree.insert( bx )

    def _add_boxes_tuple( self ):
        """ TODO """
        print "NOT IMPLEMENTED!"

    def _make_box( self, b ):
        """
        b -- tuple or array of 
        """
        anchor = b[0] - (b[1] / 2.)
        if type( b ) == tuple:
            width = self.dim * [ b[1] ]
        else:
            width = b[1]
        bx = np.array( [ anchor, width ] )
        return bx
    
    def _expand_equal( self, idx ):
        """
        Expand box dimension equally by self.expansion in all
        directions. Since boxes are anchored in lower left corner,
        shift each coordinate by (self.expansion * w - w )/2, where w
        is the width of the box in each dimension.

        box : array( [[ x1,...,xd ], [ w1,...,wd ]] )

        Returns expanded and shifted box
        """
        B = self.tree.boxes()
        anchors = B.corners[ idx ]
        width = B.width
        new_width = self.expansion * width
        shift = ( new_width - width ) / 2.
        new_anchors = anchors - shift
        new_box = np.array( [ new_anchors, new_width ] )
        print new_box
        print ""
        return new_box
        
    def add_error_boxes( self ):
        """
        Intersect each noise box containing a data point with the grid
        contained in Tree. This is used to construct the grid on the
        phase space without a MVM. the MVM function perform the same
        operation during the construction of the map.
        """
        if hasattr( self.noise[0], '__len__' ):
            self._add_boxes_tuple()  # TODO
        else:
            errors = izip( self.data, self.noise )
            for box in errors:
                self._add_box( box )

    def boxes( self ):
        """ Return a list of all boxes in the tree. """
        return self.tree.boxes()

    def construct_mvm_simple( self ):
        """
        Construct a directed graph on the boxes in self.tree. Boxes
        intersecting error_box[i] are mapped to boxes intersecting
        error_box[i+1]. [No expansion estimates are used.]
        """
        # store the finite representation
        self.mvm = DiGraph()

        # generator to save memory
        error_boxes = izip( self.data, self.noise )

        # pull first time step off the top
        data_idx = 0
        pred = self._make_box( error_boxes.next() )
        pred_ids = self.tree.search( pred )

        self.data_hash[ data_idx ] = pred_ids
        
        # iteration starts at second element
        for succ in error_boxes:
            bx = self._make_box( succ )
            self.tree.insert( bx )
            succ_ids = self.tree.search( bx )
            
            # loop over boxes in predecessor region and create edge to
            # those in successor regions
            for u in pred_ids:
                for v in succ_ids:
                    self.mvm.add_edge( u, v )
                    
            # update predecessor for next time step
            pred = succ
            pred_ids = succ_ids
            data_idx += 1
            self.data_hash[ data_idx ] = pred_ids
            

    def construct_mvm_expansion( self ):
        """
        Construct a directed graph on the boxes in self.tree
        using. Boxes G_i intersecting error_box[i] are mapped to boxes
        G_{i+1} intersecting error_box[i+1] with expansion rate
        C. Thus the image boxes are expanded equally in all directions
        by a factor C > 1. This image is intersected with boxes in the
        tree and the image is updated.
        """
        # store the finite representation
        self.mvm = DiGraph()

        # generator to save memory
        error_boxes = izip( self.data, self.noise )

        # pull first time step off the top 
        pred = self._make_box( error_boxes.next() )
        pred_ids = self.tree.search( pred )

        # loop optimizations
        maker = self._make_box
        expander = self._expand_equal
        tree_insert = self.tree.insert
        tree_search = self.tree.search
        
        # iteration starts at second element
        for succ in error_boxes:
            # error in 'box' form
            bx = self._make_box( succ )
            # intersect with subdivision
            self.tree.insert( bx )
            succ_ids = self.tree.search( bx )
            
            # apply expansion to image
            ex_box = self._expand_equal( succ_ids )

            # DANGER! THIS MIGHT DOUBLE INSERT BOXES
            self.tree.insert( ex_box )       

            # loop over boxes in predecessor region and connect to
            # those in successor regions
            for u in pred_ids:
                for v in succ_ids:
                    self.mvm.add_edge( u, v )
            # update predecessor for next time step
            pred = succ
            pred_ids = succ_ids

    def graph_mis( self ):
        self.mis = alg.graph_mis( self.mvm )

    def trim_graph( self, copy=False ):
        """
        Trim the MVM graph to include only nodes from the maximal
        invariant set (i.e. the strongly connected component == SCC).

        copy : boolean. Default False. If True, copy original MVM to
        self.full_mvm. In either case, self.mvm is replaced by the
        SCC.
        """
        nbunch = set( self.mvm.nodes() )
        scc = set( self.mis )
        non_scc = nbunch - scc 

        if copy:
            self.full_mvm = DiGraph()
            # copy returns NX.DiGraph()
            self.full_mvm.graph = self.mvm.copy()
        self.mvm.remove_nodes_from( non_scc )

    def pickle_tree( self, fname, tree=None ):
        """
        Extact necessary information to create a persistent object.
        """
        if not tree:
            tree = self.tree
        b = tree.boxes()
        tree_dict = { 'corners' : b.corners,
                      'width' : b.width,
                      'dim' : b.dim,
                      'size' : b.size
                      }
        with open( fname, 'wb' ) as fh:
            pkl.dump( tree_dict, fh )

    def write_mvm( self, fname, stype='dot' ):
        """
        A wrapper around NX's graph writers.

        fname : full path to save graph to

        type : 'pkl' or 'dot' (default).  'pkl' => pickle the
        graph. 'dot' => save graph in dot format (more portable)
        """
        if stype == 'pkl':
            write_gpickle( self.mvm.graph, fname )
        else:
            write_dot( self.mvm.graph, fname )       

    def show_boxes( self, color='b', alpha=0.6 ):
        """
        """
        fig = gfx.show_uboxes( self.boxes(), col=color )
        return fig

    def show_error_boxes( self, box=None, color='r', alpha=0.6, fig=None ):
        """
        """
        error_boxes = izip( self.data, self.noise )
        # boxes = [ self._make_box( b ) for b in error_boxes ]
        # gfx.show_boxes( error_boxes, S=range( len(boxes) ), col=color,
        #                 alpha=alpha, fig=fig )
        for b in error_boxes:
            # shift center to lower left corner anchor
            bx = self._make_box( b )
            fig = gfx.show_box( bx, col=color, alpha=alpha, fig=fig )
        return fig


            
if __name__ == "__main__":
    
    npts = 2000

    # initial compact region X, anchored at (-2.0,2), w x h = 4 x 4
    box = np.array([[-2.0,-2],[4,4]])

    # init the tree
    depth = 7 # AKA resolution, 2^{-9} boxes 
    tree = BoxTree( box, depth )

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
    
    FR.expansion = 4.0
    #FR.construct_mvm_expansion()
    print "MVM done!"

    FR.graph_mis()

    FR.tree.remove( list(set(range(FR.tree.tree.size))-set(FR.mis)) )

    # print "Computed maximal invariant set (SCC)!"
    # print "len(FR.mis) = ", len( FR.mis )

    # if len( FR.mis ) != len( FR.mvm ):
    #     print "There are", len( FR.mvm ) - len( FR.mis ), "transient nodes."
    #     FR.trim_graph()
    #     print "Trimmed graph down the maximal invariant set (SCC)."

    print "Plotting boxes... "
    fig = FR.show_boxes()
    fig = FR.show_error_boxes( color='r', fig=fig )

    # fig2 = gfx.plt.figure()
    # ax = fig2.gca()
    # FR.mvm.draw( nodes_size=80, node_color='g', alpha=0.6, ax=ax)
