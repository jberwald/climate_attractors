import xppy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#ode_file = 'lorenz96.ode'; color='b'
#ode_file = 'lorenz96v2.ode'; color='r'

# Lorenz 84
ode_file = 'lorenz84.ode'; color='b'

# init the xppy object
xppy.createTmp( ode_file )

# run it
out = xppy.run( )# ode_file )
# equivalent to xpp continue

pars = xppy.parse.readOdePars(ode_file, False, True, False)

ts = list( out[0] )
xs = list( out[1] )
ys = list( out[2] )
zs = list( out[3] )

# first, 3d
fig = plt.figure( 1 )
ax = fig.gca(projection='3d')
ax.plot( xs, ys, zs, color=color, marker='o' )#, lw=3, alpha=0.8)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# individual 2D plots
if 1:
    fig2 = plt.figure( 2, figsize=(8,12) )
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
fig2.show()

xppy.cleanUp()
