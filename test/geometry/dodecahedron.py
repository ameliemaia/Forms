from forms.geometry import dodecahedron

reload( dodecahedron )


x = dodecahedron.Dodecahedron().mesh()
y = dodecahedron.Sierpinski().generate()

print x
print y

# Result: [nt.Transform(u'pSolid1'), nt.PolyPlatonicSolid(u'polyPlatonicSolid1')]
# Result: [nt.Transform(u'Sierpinski_Iteration_1')]

