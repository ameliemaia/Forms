import cProfile
import pstats
from forms.geometry import hexahedron

# TODO... Make some sort of profiling util

cProfile.run('hexahedron.MengerSponge().generate(50, 4)', "prof_result")
p = pstats.Stats('prof_result')
p.sort_stats('cumulative').print_stats(10)
