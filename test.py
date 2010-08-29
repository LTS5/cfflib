from loadsave import *

a = load_from_cff('datasets/meta.cff')
#a = load_from_metaxml('datasets/meta.xml')

#myvol = a.get_by_name('T1-weighted single subject')[0]
#myvol.load()
#print myvol.content

mynetwork = a.get_by_name('Network Lausanne83')[0]
mynetwork.load()
print mynetwork.content