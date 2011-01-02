# TESTS file 

# test to save a CNetwork from NetworkX object to cff 
def test_save_nx2cff():
    from cfflib import *
    c = connectome('test networkx')
    net = CNetwork('test')
    net.update_metadata({'sd':1234})
    c.add_connectome_network(net)
    net.set_with_nxgraph('tet', nx.Graph())
    save_to_cff(c,'test.cff')

# test to save a CNetwork from GraphML to cff 
def test_save_gml2cff():
    from cfflib import *
    c = connectome('test graphml')
    net = CNetwork.create_from_graphml('my net', 'network_res83.graphml')
    net.update_metadata({'sd':1234})
    c.add_connectome_network(net)
    save_to_cff(c,'test2.cff')
       
# test to save a CVolume from nifti1 file to cff 
def test_load_save_cvol():
    from cfflib import *
    cv = CVolume.create_from_nifti('My first volume', 'T1.nii.gz') # Path to the nifti1 file
    cv.set_description('My first CVolume')
    cv.update_metadata({'meta1':'only T1 scan of this patient'})
    c = connectome('test CVolume')
    c.add_connectome_volume(cv)
    save_to_cff(c,'test3.cff')
        
# test to save a CSurface from gifti file to cff 
def test_load_save_csurf():
    from cfflib import *
    cs = CSurface.create_from_gifti('My first surface', 'testsubject_labels.gii') # Path to the gifti file
    cs.set_description('My first CSurface')
    cs.update_metadata({'meta1':'a metadata for my CSurface'})
    c = connectome('test CSurface')
    c.add_connectome_surface(cs)
    save_to_cff(c,'test4.cff')
    
    
    
