=============================================
How to use the Connectome File Format Library
=============================================

An example dataset is provided with the source distribution.

Import the library. Subsequently, we assume that this has been done::

	from cfflib import *
	
Load the dataset from the file system::

	a=load_from_meta_cml('datasets/ds2/meta.cml')
	
You can print all the loaded connectome objects::

	print a.get_all()

If you have a zipped file with ending .cff, you can load it as well with::

	a=load_from_cff('datasets/ds2/connectomefile.cff')
	

You can get the first network and load it like this::

	mynetwork = a.get_by_name('Network Lausanne83')[0]
	mynetwork.load()
	
The loaded network object stored on the content attribute::

	print mynetwork.content

You see that it is a NetworkX graph. You can modify it as you like.

After modification, you can store it, which stores it in the corresponding file that
this CNetwork was referenced to (relative path)::

	print mynetwork.src
	mynetwork.save()
	
Show other attributes::
	
	print mynetwork.name
	print mynetwork.dtype
	print mynetwork.description.valueOf_

You can save the currently loaded connectome file::

	save_to_cff('myconnectome.cff', a)
	
The same you can do for other connectome objects, if the corresponding Python libraries are installed correctly::

	# CVolume
	obj = a.get_by_name('T1-weighted single subject')[0]
	obj.load()
	print obj.content

	# CSurface
	obj = a.get_by_name('Individual surfaces')[0]
	obj.load()
	print obj.content

	# CTrack
	obj = a.get_by_name('Tractography')[0]
	obj.load()
	# You do not want to display all fibers, just show header
	print obj.content[1]

	# CTimeserie
	obj = a.get_by_name('Generated timeseries data')[0]
	obj.load()
	print obj.content
		
	# CData
	obj = a.get_by_name('Arbitrary data file')[0]
	obj.load()
	print obj.content
	
	# CScript
	obj = a.get_by_name('Analysis Script MMXXXIV')[0]
	obj.load()
	print obj.content
	
	# CImagestack
	obj = a.get_by_name('Planar anatomical segmentation')[0]
	obj.load()
	print obj.content
	
