==============================================
Installation of Connectome File Format Library
==============================================

You can clone the library from github using git::

	git clone git@github.com:unidesigner/cfflib.git
	
And then do a install in the cloned folder::

  sudo python setup.py install
	
Be aware that for the successfull loading of different connectome objects, you need
to have the corresponding Python libraries installed. Here are the dependencies:

+------------+---------------------------+----------------------------------------+
| Library    | Used for                  | Supports file formats                  |
+============+===========================+========================================+
| NetworkX   | CNetwork                  | GraphML, GEXF                          |
+------------+---------------------------+----------------------------------------+
| Nibabel    | CVolume, CSurface, CTrack | Nifti1, Gifti, TrackVis                |
+------------+---------------------------+----------------------------------------+
| NumPy      | CData                     | NumPy                                  |
+------------+---------------------------+----------------------------------------+
| PyTables   | CTimeserie, CData         | HDF5                                   |
+------------+---------------------------+----------------------------------------+
	