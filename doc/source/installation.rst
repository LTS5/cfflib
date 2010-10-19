==============================================
Installation of Connectome File Format Library
==============================================

You can install the library using easy_install::

	pip install cfflib
	
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
	