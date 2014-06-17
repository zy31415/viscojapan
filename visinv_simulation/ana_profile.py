import pstats

stream = open('out', 'w')

p = pstats.Stats('stat', stream=stream)
p.strip_dirs()
p.sort_stats('tottime')
p.print_stats()

