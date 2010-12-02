How to create a Connectome File
*******************************

This short tutorial will give you the basics in creating a new connectome file with the **cfflib**.

Create the connectome object
============================

First of all you need to import the library::

    from cfflib import *

Then your first command will be::

    myConnectome = connectome()
    
in order to have a connectome object. 

.. note::
    
    The method ``connectome()`` can take as argument each possible object the connectome can handle. For example, you can create a new connectome with an existing network. But, we will see these possible objects later.

To get some informations about this new object you can try::

    myConnectome
    myConnectome.get_all()
    myConnectome.hasContent_()

The first line is just to show that you have a connectome object, the function ``get_all()`` return all connectome's objects mixed, for now its output is empty, and the function ``hasContent_()`` tell you if your object contains something, its output should be ``False``.

Add the connectome metadata
===========================

The connectome's metadata is required. So you have to create a CMetadata object with a name::

    myMetadata = CMetadata(name)
    
you are now able to add a lot of informations to this object but three are required:

    - *name* : the unique name of your connectome object
    
    - *version* : the version of the cfflib, by default **2.0**
    
    - *generator* : the generator of the connectome object, by default **cfflib**

For example the followings::

    myMetadata.set_author('Connectome Tutorial')
    myMetadata.set_institution('EPFL')
    myMetadata.set_creation_date('2010-10-26')
    myMetadata.set_url('www.connectome.ch')
    myMetadata.set_description('First connectome object created with the tutorial.')
    
Then, you must add your metadata to your connectome object. Do it like this::

    myConnectome.set_connectome_meta(myMetadata)

Save to file
============

After these first creations, we want to get a look at the output file this object will produce. There are two methods to save your object to file::

    save_to_cff(myConnectome, '/your/wanted/path/myConnectome.cff')
    save_to_meta_cml(myConnectome, '/your/wanted/path/meta.cml')

The first one will save the connectome object to a compressed CFF file and the second one will just save in a CML file.

Open the created CML file. You can see a first tag nammed *connectome* which is your connectome object. Inside, you should find your connectome metadata surrounded by the *connectome-meta* tag.

More precisely, your CML file should look like this one::

    <?xml version="1.0" encoding="UTF-8"?>
    <connectome xmlns="http://www.connectomics.org/2010/Connectome/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.connectomics.org/2010/Connectome/xmlns connectome.xsd">
        <connectome-meta version="2.0">
            <generator>cfflib</generator>
            <author>Connectome Tutorial</author>
            <institution>EPFL</institution>
            <creation-date>2010-10-26</creation-date>
            <name>my_first_connectome</name>
            <url>www.connectome.ch</url>
            <description format="plaintext">First connectome object created with the tutorial.</description>
        </connectome-meta>
    </connectome>

Load from file
==============

To retrieve your connectome object you can load from the previous saved file. Here again, there are two methods to do it, one for the CFF file and one for the CML::
    
    myConnectomeFromMeta = load_from_meta_cml('/your/wanted/path/meta.cml')
    myConnectomeFromCFF = load_from_cff('/your/wanted/path/myconnectome.cff')

Add a network
=============

To add a network to you connectome object, you have to create a CNetwork object. This object has three required parameters:

    - *name* : the unique name of this network
    
    - *fileformat* : the fileformat of the network, by default **GraphML**
    
    - *dtype* : the data type of the network, by default **AttributeNetwork**

You can create a new CNetwork like this::

    myCNetwork = CNetwork('My First CNetwork')  
    
On the exemple above, the CNetwork is created with a specified name and the default values for the two others required parameters. You can specified some other attributes:

    - *src* : the source file of the network
    
    - *description* : a description of the network
    
    - *metadata* : some meta data of the network 

Now, assume that you want to add a networkx graph to your CNetwork object. First, we'll create a basic networkx::

    import networkx as nx
    myNetworkx = nx.Graph()
    myNetworkx.add_node(0)
    myNetworkx.add_node(1)
    myNetworkx.add_node(2)
    myNetworkx.add_edge(0,1)
    myNetworkx.add_edge(1,2)
    
Then we can add this simple graph to our CNetwork object::

    myCNetwork.set_with_nxgraph(myNetworkx)
    
Finally, we add the CNetwork to our connectome object::

    myConnectome.add_connectome_network(myCNetwork)

You can add a CNetwork object based on a NetworkX graph directly from the connectome with this function::

    myConnectome.add_connectome_network_from_nxgraph(myNetworkx, 'My first CNetwork')
    
.. warning::
    When you add a CNetwork, but it's true for any CObject, to your connectome, the name of your object is checked and has to be unique. If not, an error will be return and the CObject will not be added to the connectome.

Now, you can try again *myConnectome.get_all()* function, it should return something like::
    
    [<cfflib.cfflib_modified.CNetwork object at 0x34364d0>]
    
You can access and modifiy this CNetwork object::

    myConnectome.get_connectome_network()[0].set_name('A CNetwork')

for example, this function will modify the name to "*A CNetwork*".


Add metadata to an object
=========================

We already saw that we can add some metadata to the connectome object with CMetadata. In fact, it's possible to add some metadata to any CObject, for example to a CNetwork object. That's what we're going to do in this section with the Metadata object. 

First we add some Metadata to our first CNetwork::

    myCN1 = myConnectome.get_connectome_network()[0]
    myCN1.metadata = Metadata()
    
Now, we have a reference on our first CNetwork *myCN1* and it contains a Metadata object.

We can create a data and add it to the metadata of our CNetwork::
    
    data = data()
    data.set_key('Resolution')
    data.set_value('83')
    myCN1.metadata.set_data(data)
    
At this point, we can try to save again our connectome to check the CML::

    save_to_meta_cml(myConnectome, '/your/wanted/path/meta.cml')  
    
The output file should look like::

    <?xml version="1.0" encoding="UTF-8"?>
    <connectome xmlns="http://www.connectomics.org/2010/Connectome/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.connectomics.org/2010/Connectome/xmlns connectome.xsd">
        <connectome-meta version="0.0.1">
            <author>Your Name</author>
            <institution>Your Institution</institution>
            <creation-date>2010-10-26</creation-date>
            <url>www.connectome.ch</url>
            <description format="plaintext">First connectome object created with the tutorial.</description>
        </connectome-meta>
        <connectome-network dtype="data" name="my1stCNetwork" fileformat="GraphML">
            <metadata>
                <data key="Resolution">83</data>
            </metadata>
            <description format="plaintext">This is my first CNetwork created for the tutorial</description>
        </connectome-network>
    </connectome>
    
    
    
    


