"""
Various math utilities module.
"""


import pymel.util as util


""" Constant PHI """
PHI = 1.61803399


""" Math shorthand constants and methods """
PI      = util.arrays.pi
HALF_PI = PI / 2
TWO_PI  = PI * 2
cos     = util.arrays.cos
sin     = util.arrays.sin
degrees = util.arrays.degrees
radians = util.arrays.radians
sqrt    = util.arrays.sqrt


"""
Scale vector arguments:
	
Parameters:
	vector -- the vector ( dt.Vector || dt.FloatVector )
	scale  -- a ratio to scale the vectors magnitude


Return:
	scaledVector -- ( dt.Vector || dt.FloatVector )

"""

def scaleVector( vector, scale ):

	scaledVector  = vector
	scaledVector *= ( float(1) - float(scale) / float(vector.length()) )
	
	return scaledVector
