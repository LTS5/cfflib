#!/usr/bin/env python
#
# Christophe Chenes
# 2010-10-29
#
# The tutorial source code
#

from cfflib import *

#----------------------------------------------------------------------#
# Create the connectome object
myConnectome = connectome()

# Check what's inside the object
myConnectome
myConnectome.get_all()
myConnectome.hasContent_()
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
# Create the metadata
myMetadata = CMetadata()
myMetadata.set_name('My first connectome')
myMetadata.set_author('Connectome Tutorial')
myMetadata.set_institution('EPFL')
myMetadata.set_creation_date('2010-10-26')
myMetadata.set_url('www.connectome.ch')
myMetadata.set_description('First connectome object created with the tutorial.')

# Add the metadata
myConnectome.set_connectome_meta(myMetadata)
#----------------------------------------------------------------------#

# Save the connectome to file
#----------------------------------------------------------------------#
save_to_meta_cml(myConnectome, 'meta.cml')#'/your/wanted/path/meta.cml')
save_to_cff(myConnectome, 'myconnectome.cff')#'/your/wanted/path/myconnectome.cff')
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
# Load from file
myConnectomeFromMeta = load_from_meta_cml('meta.cml')
myConnectomeFromCFF = load_from_cff('myconnectome.cff')
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
# Create and add a network
# Create a networkx graph
myNetworkx = nx.Graph()
myNetworkx.add_node(0)
myNetworkx.add_node(1)
myNetworkx.add_node(2)
myNetworkx.add_edge(0,1)
myNetworkx.add_edge(1,2)

# Create a CNetwork
myCNet = CNetwork('My First CNetwork')

# Set with the NetworkX graph
myCNet.set_with_nxgraph(myNetworkx)

# Add the network to the connectome object
myConnectome.add_connectome_network(myCNet)

# Try to get all
myConnectome.get_all()

# Modify the CNetwork through the connectome object
myConnectome.get_connectome_network()[0].set_description('A first CNetwork created with the tutorial')
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
# Add metadata to an object
#----------------------------------------------------------------------#
myCN = myConnectome.get_connectome_network()[0]
myCN.set_metadata({'sd':1234})

# Try to save again
save_to_meta_cml(myConnectome, 'meta2.cml')#'/your/wanted/path/meta.cml')




