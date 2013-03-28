from forms.geometry import hexahedron

reload( hexahedron )


x = hexahedron.Hexahedron().mesh()
y = hexahedron.MengerSponge().generate()

print x
print y

# Result: [nt.Transform(u'pCube1'), nt.PolyCube(u'polyCube1')]
# Result: [nt.Transform(u'MengerSponge_Iteration_1')]

