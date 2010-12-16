# TESTS file 

# test to save a CNetwork from scratch to cff 
def test_savecff():
    import cfflib
    c=cfflib.connectome()
    import cfflib as cc
    c.connectome_meta=cc.CMetadata('test')
    net=cc.CNetwork('test')
    net.set_metadata({'sd':1234})
    c.add_connectome_network(net)
    import networkx as nx
    net.set_with_nxgraph('tet', nx.Graph())
    cc.save_to_cff(c,'test.cff')

# test to save a CNetwork from scratch to cml 
def test_savecml():
    import cfflib
    c=cfflib.connectome()
    import cfflib as cc
    c.connectome_meta=cc.CMetadata('test')
    net=cc.CNetwork.create_from_graphml('my net', 'network_res83.graphml')
    net.set_metadata({'sd':1234})
    c.add_connectome_network(net)
    cc.save_to_cff(c,'test2.cff')
       
# test to save a CVolume from nifti1 file to cff 
def test_load_save_cvol():
    from cfflib import *
    cv = CVolume.create_from_nifti('T1.nii.gz', 'My first volume') # Path to the nifti1 file
    cv.set_description('My first CVolume')
    cv.set_metadata({'meta1':'only T1 scan of this patient'})
    c = connectome()
    c.connectome_meta = CMetadata()
    c.add_connectome_volume(cv)
    save_to_cff(c,'test_cvol.cff')
    
# test to save a CVolume from scratch to cff 
# ERROR - it doesn't work: "there is nothing to save"
def test_load_save_cvol_ERROR():
    from cfflib import *
    cv = CVolume()
    cv.set_description('my first cvolume')
    cv.set_metadata({'m1':1234,'m2':'test'})
    c = connectome()
    c.connectome_meta = CMetadata()
    c.add_connectome_volume(cv)
    save_to_cff(c,'c.cff')
    
# test to save a CSurface from gifti file to cff 
def test_load_save_csurf():
    from cfflib import *
    cs = CSurface.create_from_gifti('testsubject_labels.gii', 'My first surface') # Path to the gifti file
    cs.set_description('My first CSurface')
    cs.set_metadata({'meta1':'a metadata for my CSurface'})
    c = connectome()
    c.connectome_meta = CMetadata()
    c.add_connectome_surface(cs)
    save_to_cff(c,'test_csurf.cff')
