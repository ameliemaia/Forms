"""
This module provides a set of classes for generating octahedral meshes.

Octahedron -- Generate a octahedron mesh
Sierpinski -- Generate a Sierpinski octahedron fractal mesh
"""


import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.util as util

from forms.util.mesh import combineClean


class Octahedron:
    
    
    """
    Generate a octahedron and return the mesh.
    
    Keyword arguments:
        **kwargs -- a list of keyword arguments, refer to the pymel class documentation for the full list of arguments

    Return:
        mesh -- ( [pymel.core.nodetypes.Transform(u''), pymel.core.nodetypes.PolyPlatonicSolid(u'')] )

    """

    def mesh( self, **kwargs ):

        return pm.polyPlatonicSolid( solidType = 2, **kwargs )



class Sierpinski( Octahedron ):
    

    """
    Generate and return the next iteration of the fractal as mesh.

    Parameters:
        mesh      -- the mesh to generate the next iteration of the fractal from ( pymel.core.nodetypes.Mesh )
        height    -- the next height ( float )
        radius    -- the next radius ( float )
        iteration -- the next iteration ( int )
    
    Return:
        mesh -- ( pymel.core.nodetypes.Transform(u'') )

    """

    def __generateMesh( self, mesh, height, radius, iteration ):

        instanceGroup = pm.group( empty = True, name = "meshInstanceGroup" )

        x = 0
        y = 0
        z = 0
            
        # Top
        meshInstance1 = mesh
        meshInstance1[ 0 ].setTranslation( [ x, height, z ] )        
        
        # Right
        meshInstance2 = pm.instance( mesh[ 0 ] )
        meshInstance2[ 0 ].setTranslation( [ radius, y, z ] )
        
        # Back
        meshInstance3 = pm.instance( mesh[ 0 ] )
        meshInstance3[ 0 ].setTranslation( [ x, y, -radius ] )           
        
        # Left
        meshInstance4 = pm.instance( mesh[ 0 ] )
        meshInstance4[ 0 ].setTranslation( [ -radius, y, z ] )
        
        # Front
        meshInstance5 = pm.instance( mesh[ 0 ] )
        meshInstance5[ 0 ].setTranslation( [ x, y, radius ] )          
        
        # Bottom
        meshInstance6 = pm.instance( mesh[ 0 ] )
        meshInstance6[ 0 ].setTranslation( [ x, -height, z ] ) 
                
        pm.parent( meshInstance1[ 0 ], meshInstance2[ 0 ], meshInstance3[ 0 ], meshInstance4[ 0 ], meshInstance5[ 0 ], meshInstance6[ 0 ], instanceGroup, add = True )        

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

        octahedronRadius = float(self.radius) / util.pow( float(2), float(self.iterations ) )
        octahedron       = self.mesh( radius = octahedronRadius )
        octahedra        = [ octahedron ]
        
        pm.polySoftEdge( angle = 0 )   

        octahedronHeight = octahedron[ 1 ].getSideLength() / util.sqrt( 2 )
    
        for i in range( iterations ):
            
            mesh = self.__generateMesh( octahedra[ 0 ], octahedronHeight, octahedronRadius, ( i + 1 ) )
            
            octahedronHeight *= 2            
            octahedronRadius *= 2            
            
            octahedra = [ mesh ]
        

        pm.xform( mesh[ 0 ], centerPivots = True )

        print( "Construction complete" )
        
        return mesh
    

    