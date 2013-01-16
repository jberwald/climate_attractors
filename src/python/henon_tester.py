import xppy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#ode_file = 'lorenz96.ode'; color='b'
#ode_file = 'lorenz96v2.ode'; color='r'

# Lorenz 84
ode_file = 'henon.ode'

set_file = 'henon.set'

# Create temporary (copies) of ode and set file.
# For security reasons it is better to work on copies instead of original files.
xppy.createTmp(ode_file, set_file)


# List with papameters to change, you can use constants or variables
pars = [['par', 'a', 1.25],
        ['par', 'b',  .3]]


print pars 
# Change parameters in the temporary set file
# (you can change specific file by giving it's name as the argument)
xppy.changeSet( pars )

# init the xppy object
#xppy.createTmp( ode_file )

# run it
out = xppy.run( )# ode_file )
# equivalent to xpp continue

pars = xppy.parse.readOdePars(ode_file, False, True, False)

ts = list( out[0] )
xs = list( out[1] )
ys = list( out[2] )

print "len", len(xs)

# for i in range(2):
#     print "OUT"
#     print out.getRawData()
#     print "    ", out[0]
#     out = xppy.runLast( out, verbose=False )

#     print out.getRawData()

#     # runLast() computes time from 0..20 only, even though it restarts
#     # from the latest IC. Account for this below
#     #0:time, 1:u[1], ..., 21:u[21]

#     # ts.extend( 20*(i+1)+out[0] )
#     # xs.extend( out[1] )
#     # ys.extend( out[2] )

    

# first
fig = plt.figure(1)
ax = fig.gca()

ax.plot( xs, ys, 'bo', ms=4 )
ax.set_xlabel("X")
ax.set_ylabel("Y")

# individual 2D plots
if 0:
    fig2 = plt.figure(2,figsize=(8,12))
    ax1 = fig2.add_subplot( 311 )
    ax1.plot( ts, xs, color=color, linestyle='-', lw=2, label='x' )
    ax2 = fig2.add_subplot( 312 )
    ax2.plot( ts, ys, color=color, linestyle='-', lw=2, label='y' )
    ax3 = fig2.add_subplot( 313 )
    ax3.plot( ts, zs, color=color, linestyle='-', lw=2, label='z' )
#ax1.legend()

# # X vs Y
# ax2 = fig2.add_subplot(322)
# ax2.plot( xs, ys, 'b-', lw=2, label='x vs y' )
# ax2.legend()
# # X vs Z
# ax3 = fig2.add_subplot( 324 )
# ax3.plot( xs, zs, 'r-', lw=2, label='x vs y' )
# ax3.legend()
# # Y vs Z
# ax4 = fig2.add_subplot( 326 )
# ax4.plot( ys, zs, 'g-', lw=2, label='y vs z' )
# ax4.legend()


fig.show()
#fig2.show()
