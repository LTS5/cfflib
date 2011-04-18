.. Connectome File Format Library documentation master file, created by
   sphinx-quickstart on Tue Oct 19 09:53:08 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Connectome File Format Library
==============================

The Connectome File Format Library (cfflib) is a pure Python library for multi-modal connectome data and metadata management and integration,
based on the specification of the Connectome File Format (CFF). The cfflib provides a high-level interface to many common data formats
by using `Nibabel <http://nipy.org>`_ for basic neuroimaging data format IO, and NumPy and the Python standard-library for other formats. The Connectome
File Format provides means to store arbitrary metadata as tags and in structured form for any so-called connectome object. Connectome objects
encapsulate the various data types as they occur in connectome research.

* CMetadata: Connectome Markup Language (XML)
* CNetwork: Networks, Connectomes (GraphML, GEXF, NXGPickle)
* CSurface: Surface data (Gifti)
* CVolume: Volumetric data (Nifti1, Nifti1GZ)
* CTrack: Fiber track data (TrackVis)
* CTimeserie: Timeseries data (HDF5, NumPy)
* CData: Other data, like tables (HDF5, NumPy, XML, JSON, CSV, Pickle)
* CScript: Processing and analysis scripts (ASCII, UTF-8, UTF-16)
* CImagestack: Imagestacks (PNG, JPG, TIFF, SVG)

The Connectome Markup Language was developed without knowing about the existence
of the `"Chemical Markup Language" <http://xml-cml.org/index.php>`_. Both markup
languages using the same abbreviation *CML* to denote their namespace.

Contents:

.. toctree::
   :maxdepth: 2
   
   installation
   tutorial
   createconnectomefile

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
