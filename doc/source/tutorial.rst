=============================================
How to use the Connectome File Format Library
=============================================

.. note:: Example connectome files are provided in the GitHub repository `cffdata <http://github.com/LTS5/cffdata>`_.

Import the library. Subsequently, we assume that this has been done::

	from cfflib import *
	
Load the dataset from the file system::

	a=load_from_meta_cml('example_dataset_01/meta.cml')
	
You can print all the loaded connectome objects::

	print a.get_all()

If you have a zipped file with ending .cff, you can load it as well with::

	a=load_from_cff('datasets/ds1/connectomefile.cff')

You can get the first network and load it like this::

	mynetwork = a.get_by_name('Network Lausanne83')[0]
	mynetwork.load()
	
The loaded network object accessible through the data attribute (a NetworkX object)::

	print mynetwork.data

You see that it is a NetworkX graph. You can modify it as you like.

After modification, you can store it, which stores it in the corresponding file that
this CNetwork was referenced to (relative path)::

	print mynetwork.src
	mynetwork.save()
	
Show other attributes::
	
	print mynetwork.name
	print mynetwork.dtype
	print mynetwork.description

To show the metadata attributes as dictionary::

  print mynetwork.get_metadata_as_dict()

You can save the currently loaded connectome file::

	save_to_cff('myconnectome.cff', a)
	
The same you can do for other connectome objects, if the corresponding Python libraries are installed correctly::

	# CVolume
	obj = a.get_by_name('Example Volume')
	obj.load()
	print obj.data

	# CSurface
	obj = a.get_by_name('Example Surface')
	obj.load()
	print obj.data

	# CTrack
	obj = a.get_by_name('Tractography')
	obj.load()
	# You do not want to display all fibers, just show the header
	print obj.data[1]

	# CTimeseries
	obj = a.get_by_name('Generated timeseries data')
	obj.load()
	print obj.data
		
	# CData
	obj = a.get_by_name('Arbitrary data file')
	obj.load()
	print obj.data
	
	# CScript
	obj = a.get_by_name('Analysis Script MMXXXIV')
	obj.load()
	print obj.data
	
	# CImagestack
	obj = a.get_by_name('FIB Rat Striatum')
	obj.load()
	print obj.data
	
