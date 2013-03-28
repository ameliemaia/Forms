"""
This module provides a set of classes for generating Koch curves.

Koch -- Generate a Koch curve
"""


import pymel.core as pm
import pymel.core.datatypes as dt
from forms.util.math import *


class _Edge():


    """
    Koch edge class.
    
    Parameters:
        v1    -- the starting vertex ( pymel.core.datatypes.FloatVector )
        v2    -- the ending vertex ( pymel.core.datatypes.FloatVector )
        angle -- the edge angle ( float )
  
    """

    def __init__( self, v1, v2, angle ):

        self.v1    = v1
        self.v2    = v2
        self.angle = angle



class Koch():


    def __init__( self ):

        self.divisor   = float(1) / float(3)
        self.edges     = [ ]
        self.verticies = [ ]
    

    """
    Generate a Koch edge and append the edges to self.
    
    Parameters:
        iteration -- the iteration level ( int )
  
    """

    def __curve( self, iteration ):   

        for i in range( iteration ):
            
            tmp = [ ]
            
            for j in range( len( self.edges ) ):
                
                edge = self.edges[ j ]
                
                v1 = edge.v1
                v2 = edge.v2

                vector = v2 - v1
                angle  = edge.angle
                
                nextSideLength = vector.length() * self.divisor
                height = nextSideLength * sqrt(3) / 2

                # start vertex
                start = v1 + vector * self.divisor

                # middle vertex
                middle    = dt.FloatVector()
                middle    = ( v1 + ( vector * 0.5 ) )
                middle.x += cos( angle - HALF_PI ) * height
                middle.y += sin( angle - HALF_PI ) * height
                
                #end vertex 
                end = v1 + vector * ( self.divisor * 2 )

                edge1 = _Edge( v1, start, angle )
                edge2 = _Edge( start, middle, angle + HALF_PI - ( HALF_PI / 3 ) )
                edge3 = _Edge( middle, end, angle - HALF_PI + ( HALF_PI / 3 ) )
                edge4 = _Edge( end, v2, angle )
                
                tmp += [ edge1, edge2, edge3, edge4 ]
            
            self.edges = tmp


    """
    Generate a Koch curve.
    
    Parameters:
        iteration -- the iteration level ( int )
        length    -- the edge length ( int || float )
  
    """

    def curve( self, iteration = 3, length = 10 ):
        
        self.edges = [ _Edge( dt.FloatVector( -length / 2, 0, 0 ), dt.FloatVector( length / 2, 0, 0 ), PI ) ]
        self.__curve( iteration )

    
    """
    Generate a Koch snowflake.
    
    Parameters:
        iteration -- the iteration level ( int )
        radius    -- the radius of the snowflake ( float or int )
  
    """

    def snowflake( self, iteration = 3, radius = 5 ):

        verticies = [ ]
        increment = TWO_PI / 3

        for i in range( 3 ):

            a = ( HALF_PI / 3 ) + i * increment
            x = radius * cos( a )
            y = radius * sin( a )
            z = 0
            v1 = dt.FloatVector( x, y, z )
            verticies.append( v1 )
        
        v1 = verticies[ 0 ]
        v2 = verticies[ 1 ]
        v3 = verticies[ 2 ]

        self.edges.append( _Edge( v2, v1, PI ) )
        self.edges.append( _Edge( v1, v3, (HALF_PI / 3) * 2 ) )
        self.edges.append( _Edge( v3, v2, TWO_PI - (HALF_PI / 3) * 2 ) )
        
        self.__curve( iteration )
         

    """
    Draw the Koch Curve.
    
    Return:
        curve -- ( pymel.core.nodetypes.Transform(u'') )

    """

    def drawCurve( self ):

        verticies = [ ]

        for edge in self.edges:
            
            verticies += [ edge.v1, edge.v2 ]

        curve = pm.curve( degree = 1, p = [ verticies[ 0 ], verticies[ 1 ] ] )

        for i in range( 2, len( verticies ) ):
            
            vertex = verticies[ i ]
            curve  = pm.curve( curve, p=[ vertex ], append = True )

        return curve

