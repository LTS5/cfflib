==============================================
Installation of Connectome File Format Library
==============================================

.. note:: Very soon, a release version will be provided through `NeuroDebian <http://neuro.debian.net>`_

For development, you can clone or fork the library from GitHub::

	git clone git@github.com:LTS5/cfflib.git
	
And then do a install in the cloned folder::

  sudo python setup.py install
	
Be aware that for the successfull loading of different connectome objects, you need
to have the corresponding Python libraries installed. Here are the dependencies:

* NetworkX >= 1.4 (GraphML, NXGPickle, GEXF)
* Nibabel >= 1.1.0 (Nifti1, Gifti, TrackVis)
* NumPy (NumPy arrays)
* PyTables (optional, HDF5)
