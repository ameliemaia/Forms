"""
This module provides a set of classes for generating icosahedra meshes.

Icosahedron -- Generate a icosahedron mesh
Sierpinski  -- Generate a Sierpinski icosahedron fractal mesh
"""


import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.util as util

from forms.util.math import PHI, scaleVector
from forms.util.mesh import combineClean


class Icosahedron:
    

    """
    Generate a icosahedron and return the mesh.
    
    Keyword arguments:
        **kwargs -- a list of keyword arguments, refer to the pymel class documentation for the full list of arguments

    Return:
        mesh -- ( [pymel.core.nodetypes.Transform(u''), pymel.core.nodetypes.PolyPlatonicSolid(u'')] )
        
    """
    
    def mesh( self, **kwargs ):

        return pm.polyPlatonicSolid( solidType = 1, **kwargs )



class Sierpinski( Icosahedron ):
    

    def __init__( self ):

        self.scaleRatio = 1 + PHI


    """
    Generate and return the next iteration of the fractal as mesh.

    Parameters:
        mesh      -- the mesh to generate the next iteration of the fractal from ( pymel.core.nodetypes.Mesh )
        positions -- a list of vertex positions to place the dodecahedra at ( [,pymel.core.datatypes.FloatVector] )
        radius    -- the next radius ( float )
        iteration -- the next iteration ( int )
    
    Return:
        mesh -- ( pymel.core.nodetypes.Transform(u'') )

    """

    def __generateMesh( self, mesh, positions, radius, iteration ):
        
        instanceGroup   = pm.group( empty = True, name = "meshInstanceGroup" )

        positionsLength = len( positions )
        instances       = [ None ] * positionsLength

        for i in range(0, positionsLength):

            position = scaleVector( positions[ i ], radius )

            if i == 0:

                meshInstance = mesh
                meshInstance[ 0 ].setTranslation( position )

            else:

                meshInstance = pm.instance( mesh[ 0 ] )
                meshInstance[ 0 ].setTranslation(position)

            instances[ i ] = meshInstance[ 0 ]

        pm.parent( instances, instanceGroup, add = True )

        return combineClean( instanceGroup, "Sierpinski_Iteration_%i" % iteration ) 


    """
    Generate a Sierpinski Dodecahedron fractal mesh. 

    Parameters:
        radius     -- the radius of the final mesh ( default 10cm )
        iterations -- the amount of iterations ( default 1 )
    
    Return:
        mesh -- ( pymel.core.nodetypes.Transform(u'') )

    """

    def generate( self, radius = 10, iterations = 1 ):
        
        self.radius     = radius
        self.iterations = iterations
        
        print( "%s radius %f iterations %i" % ( self.__class__.__name__, self.radius, self.iterations ) )

        icosahedronRadius = float(self.radius) / util.pow( float(self.scaleRatio), float(self.iterations) )
        icosahedron       = self.mesh( radius = icosahedronRadius )
        icosahedra        = [ icosahedron ]
        
        pm.polySoftEdge( angle = 0 )
        
        positions = [ ]
        vertices  = icosahedron[ 0 ].vtx

        for vertex in vertices:

            position = vertex.getPosition()
            positions.append( dt.FloatVector( position ) )

    
        for i in range( iterations ):

            for j in range( len( positions ) ):

                positions[ j ] *= self.scaleRatio
                
            mesh = self.__generateMesh( icosahedra[ 0 ], positions, icosahedronRadius, ( i + 1 ) )
            
            icosahedronRadius *= self.scaleRatio

            icosahedra = [ mesh ]


        pm.xform( mesh[ 0 ], centerPivots = True )

        print( "Construction complete" )

        return mesh
    

    