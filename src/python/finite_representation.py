import numpy as np
import numpy.random as nprand
import matplotlib.pylab as plt
from rads.enclosure import UBoxSet,Tree
from rads.misc import gfx
from rads.graphs import DiGraph
from rads.graphs import algorithms as alg
from itertools import izip


class BoxTree( Tree ):
    """
    Inherits from Tree. Mostly local wrapper for functionality.
    """
    def __init__( self, region, depth=6 ):
        """
        Initialize BoxTree with (compact) 'region'. Specify depth if
        desired. Number of boxes will equal (dim^depth)/2.
        """
        self.tree = Tree( region )
        for i in range( depth ):
            self.tree.subdivide()

    def insert( self, box ):
        return self.tree.insert( box )

    def search( self, box ):
        return self.tree.search( box )

    def boxes( self ):
        return self.tree.boxes()


class FiniteRepresentation( object ): 
    """
    """
    def __init__( self, data, tree, noise ):
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
        
    def add_error_boxes( self ):
        """
        Intersect each noise box containing a data point with the grid
        contained in Tree.
        """
        if hasattr( self.noise[0], '__len__' ):
            self._add_boxes_tuple()  # TODO
        else:
            errors = izip( self.data, self.noise )
            for box in errors:
                self._add_box( box )

    def boxes( self ):
        return self.tree.boxes()
          
    def show_boxes( self, color='b', alpha=0.6 ):
        """
        """
        gfx.show_uboxes( self.boxes(), col=color )

    def show_error_boxes( self, box=None, color='r', alpha=0.6 ):
        """
        """
        error_boxes = izip( self.data, self.noise )
        for b in error_boxes:
            # shift center to lower left corner anchor
            bx = self._make_box( b )
            gfx.show_box( bx, col=color, alpha=alpha )

    # def show_mvm_boxes( self, bcolor='b', ecolor='r' ):
    #     """
    #     """
    #     pos = dict()
    #     nbunch = self.graph.
    # TODO  ...

    def construct_mvm_simple( self ):
        """
        Construct a directed graph on the boxes in self.tree. Boxes
        intersecting error_box[i] are mapped to boxes intersecting
        error_box[i+1]. No expansion estimates are used. 
        """
        self.mvm = DiGraph()

        # generator to save memory
        error_boxes = izip( self.data, self.noise )

        # pull first time step off the top 
        pred = self._make_box( error_boxes.next() )
        pred_ids = self.tree.search( pred )

        # iteration starts at second element
        for succ in error_boxes:
            bx = self._make_box( succ )
            self.tree.insert( bx )
            succ_ids = self.tree.search( bx )
            # loop over boxes in predecessor region and connect to
            # those in successor regions
            for u in pred_ids:
                for v in succ_ids:
                    self.mvm.add_edge( u, v )
            # update predecessor for next time step
            pred = succ
            pred_ids = succ_ids

    def graph_maximal_inv_set( self ):
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


            
if __name__ == "__main__":
    
    npts = 100

    # initial compact region X, anchored at (-2.0,2), w x h = 4 x 4
    box = np.array([[-2.0,-2],[4,4]])

    # the trunk
    depth = 9 # AKA resolution
    tree = BoxTree( box, depth )

    # boxes defined by lower corner followed by width and height. So
    # np.array( [[1,2.],[1,3]] ) is anchored at (1,2), has width 1 and
    # height 3. Definition extends for higher dimensions (row 0 == anchor,
    # row 1 == size in j'th dimension).
    all_data = np.loadtxt( 'sandbox/squareNoiseHenonLong.txt' )
    data = all_data[:npts,:2]
    noise = all_data[:npts,2]
    print "data", data
    print ""
    print "noise", noise
    print ""
    
    FR = FiniteRepresentation( data, tree, noise )
    FR.add_error_boxes()
    print "Constructed tree and error boxes"

    FR.construct_mvm_simple()
    print "MVM done!"

    FR.graph_maximal_inv_set()
    print "Computed maximal invariant set (SCC)!"

    if len( FR.mis ) != len( FR.mvm ):
        print "There are", len( FR.mvm ) - len( FR.mis ), "transient nodes."
        FR.trim_graph()
        print "Trimmed graph down the maximal invariant set (SCC)."
    
    FR.show_boxes()
    FR.show_error_boxes( color='r' )

