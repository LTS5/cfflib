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
myConnectome = connectome('1st connectome')

# Check what's inside the object
myConnectome
myConnectome.get_all()
myConnectome.hasContent_()
myConnectome.print_summary()
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
# Create the connectome metadata
myMetadata = myConnectome.get_connectome_meta()
myMetadata.set_title('My first connectome')
myMetadata.set_species('Homo Sapiens')
myMetadata.set_creator('Connectome Tutorial')
myMetadata.set_email('yourname@epfl.ch')
myMetadata.set_created('2010-10-26')
myMetadata.set_modified('2011-02-24')
myMetadata.set_description('First connectome object created with the tutorial.')
#----------------------------------------------------------------------#

# Save the connectome to file
#----------------------------------------------------------------------#
save_to_meta_cml(myConnectome, 'meta.cml')#'/your/wanted/path/meta.cml')
save_to_cff(myConnectome, 'myconnectome.cff')#'/your/wanted/path/myconnectome.cff')
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
# Load from file
myConnectomeFromMeta = load('meta.cml')
myConnectomeFromCFF = load('myconnectome.cff')
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

# From a graphml file 
# way 1
my2ndCNetwork = CNetwork.create_from_graphml('My GraphML Network', 'network_res83.graphml')
myConnectome.add_connectome_network(my2ndCNetwork)

#way 2
myConnectome.add_connectome_network_from_graphml('My GraphML Network', 'network_res83.graphml')
#----------------------------------------------------------------------#

#----------------------------------------------------------------------#
# Add metadata to an object
#----------------------------------------------------------------------#
myCN = myConnectome.get_connectome_network()[0]
myCN.update_metadata({'sd':1234})
myCN.get_metadata_as_dict()

# Try to save again
save_to_meta_cml(myConnectome, 'meta2.cml')#'/your/wanted/path/meta.cml')
save_to_cff(myConnectome, 'myconnectome2.cff')


#----------------------------------------------------------------------#
# Add a  CVolume
#----------------------------------------------------------------------#
cv = CVolume.create_from_nifti('My first volume', 'T1.nii.gz') # Path to the nifti1 file
myConnectome.add_connectome_volume(cv)
cv.set_description('A first CVolume created with the cfflib tutorial')
cv.update_metadata({'meta1': 123})      
#----------------------------------------------------------------------#


