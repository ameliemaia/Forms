"""
This module provides a class for generating spherical meshes.

Sphere -- Generate a sphere mesh
"""


import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.util as util

from forms.util.math import *

class Sphere:


	"""
	Generate a sphere and return the mesh.

	Keyword arguments:
		radius 			   -- Radius of the sphere
		subdivisionsAxis   -- The amount of subdivisions along the axis
		subdivisionsHeight -- The amount of subdivisions along the height

	Return:
		mesh -- ( [pymel.core.nodetypes.Transform(u''), pymel.core.nodetypes.PolyUnite(u'')] )

	"""

	def mesh( self, radius = 10, subdivisionsAxis = 8, subdivisionsHeight = 8 ):

		faces = []

		for i in range(subdivisionsHeight):
			for j in range(subdivisionsAxis):
				if i == 0 or i == subdivisionsHeight - 1:

					# bottom
					if i == subdivisionsHeight - 1:
						nextIndex = i
						y_index   = i + 1

					# top
					else:
						nextIndex = i + 1
						y_index   = i

					if j < subdivisionsAxis - 1:
						k = j + 1
					else:
						k = 0

					# Top vertex
					r1 = 0

					v0   = dt.FloatVector()
					v0.x = r1      * cos(j * (TWO_PI / subdivisionsAxis))
					v0.y = radius  * cos(y_index * (PI / subdivisionsHeight))
					v0.z = r1      * sin(j * (TWO_PI / subdivisionsAxis))

					# Left vertex
					r2 = radius  * sin(nextIndex * (PI / subdivisionsAxis))

					v1 	 = dt.FloatVector()
					v1.x = r2      * cos(j * (TWO_PI / subdivisionsAxis))
					v1.y = radius  * cos(nextIndex * (PI / subdivisionsHeight))
					v1.z = r2      * sin(j * (TWO_PI / subdivisionsAxis))

					# Right vertex
					v2 	 = dt.FloatVector()
					v2.x = r2      * cos(k * (TWO_PI / subdivisionsAxis))
					v2.y = radius  * cos(nextIndex * (PI / subdivisionsHeight))
					v2.z = r2      * sin(k * (TWO_PI / subdivisionsAxis))

					vertices = [v0, v1, v2]

					if i == subdivisionsHeight - 1:
						vertices = [v0, v1, v2]
					else:
						vertices = [v2, v1, v0]

					faces.append(pm.polyCreateFacet(p=vertices))

				else:

					nextIndex = i + 1

					if j < subdivisionsAxis - 1:
						k = j + 1
					else:
						k = 0

					# Bottom y
					r1 = radius * sin(i * (PI / subdivisionsAxis))
					y1 = radius * cos(i * (PI / subdivisionsHeight))

					# Top y
					r2 = radius * sin(nextIndex * (PI / subdivisionsAxis))
					y2 = radius * cos(nextIndex * (PI / subdivisionsHeight))

					# Top left vertex
					v0   = dt.FloatVector()
					v0.x = r2 * cos(j * (TWO_PI / subdivisionsAxis))
					v0.y = y2
					v0.z = r2 * sin(j * (TWO_PI / subdivisionsAxis))

					# Bottom left vertex
					v1   = dt.FloatVector()
					v1.x = r1 * cos(j * (TWO_PI / subdivisionsAxis))
					v1.y = y1
					v1.z = r1 * sin(j * (TWO_PI / subdivisionsAxis))

					# Bottom right vertex
					v2 = dt.FloatVector()
					v2.x = r1 * cos(k * (TWO_PI / subdivisionsAxis))
					v2.y = y1
					v2.z = r1 * sin(k * (TWO_PI / subdivisionsAxis))

					# Top right vertex
					v3 	 = dt.FloatVector()
					v3.x = r2 * cos(k * (TWO_PI / subdivisionsAxis))
					v3.y = y2
					v3.z = r2 * sin(k * (TWO_PI / subdivisionsAxis))

					vertices = [v0, v1, v2, v3]

					faces.append(pm.polyCreateFacet(p=vertices))

		return pm.polyUnite(faces, ch = False)

Sphere().mesh(10, 16, 16)