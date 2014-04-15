#!/usr/bin/python

import numpy as np
from rads.enclosure import CombEnc,Tree
from finite_representation import BoxTree,FiniteRepresentation
from rads.maps.henon import HenonMapper
from rads.graphs.algorithms import graph_mis
from rads.misc import gfx
import pprocess
import time
import utils

dot = "."

def test_rigorous_henon( depth, box, plot=False, fpath='../sandbox/henon_test' ):

	# our tree, mapper, enclosure
	tree = Tree(box,full=True)
	m = HenonMapper()
	ce = CombEnc(tree,m)

	for d in range(depth):
		#print 'at depth', d
		ce.tree.subdivide()
		#print 'subdivided:', ce.tree.size, 'boxes'
		ce.update()
		#print 'enclosure updated'
		I = graph_mis(ce.mvm)
		#print 'len(I) = ', len(I)
		#print ''
		# now remove all boxes not in I (the maximal invariant set)
		ce.tree.remove(list(set(range(ce.tree.size))-set(I)))

	if plot:
		# now display the tree!
		boxes = ce.tree.boxes()
		gfx.show_uboxes(boxes, col='c', ecol='b')
	print "done with rigorous henon @ depth", depth
	print ""
	
	fname = fpath + dot + "CE" + dot + str( depth )
	utils.write_dot( ce.mvm.graph, fname + '.dot' )
	utils.pickle_tree( ce.tree, fname + '.pkl' )
	

def test_finite_rep_henon( depth, box, npts, plot=False, fpath='../sandbox/henon_test' ):	 

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
	 #FR.construct_mvm_expansion()
	 print "MVM done!"
	 
	 FR.graph_mis()
	 print "Computed maximal invariant set (SCC)!"
	 print "len(FR.mis) = ", len( FR.mis )
	 
	 # if len( FR.mis ) != len( FR.mvm ):
	 #     print "There are", len( FR.mvm ) - len( FR.mis ), "transient nodes."
	 #     FR.trim_graph()
	 #     print "Trimmed graph down the maximal invariant set (SCC)."
	 
	 if plot:
		 print "Plotting boxes... "
		 fig = FR.show_boxes()
		 fig = FR.show_error_boxes( color='r', fig=fig )
	 print "done with FR @ depth", depth
	 print ""

	 fname = fpath + dot + "FR" + dot + str( depth ) + \
	     dot + str( npts ) 
	 FR.write_mvm( fname + '.dot' )
	 FR.pickle_tree( fname + '.pkl' )

#############################
# START TEST RUNS BELOW
#############################
 
if __name__ == "__main__":
	plot = False
	npts = 2000
	depth_list = [6,7]
	nprocs = 4

	# main bounding box
	box = np.array([[-2.0,-2],[4,4]])

	# init parallel jobs
	queue = pprocess.Queue(limit=nprocs)
	paraFinRep = pprocess.MakeParallel( test_finite_rep_henon )
	paraRigHenon = pprocess.MakeParallel( test_rigorous_henon )

	tstart = time.time()

	for d in depth_list:
		queue.start( paraRigHenon, *( d, box ) )
		queue.start( paraFinRep, *( d, box, npts ) )
		
	print "Time for computation: %f s." % ( time.time() - tstart )




