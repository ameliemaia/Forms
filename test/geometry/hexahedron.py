from forms.geometry import hexahedron

reload( hexahedron )


x = hexahedron.Hexahedron().mesh()
y = hexahedron.Sierpinski().generate()

print x
print y

# Result: [nt.Transform(u'pCube1'), nt.PolyCube(u'polyCube1')]
# Result: [nt.Transform(u'Sierpinski_Iteration_1')]