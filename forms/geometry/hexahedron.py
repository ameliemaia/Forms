"""
This module provides a set of classes for generating Hexahedron meshes.

Hexahedron    -- Generate a Hexahedron mesh
Sierpinski    -- Generate a Sierpinski hexahedron fractal mesh
"""


import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.util as util

from forms.util.mesh import combineClean


class Hexahedron:


    """
    Generate a hexahedron and return the mesh.

    Keyword arguments:
        **kwargs -- a list of keyword arguments, refer to the pymel class documentation for the full list of arguments
    
    Return:
        mesh -- ( [pymel.core.nodetypes.Transform(u''), pymel.core.nodetypes.PolyCube(u'')] )
        
    """
    
    def mesh( self, **kwargs ):

        return pm.polyCube( **kwargs )



class Sierpinski( Hexahedron ):
    
    
    """
    Generate and return the next iteration of the fractal as mesh.

    Parameters:
        mesh      -- the mesh to generate the next iteration of the fractal from ( pymel.core.nodetypes.Mesh )
        size      -- the next sponge size ( float )
        iteration -- the next fractal iteration ( int )

    Return:
        mesh -- ( pymel.core.nodetypes.Transform(u'') )

    """
    
    def __generateMesh( self, mesh, size, iteration ):

        instanceGroup   = pm.group( empty = True, name = "meshInstanceGroup" )
        
        instances = [ None ] * util.pow( self.grid, 3 )
        
        # Instance a sponge, position it, then add it to the group
        
        def makeInstance( levels, rows, columns, index ):

            x = ( size * 1 ) - ( rows * size )
            y = ( size * 1 ) - ( levels * size )
            z = ( size * 1 ) - ( columns * size )

            if index == 0:

                meshInstance = mesh

            else:

                meshInstance = pm.instance( mesh[ 0 ] )

            meshInstance[ 0 ].setTranslation( [ x, y, z ] )
            instances.append( meshInstance[ 0 ] )
        

        # Generate the sponge instances
        
        i = 0   
        j = 0   
        
        for levels in range( self.grid ):

            for rows in range( self.grid ):

                for columns in range( self.grid ):

                    if i not in self.holes:

                        makeInstance( levels, rows, columns, j ) 

                        j += 1

                    i += 1

        
        pm.parent( instances, instanceGroup, add = True )
        
        return combineClean( instanceGroup, "Sierpinski_Iteration_%i" % iteration, True )
    


    """ 
    Generate a Sierpinski hexahedron fractal mesh. 

    Parameters:
        size       -- the size of the final mesh ( default 10cm )
        iterations -- the amount of iterations ( default 1 )
        grid       -- the grid subdivision amount ( default 3 )
        holes      -- a list of holes ( default [ 4, 10, 12, 13, 14, 16, 22 ] )
    
    Return:
        mesh -- ( pymel.core.nodetypes.Transform(u'') )

    """

    def generate( self, size = 10, iterations = 1, grid = 3, holes = [ 4, 10, 12, 13, 14, 16, 22 ] ):

        self.size       = size
        self.iterations = iterations
        self.grid       = grid
        self.holes      = holes

        print( "%s radius %f iterations %i" % ( self.__class__.__name__, self.size, self.iterations ) )
    
        cubeSize = float(self.size) /  util.pow( float(self.grid), float(self.iterations) )
        cube     = self.mesh( width = cubeSize, height = cubeSize, depth = cubeSize )    
        cubes    = [ cube ]
        
        for i in range( iterations ):

            mesh     = self.__generateMesh( cubes[ 0 ], cubeSize, ( i + 1 ) )
            cubeSize = cubeSize * self.grid
            cubes    = [ mesh ]


        pm.xform( mesh[ 0 ], centerPivots = True )

        print( "Construction complete" )

        return mesh
    