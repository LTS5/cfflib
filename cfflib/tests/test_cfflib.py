

def test_savecff():
    import cfflib
    c=cfflib.connectome()
    import cfflib as cc
    c.connectome_meta=cc.CMetadata('test')
    net=cc.CNetwork('test')
    net.metadata
    net.metadata = cc.Metadata()
    net.set_metadata({'sd':1234})
    c.add_connectome_network(net)
    import networkx as nx
    net.set_with_nxgraph('tet', nx.Graph())
    cc.save_to_cff(c,'test.cff')

