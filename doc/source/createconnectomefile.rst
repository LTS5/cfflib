How to create a Connectome File
*******************************

This short tutorial will give you the basics in creating a new connectome file with the **cfflib**.

Create the connectome object
============================

First of all you need to import the library::

    from cfflib import *

Then your first command will be::

    myConnectome = connectome()
    
in order to have a connectome object. The method ``connectome()`` can take as argument each possible object the connectome can handle. For example, you can create a new connectome with an existing network. But, we will see these possible objects later.

To get some informations about this new object you can try::

    myConnectome
    myConnectome.get_all()
    myConnectome.hasContent_()

The first line is just to show that you have a connectome object, the function ``get_all()`` return all connectome's objects mixed, for now its output is empty, and the function ``hasContent_()`` tell you if your object contains something, its output should be ``False``.

Add the metadata
================

Now we want to add some metadata to the connectome. So you have to create a CMetadata object::

    myMetadata = CMetadata()
    
you are now able to add a lot of informations to this object. For example the followings::

    myMetadata.set_author('Your Name')
    myMetadata.set_institution('Your Institution')
    myMetadata.set_creation_date('2010-10-26')
    myMetadata.set_url('www.connectome.ch')
    myMetadata.set_version('0.0.1')
    myMetadata.set_description(description('plaintext','First connectome object created with the tutorial.'))
    
and many more.

Then, you must add your metadata to your connectome object. Do it like this::

    myConnectome.set_connectome_meta(myMetadata)

Save to file
============

After these first creations, we want to get a look at the output file this object will produce. Begin by save the file to the CML format::

    save_to_meta_cml(myConnectome, '/your/wanted/path/meta.cml')
    
Open the created file. You can see a first tag nammed *connectome* which is your connectome object. Inside, you find your metadata surrounded by the *connectome-meta* tag.

More precisely, your file should look like this one::

    <?xml version="1.0" encoding="UTF-8"?>
    <connectome xmlns="http://www.connectomics.org/2010/Connectome/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.connectomics.org/2010/Connectome/xmlns connectome.xsd">
        <connectome-meta version="0.0.1">
            <author>Your Name</author>
            <institution>Your Institution</institution>
            <creation-date>2010-10-26</creation-date>
            <url>www.connectome.ch</url>
            <description format="plaintext">First connectome object created with the tutorial.</description>
        </connectome-meta>
    </connectome>

Load from file
==============



