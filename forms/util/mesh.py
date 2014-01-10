"""
This module provides various mesh utilities for cleaning and extruding.
"""


import pymel.core as pm
import maya.mel as mel

	

"""
Combine multiple polygon meshes with the option of removing duplicate internal faces.

Parameters:
	instanceGroup  -- A group of meshes to combine ( pymel.core.general.group )
	meshName       -- A name for the mesh output ( default "mesh" )
	duplicateFaces -- Optionally remove lamina and the faces they share ( default False )

Return:
	mesh -- ( pymel.core.nodetypes.Transform(u'') )
		
"""

def combineClean( instanceGroup, meshName, duplicateFaces = False ):
			
	print( "Combining mesh" )
	
	mesh = pm.polyUnite( instanceGroup, name = meshName, constructionHistory = False )

	#print( "Merging %i" % len( mesh[ 0 ].vtx ) + " verticies" )
	pm.polyMergeVertex( mesh[ 0 ].vtx, distance = 0.1 )
	#print( "Reduced to %i" % mesh[ 0 ].numVertices() + " verticies" )

	if duplicateFaces:

		print( "Cleaning up faces" )

		pm.select( mesh[ 0 ] )
		pm.selectType( polymeshFace = True )
		pm.polySelectConstraint( mode = 3, type = 0x0008, topology = 2 )
		
		# Don't ask me how I did this

		mel.eval('polyCleanupArgList 3 { "0","2","0","0","0","0","0","0","0","1e-005","0","1e-005","1","0.3","0","-1","1" };') 
		
		pm.delete()
		pm.polySelectConstraint( mode = 0, topology = 0 ) 
		pm.selectType( polymeshFace = False )   
		pm.selectMode( object = True )

		print( "Faces reduced" )      


	if pm.PyNode( instanceGroup ).exists():
		
		pm.delete( instanceGroup )


	pm.delete( constructionHistory = True )
	pm.select( clear = True )
	
	print( "Cleaning up complete" )

	return mesh



"""
Create a wireframe style mesh
Ported from jh_polyWire.mel http://www.creativecrash.com/maya/downloads/scripts-plugins/modeling/poly-tools/c/convert-to-polywire

Parameters:
	mesh        -- The mesh to convert ( pm.core.nodetypes.Mesh )
	gridSize    -- The thickness of the borders ( default 0.9 )
	depth       -- The depth of the extrusion. The value is relative to the scale of the model ( default 0.5 )
	extrudeMode -- The extrusion mode. 0 to scale the faces in world space, 1 to translate the faces in local space ( default 1 )

"""
def polyWire( mesh, gridSize = 0.9, depth = 0.5, extrudeMode = 0 ):

	# Select the faces
	pm.select( mesh[ 0 ].f )

	# Extrude and scale the faces
	extrude = pm.polyExtrudeFacet( constructionHistory = True, keepFacesTogether = False, divisions = 1, twist = 0, taper = 0, off = 0 )
	pm.PyNode( extrude[ 0 ] ).localScale.set( [ gridSize, gridSize, gridSize ] )
	
	#return

	# Delete inner faces
	pm.delete()

	pm.select( mesh[ 0 ].f )

	# Extrude the faces
	extrude = pm.polyExtrudeFacet( constructionHistory = True, keepFacesTogether = True, divisions = 1, twist = 0, taper = 0, off = 0 )
	
	if extrudeMode == 0:
		
		 pm.PyNode( extrude[ 0 ] ).scale.set( [ depth, depth, depth ] )
	
	elif extrudeMode == 1:
		
		pm.PyNode( extrude[ 0 ] ).localTranslate.set( [ 0, 0, depth ] )
	

	pm.select( clear = True )

