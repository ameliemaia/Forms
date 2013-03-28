from forms.geometry import octahedron

reload( octahedron )


x = octahedron.Octahedron().mesh()
y = octahedron.Sierpinski().generate()

print x
print y

# Result: [nt.Transform(u'pSolid1'), nt.PolyPlatonicSolid(u'polyPlatonicSolid1')]
# Result: [nt.Transform(u'Sierpinski_Iteration_1')]

