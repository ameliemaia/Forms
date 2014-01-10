import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.util as util
import random
from functools import partial

class SurfaceDetail:

	def __init__( self ):
		self.reset()

	def reset( self ):

		self.iterations       = 3
		self.radius           = 5
		self.labels           = [ ]
		self.sliders          = [ ]
		self.sliderValues     = [ None ] * self.iterations
		self.meshTypes 		  = { 'Soccer Ball': 0, 'Dodecahedron': 0, 'Icosahedron': 1, 'Octahedron': 2, 'Tetrahedron': 3 } 
		self.meshType         = 'Soccer Ball'
		self.operations       = [ 'poke', 'quad' ]
		self.operation        = 'poke'
		self.mesh         	  = None
		self.indicies     	  = [ ]
		self.vertexIndicies   = [ ]
		self.vertexPositions  = [ ]


	def generate( self, meshType, radius, iterations, operation ):
		
		self.reset()

		self.meshType   = meshType
		self.radius     = radius
		self.iterations = iterations
		self.operation  = operation

		if self.meshType == 'Soccer Ball':
			self.mesh = pm.polyPrimitive( radius = self.radius, polyType = self.meshTypes[ self.meshType ] )
		else:
			self.mesh = pm.polyPlatonicSolid( radius = self.radius, solidType = self.meshTypes[ self.meshType ] )

		self.vertexIndicies = self.__subdivide()

		# Store each vertex position from each iteration
		for vertex in self.mesh[0].vtx:
			position = vertex.getPosition()
			self.vertexPositions.append( position )

		return self.mesh


	def setScale( self, scaleValues ):

		length = len( self.vertexIndicies )

		verticesStartIndex = 0
		verticesEndIndex   = 1

		for i in range( self.iterations + 1 ):

			verticesStartIndex = self.vertexIndicies[ i - 1 ]
			verticesEndIndex   = self.vertexIndicies[ i ]

			for j in range( verticesStartIndex, verticesEndIndex ):
				position = self.vertexPositions[ j ] * scaleValues[ i ]
				self.mesh[ 0 ].vtx[ j ].setPosition( position )


	def __subdivide( self ):

		vertices = [ ]

		for i in range( self.iterations ):
			
			_faces    = self.mesh[ 0 ].f
			_vertices = self.mesh[ 0 ].vtx
			length   = len( _vertices )

			if i is 0:
				vertices.append( length )

			if self.operation == 'quad': divisionMode = 0
			if self.operation == 'triangle': divisionMode = 1
			
			if self.operation == 'poke':
				pm.polyPoke( _faces, translateX = 0, translateY = 0, translateZ = 0, worldSpace = True )
			else:
				pm.polySubdivideFacet( _faces, mode = divisionMode, divisions = 1 )

			_faces    = self.mesh[ 0 ].f
			_vertices = self.mesh[ 0 ].vtx
			length   = len( _vertices )

			vertices.append( length )

		pm.select( clear = True )

		return vertices



# Generate some random solids

#tool = SurfaceDetail()

# for key in tool.meshTypes:

def surfaceDetailSolidGenerator():

	rows = 10
	cols = 10

	radius      = 10
	iterations  = 3
	scaleValues = []
	minScale    = 0.01
	maxScale    = 0.5

	for col in range(cols):
		for row in range(rows):

			x = col * (radius * 4)
			z = row * (radius * 4)

			for i in range(iterations):

				if i is 0:
					newScale = 1
				else:
					newScale = scaleValues[i-1] - random.uniform(minScale, maxScale) 

				scaleValues.append( newScale )

			meshType  = random.choice(tool.meshTypes.keys())
			# meshType  = 'Icosahedron'
			operation = random.choice(tool.operations)

			mesh = tool.generate(meshType, radius, iterations, operation)
			tool.setScale(scaleValues)
			mesh[0].setTranslation([x, 0, z])

			print 'FORM :: type: ', meshType, ' operation: ', operation 


#surfaceDetailSolidGenerator()
