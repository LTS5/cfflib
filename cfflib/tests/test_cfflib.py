# ================================================================================== #
# TESTS functions for the cfflib 
# ================================================================================== #

from nose.tools import assert_true, assert_false, assert_equal, assert_almost_equal, assert_not_equal
from numpy.testing import assert_array_equal, assert_array_almost_equal
from cfflib import *
import tempfile
import os.path as op

# Load and store data locations
TMP        = tempfile.gettempdir()

# Test the connectome object and the CMetadata
def test_connectome():

    c = connectome()
    assert_not_equal(c.connectome_meta, None)
    assert_equal(c.get_connectome_meta().get_name(), 'myconnectome')
    assert_equal(c.get_connectome_meta().get_generator(), 'cfflib')
    assert_equal(c.get_connectome_meta().get_version(), '2.0')
    
    c = connectome('Test connectome')
    assert_equal(c.get_connectome_meta().get_name(), 'Test connectome')
    assert_equal(c.get_all(), [])
    assert_true(c.hasContent_())
    
    c.connectome_meta.set_name('My first connectome')
    assert_equal(c.connectome_meta.get_name(), 'My first connectome')
    
    c.connectome_meta.set_author('Connectome Tutorial')
    assert_equal(c.connectome_meta.get_author(), 'Connectome Tutorial')
    
    c.connectome_meta.set_institution('EPFL')
    assert_equal( c.connectome_meta.get_institution(), 'EPFL')
    
    c.connectome_meta.set_creation_date('2010-10-26')
    assert_equal(c.connectome_meta.get_creation_date(), '2010-10-26')
    
    c.connectome_meta.set_url('www.connectome.ch')
    assert_equal(c.connectome_meta.get_url(), 'www.connectome.ch')
    
    c.connectome_meta.set_description('First connectome object created with the tutorial.')
    assert_equal(c.connectome_meta.get_description(), 'First connectome object created with the tutorial.')

# Test the connectome network
# With nxgraph
def test_cnetwork_nxgraph():

    c = connectome()
    
    n = CNetwork()
    assert_equal(n.get_name(), 'mynetwork')
    
    n = CNetwork('Test network')
    assert_equal(n.get_name(), 'Test network')
    
    g = nx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0,1)
    g.add_edge(2,1)
    g.add_edge(0,2)
    
    n.set_with_nxgraph(g)
    assert_equal(n.get_name(), 'Test network')
    assert_equal(n.get_src(), 'CNetwork/test_network.gpickle')
    assert_equal(n.get_dtype(), 'AttributeNetwork')
    assert_equal(n.get_fileformat(), 'NXGPickle')
    
    c.add_connectome_network(n)
    assert_not_equal(c.get_connectome_network(), [])
    assert_equal(len(c.get_connectome_network()), 1)
    assert_not_equal(c.get_all(), [])
    
    c.get_connectome_network()[0].set_name('modif')
    assert_equal(n.get_name(), 'modif')

    c.add_connectome_network_from_nxgraph('2nd nxgraph', g)
    assert_equal(c.get_connectome_network()[1].get_name(), '2nd nxgraph')

# With graphml
def test_cnetwork_graphml():

    c = connectome()
    
    n = CNetwork.create_from_graphml('GraphML net', 'data/Networks/network_res83.graphml')
    assert_equal(n.get_name(), 'GraphML net')
    assert_equal(n.get_fileformat(), 'GraphML')
    c.add_connectome_network(n)
    assert_not_equal(c.get_connectome_network(), [])
    assert_equal(c.get_connectome_network()[0].get_src(), 'CNetwork/graphml_net.graphml')
    
    c.add_connectome_network_from_graphml('2nd graphml', 'data/Networks/network_res83.graphml')
    assert_equal(len(c.get_connectome_network()), 2)
    assert_equal(c.get_connectome_network()[1].get_name(), '2nd graphml')

# Test the description and metadata
def test_desc_meta():
    c = connectome('desc & meta connectome')
    n = CNetwork()
    n.update_metadata({'m1':'v1', 'm2':121})
    assert_not_equal(n.get_metadata_as_dict(), None)

# Test SAVE and LOAD 
def test_save_load():

    c = connectome('Load & Save connectome')
    assert_equal(c.get_connectome_meta().get_name(), 'Load & Save connectome')
    assert_equal(c.get_connectome_meta().get_generator(), 'cfflib')
    assert_equal(c.get_connectome_meta().get_version(), '2.0')
    
    c.add_connectome_network_from_graphml('GraphML net', 'data/Networks/network_res83.graphml')
    assert_equal(c.get_connectome_network()[0].get_src(), 'CNetwork/graphml_net.graphml')
    n = c.get_connectome_network()[0]
    n.update_metadata({'nb':123})
    assert_true(c.get_connectome_network()[0].get_metadata_as_dict().has_key('nb'))

    save_to_cff(c, op.join(TMP, 'test.cff'))
    
    c2 = load_from_cff(op.join(TMP, 'test.cff'))
    assert_equal(c2.get_connectome_meta().get_name(), 'Load & Save connectome')
    assert_equal(c2.get_connectome_meta().get_generator(), 'cfflib')
    assert_equal(c2.get_connectome_meta().get_version(), '2.0')
    assert_equal(c2.get_connectome_network()[0].get_src(), 'CNetwork/graphml_net.graphml')
    assert_true(c2.get_connectome_network()[0].get_metadata_as_dict().has_key('nb'))

#def test_save_nx2cff():
#    c = connectome('test networkx')
#    net = CNetwork('test')
#    assert_equal(net.get_metadata_as_dict(), {})
#    net.update_metadata({'sd':1234})
#    assert_true(net.get_metadata_as_dict().has_key('sd'))
#    assert_equal(net.get_metadata_as_dict(), {})
#    c.add_connectome_network(net)
#    net.set_with_nxgraph('tet', nx.Graph())
#    save_to_cff(c,'test.cff')


## test to save a CNetwork from GraphML to cff 
#def test_save_gml2cff():
#    c = connectome('test graphml')
#    net = CNetwork.create_from_graphml('my net', op.join(DATAFOLDER, 'network_res83.graphml'))
#    net.update_metadata({'sd':1234})
#    c.add_connectome_network(net)
#    save_to_cff(c,op.join(TMP,'test2.cff'))
#       
## test to save a CVolume from nifti1 file to cff 
#def test_load_save_cvol():
#    cv = CVolume.create_from_nifti('My first volume', op.join(DATAFOLDER, 'T1.nii.gz')) # Path to the nifti1 file
#    cv.set_description('My first CVolume')
#    cv.update_metadata({'meta1':'only T1 scan of this patient'})
#    c = connectome('test CVolume')
#    c.add_connectome_volume(cv)
#    save_to_cff(c,'test3.cff')
#        
## test to save a CSurface from gifti file to cff 
#def test_load_save_csurf():
#    
#    cs = CSurface.create_from_gifti('My first surface', op.join(DATAFOLDER, 'testsubject_labels.gii')) # Path to the gifti file
#    cs.set_description('My first CSurface')
#    cs.update_metadata({'meta1':'a metadata for my CSurface'})
#    c = connectome('test CSurface')
#    c.add_connectome_surface(cs)
#    save_to_cff(c,'test4.cff')
#    
#    
#    
