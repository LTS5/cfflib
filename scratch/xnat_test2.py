import cfflib as cf
a=cf.connectome()
#a=cf.load('/home/stephan/test/meta.cml')
interface = cf.pyxnat.Interface('http://sandbox.xnat.org','unidesigner', 'xnat2011')
a.set_xnat_connection(interface)
mycon = a.pull('debug', 'new007', 'consciousnessstudy', '/home/stephan/tes')
mycon.print_summary()
