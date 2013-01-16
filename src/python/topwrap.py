import subprocess as sp
import top_utils


class TopWrapper( object ):

    def __init__( self, tool, **kwargs ):

        fargs = { 'pers_type': 'vr',
                  'chomp_type': 'cube' }
        fargs.update( kwargs )

        # select the analysis tool from a list given self.tool.
        self.avail_tools = [ 'perseus',
                             'chomp',
                             'dionysus',
                             'capd' ]
        if tool not in self.avail_tools:
            raise ValueError, "Topology tool '", tool, "' not found. Please choose from:\n"\
                + self.avail_tools

        self.tool = tool
        self._chooser()

    def __repr__( self ):
        s = "Wrapper for topological analysis using ", self.tool
        return s

    def _chooser( self ):
        """
        Choose analyzer from the list....
        """
        if self.tool == 'perseus':
            self.analyzer = self.perseus
        elif self.tool == 'chomp':
            self.analyzer = self.chomp
        elif self.tool == 'dionysus':
            print "Dionysus wrapper not implemented"
        else:
            print "CAPD wrapper not implemented"
    
    
    
