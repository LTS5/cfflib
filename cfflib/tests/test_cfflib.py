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
    
    # Check the default values
    n = CNetwork()
    assert_equal(n.get_name(), 'mynetwork')
    assert_equal(n.get_dtype(), 'AttributeNetwork')
    assert_equal(n.get_fileformat(), 'GraphML')
    assert_equal(n.get_metadata_as_dict(), {})
    
    # Check given values
    n = CNetwork('Test network', metadataDict={'number':1024})
    assert_equal(n.get_name(), 'Test network')
    assert_true(n.get_metadata_as_dict().has_key('number'))
    assert_equal(n.get_metadata_as_dict()['number'], '1024')
    
    g = nx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_edge(0,1)
    g.add_edge(2,1)
    g.add_edge(0,2)
    
    # Check the properties when the network is set with a nxgraph
    n.set_with_nxgraph(g)
    assert_equal(n.get_name(), 'Test network')
    assert_equal(n.get_src(), 'CNetwork/test_network.gpickle')
    assert_equal(n.get_dtype(), 'AttributeNetwork')
    assert_equal(n.get_fileformat(), 'NXGPickle')
    
    # Check the add function to connectome
    c.add_connectome_network(n)
    assert_not_equal(c.get_connectome_network(), [])
    assert_equal(len(c.get_connectome_network()), 1)
    assert_not_equal(c.get_all(), [])
    
    # Check to change the name of the nework directly from the connectome
    c.get_connectome_network()[0].set_name('modif')
    assert_equal(n.get_name(), 'modif')
    
    # Check the 2nd way to add a nxgraph network
    c.add_connectome_network_from_nxgraph('2nd nxgraph', g)
    assert_equal(c.get_connectome_network()[1].get_name(), '2nd nxgraph')
    
    # Check to change the name of the 2nd nework to match the first network name
    # TODO fix issue: make it impossible !!
    c.get_connectome_network()[1].set_name('modif')
    assert_equal(n.get_name(), c.get_connectome_network()[1].get_name())

# With graphml
def test_cnetwork_graphml():

    c = connectome()
    
    # Check the classmethod and default attributes
    n = CNetwork.create_from_graphml('GraphML net', 'data/Networks/network_res83.graphml')
    assert_equal(n.get_name(), 'GraphML net')
    assert_equal(n.get_fileformat(), 'GraphML')
    assert_equal(n.get_src(), 'CNetwork/graphml_net.graphml')
    assert_equal(n.get_dtype(), 'AttributeNetwork')
    
    # Check to add to the connectome
    c.add_connectome_network(n)
    assert_not_equal(c.get_connectome_network(), [])
    assert_equal(c.get_connectome_network()[0].get_src(), 'CNetwork/graphml_net.graphml')
    
    # Check to directly add to the connectome
    c.add_connectome_network_from_graphml('2nd graphml', 'data/Networks/network_res83.graphml')
    assert_equal(len(c.get_connectome_network()), 2)
    assert_equal(c.get_connectome_network()[1].get_name(), '2nd graphml')
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test the description and metadata
def test_desc_meta():

    c = connectome('desc & meta connectome')
    
    # Check the updated keys and corresponding values
    n = CNetwork(metadataDict={'m0':'v0'})
    n.update_metadata({'m1':'v1', 'm2':121})
    assert_not_equal(n.get_metadata_as_dict(), None)
    assert_true(n.get_metadata_as_dict().has_key('m0'))
    assert_true(n.get_metadata_as_dict().has_key('m1'))
    assert_true(n.get_metadata_as_dict().has_key('m2'))
    assert_equal(n.get_metadata_as_dict()['m0'], 'v0')
    assert_equal(n.get_metadata_as_dict()['m1'], 'v1')
    assert_equal(n.get_metadata_as_dict()['m2'], '121')
    
    # Check the update of an existing key 
    n.update_metadata({'m1':'v2'})
    assert_equal(n.get_metadata_as_dict()['m1'], 'v2')
    
    #  Check the description 
    n.set_description('An useless description...')
    assert_equal(n.get_description(),'An useless description...')
# ---------------------------------------------------------------------------------- #
    
    
# ---------------------------------------------------------------------------------- #
# Test SAVE and LOAD 
def test_save_load():

    # Check CMetadata attributes
    c = connectome('Load & Save connectome')
    assert_equal(c.get_connectome_meta().get_name(), 'Load & Save connectome')
    assert_equal(c.get_connectome_meta().get_generator(), 'cfflib')
    assert_equal(c.get_connectome_meta().get_version(), '2.0')
    
    # Check CNetwork
    c.add_connectome_network_from_graphml('GraphML net', 'data/Networks/network_res83.graphml')
    assert_equal(c.get_connectome_network()[0].get_src(), 'CNetwork/graphml_net.graphml')
    n = c.get_connectome_network()[0]
    
    # Check Metadata
    n.update_metadata({'nb':123})
    assert_true(c.get_connectome_network()[0].get_metadata_as_dict().has_key('nb'))

    # Save and load
    save_to_cff(c, op.join(TMP, 'test.cff'))
    c2 = load_from_cff(op.join(TMP, 'test.cff'))
    
    # Check the loaded connectome properties
    assert_equal(c2.get_connectome_meta().get_name(), 'Load & Save connectome')
    assert_equal(c2.get_connectome_meta().get_generator(), 'cfflib')
    assert_equal(c2.get_connectome_meta().get_version(), '2.0')
    assert_equal(c2.get_connectome_network()[0].get_src(), 'CNetwork/graphml_net.graphml')
    assert_true(c2.get_connectome_network()[0].get_metadata_as_dict().has_key('nb'))
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CVolume
def test_cvolume_nifti1():

    c = connectome()
    
    # Check the default values
    v1 = CVolume()
    assert_equal(v1.get_name(), 'myvolume')
    assert_equal(v1.get_fileformat(), 'Nifti1')
    assert_equal(v1.get_metadata_as_dict(), {})
    
    # Check the specified values
    v2 = CVolume('Second volume', metadataDict={'m0':123})
    assert_equal(v2.get_name(), 'Second volume')
    assert_not_equal(v2.get_metadata_as_dict(), {})
    assert_true(v2.get_metadata_as_dict().has_key('m0'))
    assert_equal(v2.get_metadata_as_dict()['m0'], '123')
    
    # Check classmethod
    v = CVolume.create_from_nifti('CVolume', 'data/Volumes/T1.nii.gz')
    assert_equal(v.get_name(), 'CVolume')
    
    # Check changing the name
    v.set_name('My volume')
    assert_equal(v.get_name(), 'My volume')
    
    # Check the description
    v.set_description('My first CVolume')
    assert_equal(v.get_description(), 'My first CVolume')
    
    # Check updating the metadata
    v.update_metadata({'meta1':'only T1 scan of this patient'})
    assert_equal(v.get_metadata_as_dict()['meta1'], 'only T1 scan of this patient')
    
    # Check add to the connectome
    c.add_connectome_volume(v)
    assert_not_equal(c.get_connectome_volume(), [])
    assert_equal(len(c.get_connectome_volume()), 1)
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CTrack
def test_ctrack_trk():

    c = connectome()
    
    # Check default values
    t = CTrack()
    assert_equal(t.get_name(), 'mytrack')
    assert_equal(t.get_fileformat(), 'TrackVis')
    assert_equal(t.get_metadata_as_dict(), {})
    
    # Check the specified values
    t = CTrack('Spec tracks', metadataDict={'fib':1})
    assert_equal(t.get_name(), 'Spec tracks')
    assert_true(t.get_metadata_as_dict().has_key('fib'))
    assert_equal(t.get_metadata_as_dict()['fib'], '1')
    
    # Check the classmethod from trackvis
    t = CTrack.create_from_trackvis('my track', 'data/Tracks/fibers_transformed.trk')
    assert_equal(t.get_name(), 'my track')
    assert_equal(t.get_src(), 'CTrack/my_track.trk')

    # Check add to the connectome
    c.add_connectome_track(t)
    assert_not_equal(c.get_connectome_track(), [])
    assert_equal(len(c.get_connectome_track()), 1)
# ---------------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------------- #
# Test CTimeserie
def test_ctimeserie_hdf5():

    c = connectome()
    
    # Check default values
    t = CTimeserie()
    assert_equal(t.get_name(), 'mytimeserie')
    assert_equal(t.get_fileformat(), 'HDF5')
    assert_equal(t.get_metadata_as_dict(), {})
    
    # Check the specified values
    t = CTimeserie('Spec timeserie', metadataDict={'ts':'val'})
    assert_equal(t.get_name(), 'Spec timeserie')
    assert_true(t.get_metadata_as_dict().has_key('ts'))
    assert_equal(t.get_metadata_as_dict()['ts'], 'val')
    
    # Check classmethod from hdf5
    t = CTimeserie.create_from_hdf5('my timeserie', 'data/Timeseries/generatedseries.hdf5')
    assert_equal(t.get_name(), 'my timeserie')
    assert_equal(t.get_src(), 'CTimeserie/my_timeserie.h5')

    # Check add to the connectome
    c.add_connectome_timeserie(t)
    assert_not_equal(c.get_connectome_timeserie(), [])
    assert_equal(len(c.get_connectome_timeserie()), 1)
# ---------------------------------------------------------------------------------- #
   
    
# ---------------------------------------------------------------------------------- #
# Test CSurface
def test_csurface_gifti():

    c = connectome()
    
    # Check default values
    s = CSurface()
    assert_equal(s.get_name(), 'mysurface')
    assert_equal(s.get_fileformat(), 'Gifti')
    assert_equal(s.get_dtype(), 'label')
    assert_equal(s.get_metadata_as_dict(), {})
    
    # Check the specified values
    s = CSurface('Spec surface', metadataDict={'surf':'ace'})
    assert_equal(s.get_name(), 'Spec surface')
    assert_true(s.get_metadata_as_dict().has_key('surf'))
    assert_equal(s.get_metadata_as_dict()['surf'], 'ace')
    
    # Check classmethod from gifti
    s = CSurface.create_from_gifti('my surface', 'data/Surfaces/testsubject_labels.gii')
    assert_equal(s.get_name(), 'my surface')
    assert_equal(s.get_src(), 'CSurface/my_surface.gii')

    # Check add to the connectome
    c.add_connectome_surface(s)
    assert_not_equal(c.get_connectome_surface(), [])
    assert_equal(len(c.get_connectome_surface()), 1)
# ---------------------------------------------------------------------------------- #


# ================================================================================== #
   
