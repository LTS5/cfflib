from loadsave import *

a = load('external/datasets_cff_v2/testdata.cff')

print cfflib.extract_file(a, a.connectome_volume[0].src)
