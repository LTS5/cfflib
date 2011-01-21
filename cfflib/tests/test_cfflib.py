# ================================================================================== #
# TEST functions for the cfflib 
# ================================================================================== #


# ---------------------------------------------------------------------------------- #
from nose.tools import assert_true, assert_false, assert_equal, assert_almost_equal, assert_not_equal
from numpy.testing import assert_array_equal, assert_array_almost_equal
from cfflib import *
import tempfile
import os.path as op
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Load and store data locations
TMP = tempfile.gettempdir()
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test the connectome object and the CMetadata
def test_connectome():

    c = connectome()
    
    # Check for the default CMetadata
    assert_not_equal(c.connectome_meta, None)
    assert_equal(c.get_connectome_meta().get_name(), 'myconnectome')
    assert_equal(c.get_connectome_meta().get_generator(), 'cfflib')
    assert_equal(c.get_connectome_meta().get_version(), '2.0')
    
    # Check for the possibility to specify a name to the connectome
    c = connectome('Test connectome')
    assert_equal(c.get_connectome_meta().get_name(), 'Test connectome')
    
    # Check for the content and the CObjects
    assert_equal(c.get_all(), [])
    assert_true(c.hasContent_())
    
    # Check to set the CMetadata attributes
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
    
    # Check the description in CMetadata
    c.connectome_meta.set_description('First connectome object created with the tutorial.')
    assert_equal(c.connectome_meta.get_description(), 'First connectome object created with the tutorial.')
    
    # Check to remove the CMetadata and save the connectome
    c.connectome_meta = None
    save_to_cff(c, op.join(TMP, 'wrong.cff'))
    assert_false(op.exists(op.join(TMP, 'wrong.cff')))
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
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
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test the description and metadata
def test_desc_meta():

    c = connectome('desc & meta connectome')
    n = CNetwork()
    
    n.update_metadata({'m1':'v1', 'm2':121})
    assert_not_equal(n.get_metadata_as_dict(), None)
    assert_equal(n.get_metadata_as_dict()['m1'], 'v1')
    assert_equal(n.get_metadata_as_dict()['m2'], '121')
    
    n.update_metadata({'m1':'v2'})
    assert_equal(n.get_metadata_as_dict()['m1'], 'v2')
    
    n.set_description('An useless description...')
    assert_equal(n.get_description(),'An useless description...')
# ---------------------------------------------------------------------------------- #
    
    
# ---------------------------------------------------------------------------------- #
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
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CVolume
# With a Nifti1 file 
def test_cvolume_nifti1():

    c = connectome()
    
    v = CVolume.create_from_nifti('CVolume', 'data/Volumes/T1.nii.gz')
    assert_equal(v.get_name(), 'CVolume')
    
    v.set_name('My volume')
    assert_equal(v.get_name(), 'My volume')
    
    v.set_description('My first CVolume')
    assert_equal(v.get_description(), 'My first CVolume')
    
    v.update_metadata({'meta1':'only T1 scan of this patient'})
    assert_equal(v.get_metadata_as_dict()['meta1'], 'only T1 scan of this patient')
    
    c.add_connectome_volume(v)
    assert_not_equal(c.get_connectome_volume(), [])
    assert_equal(len(c.get_connectome_volume()), 1)
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CTrack
# with a trk file 
def test_ctrack_trk():

    c = connectome()
    
    t = CTrack.create_from_trackvis('my track', 'data/Tracks/fibers_transformed.trk')
    assert_equal(t.get_name(), 'my track')
    assert_equal(t.get_src(), 'CTrack/my_track.trk')

    c.add_connectome_track(t)
    assert_not_equal(c.get_connectome_track(), [])
    assert_equal(len(c.get_connectome_track()), 1)
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CTimeserie
# with a HDF5 file 
def test_ctimeserie_hdf5():

    c = connectome()
    
    t = CTimeserie.create_from_hdf5('my timeserie', 'data/Timeseries/generatedseries.hdf5')
    assert_equal(t.get_name(), 'my timeserie')
    assert_equal(t.get_src(), 'CTimeserie/my_timeserie.h5')

    c.add_connectome_timeserie(t)
    assert_not_equal(c.get_connectome_timeserie(), [])
    assert_equal(len(c.get_connectome_timeserie()), 1)
# ---------------------------------------------------------------------------------- #
   
    
# ---------------------------------------------------------------------------------- #
# Test CSurface
# with a Gifti file 
def test_csurface_gifti():

    c = connectome()
    
    s = CSurface.create_from_gifti('my surface', 'data/Surfaces/testsubject_labels.gii')
    assert_equal(s.get_name(), 'my surface')
    assert_equal(s.get_src(), 'CSurface/my_surface.gii')

    c.add_connectome_surface(s)
    assert_not_equal(c.get_connectome_surface(), [])
    assert_equal(len(c.get_connectome_surface()), 1)
# ---------------------------------------------------------------------------------- #


# ================================================================================== #
   
