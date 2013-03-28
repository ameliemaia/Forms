import pymel.core as pm
import forms.util.mesh as meshUtil

reload ( meshUtil )


sphere = pm.polySphere( subdivisionsAxis = 8, subdivisionsX = 8, subdivisionsY = 8, subdivisionsHeight = 8, radius = 10 )

mesh1 = pm.duplicate( sphere[ 0 ] )
mesh2 = pm.duplicate( sphere[ 0 ] )
mesh1[ 0 ].setAttr( 'translateZ', -20 )
mesh2[ 0 ].setAttr( 'translateZ', 20 )

meshUtil.polyWire( mesh1, depth = 0.9, extrudeMode = 0 )
meshUtil.polyWire( mesh2, depth = 0.9, extrudeMode = 1 )

print mesh1
print mesh2

# Result: [nt.Transform(u'pSphere2')]
# Result: [nt.Transform(u'pSphere3')]

mesh1 = pm.duplicate( sphere[ 0 ] )
mesh2 = pm.duplicate( sphere[ 0 ] )
mesh3 = pm.duplicate( sphere[ 0 ] )

mesh1[ 0 ].setTranslation( [ -20, 0, -10 ] )
mesh2[ 0 ].setTranslation( [ -20, 0, 10 ] )
mesh3[ 0 ].setTranslation( [ -20, 0, 0 ] )

meshUtil.combineClean( pm.group( mesh1, mesh2, mesh3 ), 'combineCleanResult' )

# Result: [nt.Transform(u'combineCleanResult')]