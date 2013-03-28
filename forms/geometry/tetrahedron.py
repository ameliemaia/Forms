"""
This module provides a set of classes for generating tetrahedral meshes.

Tetrahedron -- Generate a tetrahedron mesh
Sierpinski  -- Generate a Sierpinski tetrahedron fractal mesh
"""


import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.util as util

from forms.util.mesh import combineClean


class Tetrahedron:
    

    """
    Generate a tetrahedron and return the mesh.
    
    Keyword arguments:
        **kwargs -- a list of keyword arguments, refer to the pymel class documentation for the full list of arguments

    Return:
        mesh -- ( [pymel.core.nodetypes.Transform(u''), pymel.core.nodetypes.PolyPlatonicSolid(u'')] )
        
    """

    def mesh( self, **kwargs ):

        return pm.polyPlatonicSolid( solidType = 3, **kwargs )



class Sierpinski( Tetrahedron ):
    

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

    def __generateMesh( self, mesh, height, radius, sideLength, positions, iteration ):
       
        instanceGroup = pm.group( empty = True, name = "meshInstanceGroup" )
        
        x = 0
        y = positions[ 0 ].y 
        z = 0

        # vertex indices's
        # [ 0 ] is right
        # [ 1 ] is left
        # [ 2 ] is front
        # [ 3 ] is top

        backVtx = positions[ 1 ]
        
        # Top
        meshInstance1 = pm.PyNode( mesh[ 0 ] )
        meshInstance1.setTranslation( [ x, y + height, z ] )
        
        # Right
        meshInstance2 = pm.instance( mesh[ 0 ] )
        meshInstance2[ 0 ].setTranslation( [ backVtx.x, y, -backVtx.z ] )

        # Left
        meshInstance3 = pm.instance( mesh[ 0 ] )
        meshInstance3[ 0 ].setTranslation( [ backVtx.x, y, backVtx.z ] )
        
        # Front
        meshInstance4 = pm.instance( mesh[ 0 ] )
        meshInstance4[ 0 ].setTranslation( [ radius, y, z ] )
                            
        pm.parent( [ meshInstance1, meshInstance2[ 0 ], meshInstance3[ 0 ], meshInstance4[ 0 ] ], instanceGroup, add = True )        
        
        return combineClean( instanceGroup, "Sierpinski_Iteration_%i" % iteration )



    """
    Generate a Sierpinski Tetrahedron fractal mesh. 

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

        tetrahedronRadius = float(self.radius) / util.pow( float(2), float(self.iterations ) )
        tetrahedron       = self.mesh( radius = tetrahedronRadius )
        tetrahedra        = [ tetrahedron ]

        pm.polySoftEdge( angle = 0 )
        
        sideLength        = tetrahedron[ 1 ].getSideLength()
        tetrahedronHeight = util.sqrt(6) / 3 * sideLength
        
        positions = [ ]

        for vertex in tetrahedron[ 0 ].vtx:

            position = vertex.getPosition()
            positions.append( dt.FloatVector( position ) );


        for i in range( iterations ):

            mesh = self.__generateMesh( tetrahedra[ 0 ], tetrahedronHeight, tetrahedronRadius, sideLength, positions, ( i + 1 ) )
            
            for j in range( len( positions ) ):
                
                positions[ j ] *= 2
            
            tetrahedronHeight = tetrahedronHeight * 2
            tetrahedronRadius = tetrahedronRadius * 2
            sideLength        = sideLength * 2
            
            tetrahedra = [ mesh ]
        

        print( "Construction complete" )

        return mesh

    