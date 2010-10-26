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

You can check what's inside this object::

    myConnectome.get_all()
    
this function return all connectome's objects mixed, for now the output is empty.

To check if your connectome is containing something you can also use::

    myConnectome.hasContent_()
            
here, the result should be false.

Add the metadata
================

Now we want to add some metadata to the connectome. So you have to create a CMetadata object::

    myMetadata = CMetadata()
    
you are now able to add a lot of informations to this object. For example the followings::

    myMetadata.set_author('Your Name')
    myMetadata.set_institution('Your institution')
    myMetadata.set_creation_date('2010-10-26')
    myMetadata.set_url('www.connectome.ch')
    
and many more.

Then, you must add your metadata to your connectome object. Do it like this::

    myConnectome.set_connectome_metadata(myMetadata)

Save to file
============

After these first creations, we want to get a look at the output file this object will produce. Begin by save the file to the CML format::

    save_to_meta_cml(myConnectome, '/your/wanted/path/meta.cml')
    
Open the created file. You can see there is a first tag nammed *connectome* which is your connectome object. Inside, you find your metadata surrounded by the *connectome-meta* tag.

