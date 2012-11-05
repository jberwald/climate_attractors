"""
basins.py

Author: Jesse Berwald

Opened: Oct. 11, 2012

Detection of attractor basins using topological methods.

Outline:

  1. Use a sequence of IC's to construct a list of trajectories in R^n.

  2. Determine which trajectories limit to the same basin. The goal is
  the learn the hull that defines a basin of attraction. For instance,
  suppose that we have topologially determined that a region has a
  fixed point. Now we want to expand this region. If a trajectory
  enters this region we can add the trajectory's IC to the basin of
  attraction. 

  3. Choosing additional points ???
  
      -- interpolate between IC's already shown to be in the basin ?? BAD, consider possible Cantor structure.

      -- Essential: Determine distance of attractor to boundary. But, where is the boundary.

  4. This module must support pluggable options: first, toy models
  with xpp; next pure data piped in from GCM's (or GCM like software)

  4a. The topological and data analysis tools must be separate from
  the IC tools in the sense that xppwrap just (via a pipeline) send
  its time + spatial output to the analysis object.

  4b. Hence, the analysis object must have a narrow interface that
  expects a numpy array (or maybe netcdf file path, but this can
  probably be pipelined).
  
  ** Current structure **  ( A -> B == "B inherits from A" )

  Trajectories: object to hold all trajectories and their attributes
  (eventually we want to label data in some way like"inside" and"outside")

  IO: all the necessary pipes to turn data into Trajectories object

  Topology -> Trajectories

  TopologyTools -> Topology  (Perseus, chomp, dionysus, etc)

  Dynamics -> Trajectories

  topwrap.TopWrapper, module and class containing all of the
  conversion necessary to run various topology software. Eg., if we
  wanted to call Perseus with simplicial data, all we would need to do
  is pass in the data as TopWrapper.perseus( data ) and perseus would
  then create a temp file, save the data there, work off of that,
  returning the file names of the results so that we can continue the
  analysis.

  ** In topwrap.py and/or top_utils.py, need to deal with creation of
     temp files/directories. How much do we want to keep?? How do we
     pass filenames around for analysis? **
    
"""
import xppwrap as XP
import topwrap import TopWrapper

class TopologyTools( TopWrapper ):
    """
    All of the tools necessary to analyze topological aspects of the
    trajetories.
    """
    def __init__( self, tool='perseus' ):
        
        TopWrapper.__init__( self, tool )

        
