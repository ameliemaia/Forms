from forms.geometry import tetrahedron

reload( tetrahedron )


x = tetrahedron.Tetrahedron().mesh()
y = tetrahedron.Sierpinski().generate()

print x
print y

# Result: [nt.Transform(u'pSolid1'), nt.PolyPlatonicSolid(u'polyPlatonicSolid1')]
# Result: [nt.Transform(u'Sierpinski_Iteration_1')]

