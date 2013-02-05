# Might have to change paths here, depending on your system and whether cython is in the PATH
exe = {
	'cython': 'cython --cplus'.split(), 
	'c++': 'g++',
	'c': 'gcc',
	}

# CAPD include and lib directories are loaded using the capd-config script
dirs = {
	'base': '/Users/jberwald/github/local/caja-matematica/rads/',
	'capd_config': '/Users/jberwald/src/capd/bin/capd-config ', #--cflags --libs`'
	'capd':  '/Users/jberwald/src/capd/'
        }


# paths to various include files. It is possible to build everything with Sage, too.
include = {
	   #	'sage': '/Applications/sage/devel/sage-main/',
	   #    'sage c': '/Applications/sage/devel/sage-main/c_lib/include/',
	'python': '/Library/Frameworks/EPD64.framework/Versions/Current/include/python2.7/',
	'cython': '/Library/Frameworks/EPD64.framework/Versions/Current/lib/python2.7/site-packages/Cython/Includes/',
	'numpy': '/Library/Frameworks/EPD64.framework/Versions/Current/lib/python2.7/site-packages/numpy/core/include/',
	'capd': '/Users/jberwald/src/capd/capdAlg/include/'
        }

# Paths to libraries for linking
link = {
	'capd': dirs['capd'],
	'c++ cython': '-L/Library/Frameworks/EPD64.framework/Versions/Current/lib -lpython2.7'.split(),
	'c++': '-L/Library/Frameworks/EPD64.framework/Versions/Current/lib -lpython2.7'.split()
	}
        

flags = {
	'c': '-fno-strict-aliasing -fno-common -arch x86_64 -DNDEBUG -O1'.split(),
	 'c++ cython': '-arch x86_64 -bundle -undefined dynamic_lookup'.split()
        }
