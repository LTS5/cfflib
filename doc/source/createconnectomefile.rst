How to create a Connectome File
*******************************

This short tutorial will give you the basics in creating a new connectome file with the **cfflib 2.0**.

Create the connectome object
============================

First of all you need to import the library::

    from cfflib import *

Then your first command will be::

    myConnectome = connectome()
    
in order to have a connectome object. 

You can specify here a name for your connectome object (see the *connectome metadata* section for more details) when you create it ::
    
    myConnectome = connectome('1st connectome')

To get some informations about this new object you can try::

    myConnectome
    myConnectome.get_all()

The first line is just to show that you have a connectome object, the function ``get_all()`` return all connectome's objects mixed, for now its output is empty.

You can also get a summary of the content of you connectome object with::

    myConnectome.print_summary()
    
which will return some metadata and statistics about this connectome object and a short description of each CObject in it.

The connectome metadata
=======================

The connectome's metadata are required by the connectome object. The initialisation of a connectome object will create a connectome metadata object with the default values of required attributes - unless you specified a name - but you can modifiy it to get your specific CMetadata object ::

    myMetadata = myConnectome.get_connectome_meta()
    
you are able to add a lot of informations to this object but three are required:

    - *title* : the unique name of your connectome object, by default **myconnectome**
    
    - *version* : the version of the Connectome Markup Language used, by default **2.0**
    
    - *generator* : the generator of the connectome object, by default **cfflib**

For example the followings::

    myMetadata.set_title('My first connectome')
    myMetadata.set_species('Homo Sapiens')
    myMetadata.set_creator('Connectome Tutorial')
    myMetadata.set_email('yourname@epfl.ch')
    myMetadata.set_created('2010-10-26')
    myMetadata.set_modified('2011-02-24')
    myMetadata.set_description('First connectome object created with the tutorial.')

Save to file
============

After these first creations, we want to get a look at the output file this object will produce. There are two methods to save your object to file::

    save_to_cff(myConnectome, '/your/wanted/path/myConnectome.cff')
    save_to_meta_cml(myConnectome, '/your/wanted/path/meta.cml')

The first one will save the connectome object to a compressed CFF file and the second one will just save in a CML file.

Open the created CML file. You can see a first tag named *connectome* which is your connectome object. Inside, you should find your connectome metadata surrounded by the *connectome-meta* tag.

More precisely, your meta.cml file should look like this one::

    <?xml version="1.0" encoding="UTF-8"?>
    <cml:connectome xmlns="http://www.connectomics.org/cff-2"
        xmlns:cml="http://www.connectomics.org/cff-2"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dcterms="http://purl.org/dc/terms/"
        xsi:schemaLocation="http://www.connectomics.org/cff-2 connectome.xsd">
        <cml:connectome-meta version="2.0">
            <dcterms:title>My first connectome</dcterms:title>
            <dcterms:creator>Connectome Tutorial</dcterms:creator>
            <dcterms:created>2010-10-26</dcterms:created>
            <dcterms:modified>2011-02-24</dcterms:modified>
            <dcterms:description>First connectome object created with the tutorial.</dcterms:description>
            <cml:generator>cfflib</cml:generator>
            <cml:email>yourname@epfl.ch</cml:email>
        </cml:connectome-meta>
    </cml:connectome>

Load from file
==============

To retrieve your connectome object you can load from the previous saved file. Here again, there are two methods to do it, one for the CFF file and one for the CML::
    
    myConnectomeFromMeta = load('/your/wanted/path/meta.cml')
    myConnectomeFromCFF = load('/your/wanted/path/myconnectome.cff')

Add a network
=============

To add a network to your connectome object, you have to create a **CNetwork** object. This object has three required parameters:

    - *name* : the unique name of this network, **mynetwork** by default
    
    - *fileformat* : the fileformat of the network, which can be :
    
        - **GraphML**, by default
        
        - *GEXF*
        
        - *NXGPickle*
        
        - *Other*
    
    - *dtype* : the data type of the network, which can be : 
    
        - **AttributeNetwork**, by default
        
        - *DynamicNetwork*
        
        - *HierarchicalNetwork*
        
        - *Other*

You can create a new CNetwork like this::

    myCNetwork = CNetwork('My First CNetwork')  
    
On the exemple above, the CNetwork is created with a specified name and the default values for the two others required parameters. You can specified some other attributes:

    - *src* : the source file of the network
    
    - *description* : a description of the network
    
    - *metadata* : some meta data of the network 

From a NetworkX object
----------------------

Now, assume that you want to add an existing NetworkX graph to your CNetwork object. First, we'll create a basic NetworkX graph::

    import networkx as nx
    myNetworkx = nx.Graph()
    myNetworkx.add_node(0)
    myNetworkx.add_node(1)
    myNetworkx.add_node(2)
    myNetworkx.add_edge(0,1)
    myNetworkx.add_edge(1,2)
    
Then we can set our CNetwork object with this graph::

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

    myConnectome.get_connectome_network()[0].set_description('A first CNetwork created with the tutorial')

for example, this function will add a description to this CNetwork.

From a GraphML file
-------------------

It is possible to create a CNetwork from a GraphML file. There are two ways to do it:

    1. first create a CNetwork from the GraphML and then add it to the connectome::
    
        my2ndCNetwork = CNetwork.create_from_graphml('My GraphML network', 'your/path/to/graph.graphml')
        myConnectome.add_connectome_network(my2ndCNetwork)

    2. directly add a CNetwork based on the GraphML file from the connectome::

        myConnectome.add_connectome_network_from_graphml('My GraphML network', 'your/path/to/graph.graphml')        

After you used one of the methods above, if you ask again the connectome for its objects::
    
    myConnectome.get_all()
    
You should get two CNetwork.

Add metadata to a CObject
=========================

We already saw that we can add some metadata to the connectome object with CMetadata. In fact, it is possible to add some metadata to any CObject, for example to a CNetwork object. That's what we're going to do in this section with the **Metadata** object. 

First, we need a reference on the wanted CObject, here the previous CNetwork object, to make things easier::

    myCN = myConnectome.get_connectome_network()[0]

We can add some metadata to this object by using a dictionary structure::
    
    myCN.update_metadata({'sd':1234})
    
this command will create the Metadata object and add the key *sd* with the value *1234*. You can use a dictionary of the length you want.

You can try to get back this dictionary with ::

    myCN.get_metadata_as_dict()

At this point, we can try to save again our connectome to check the CML::

    save_to_meta_cml(myConnectome, '/your/wanted/path/meta.cml')  
    
The output file should look like::

    <?xml version="1.0" encoding="UTF-8"?>
    <cml:connectome xmlns="http://www.connectomics.org/cff-2"
        xmlns:cml="http://www.connectomics.org/cff-2"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dcterms="http://purl.org/dc/terms/"
        xsi:schemaLocation="http://www.connectomics.org/cff-2 connectome.xsd">
        <cml:connectome-meta version="2.0">
            <dcterms:title>My first connectome</dcterms:title>
            <dcterms:creator>Connectome Tutorial</dcterms:creator>
            <dcterms:created>2010-10-26</dcterms:created>
            <dcterms:modified>2011-02-24</dcterms:modified>
            <dcterms:description>First connectome object created with the tutorial.</dcterms:description>
            <cml:generator>cfflib</cml:generator>
            <cml:email>yourname@epfl.ch</cml:email>
        </cml:connectome-meta>
        <cml:connectome-network src="CNetwork/my_first_cnetwork.gpickle" dtype="AttributeNetwork" name="My First CNetwork" fileformat="NXGPickle">
            <cml:metadata>
                <cml:tag key="sd">1234</cml:tag>
            </cml:metadata>
            <cml:description>A first CNetwork created with the tutorial</cml:description>
        </cml:connectome-network>
        <cml:connectome-network src="CNetwork/my_graphml_network.graphml" dtype="AttributeNetwork" name="My GraphML Network" fileformat="GraphML"/>
    </cml:connectome>
    
Now you can see there are two new blocks with the tag *connectome-network* which are the added CNetwork with the given attributes. The first one is the CNetwork added from the NetworkX object and contains the metadata and the description. The second one is the one created from the GraphML file.
    
Add a volume
============

To add a volume to your connectome object, you have to use a CVolume object. This object has the following parameters:

    - *name* : **'myvolume'**,
            the unique name of the volume
    - *dtype* : string, optional,
            the data type of the volume. It can be: 'Segmentation', 'T1-weighted', 'T2-weighted', 'PD-weighted', 'fMRI', 'MD', 'FA', 'LD', 'TD', 'FLAIR', 'MRA' or 'MRS depending on your dataset.
    - *fileformat* : **'Nifti1'**,
            the fileformat of the volume. Only 'Nifti1' is supported, its compressed version '.nii.gz' too.
    - *src* : string, optional,
            the source file of the volume
    - *description* : string, optional,
	       A description according to the format attribute syntax.
    - *metadataDict* : dictionary, optional,
            More metadata relative to the volume as a dictionary

First create a CVolume from a Nifti file and then add it to the connectome object::
        
    cv = CVolume.create_from_nifti('My first volume', 'T1.nii.gz') # Path to the nifti1 file
    myConnectome.add_connectome_volume(cv)
       
Again, you can add some more informations with the description and the metadata::

    cv.set_description('A first CVolume created with the cfflib tutorial')
    cv.update_metadata({'meta1': 123})        
        
        
Other objects
=============

You can display the docstring of the other connectome objects to see how to create, manipulate and store them.
The procedures are very similar. If you need more working code to get you started, you can look into the
`tests <http://github.com/LTS5/cfflib/tree/master/cfflib/tests>`_.

.. note :: Example connectome files are provided in the GitHub repository `cffdata <http://github.com/LTS5/cffdata>`_.