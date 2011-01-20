#!/usr/bin/env python

#
# Generated Sun Aug 29 11:58:22 2010 by generateDS.py version 2.1a.
#

### My Imports

import warnings
from util import *

###

import sys
from string import lower as str_lower

import cff as supermod

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#

class connectome(supermod.connectome):
    """The connectome object is the main object of this format. It contains CMetadata, it can contain some CData, CNetwork, CScript, CSurface, CTimeserie, CTrack and CVolume. It is possible to store it to a simple CML file or to a complete compressed CFF file with all sources."""
    
    def __init__(self, name='myconnectome', connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeserie=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        """Create a new connectome object.
        
        Parameters
        ----------
        name: 'myconnectome',
            the name of this connectome object
        
        See also
        --------
        CMetadata, CNetwork, CSurface, CVolume, CTrack, CTimeserie, CData, CScript and CImagestack
    
        """
        super(connectome, self).__init__(connectome_meta, connectome_network, connectome_surface, connectome_volume, connectome_track, connectome_timeserie, connectome_data, connectome_script, connectome_imagestack, )
        
        # add parent reference to all children
        self._update_parent_reference()
        
        # add some useful attributes to the save functions
        self.iszip = False
        
        # Default CMetadata
        if connectome_meta is None:
            self.connectome_meta = CMetadata(name)
        
    def get_all(self):
        """Return all connectome objects mixed as a list.
                    
        Examples
        --------
        >> myConnectome.get_all()
            [<cfflib.cfflib_modified.CNetwork object at 0x2c46b10>,
            <cfflib.cfflib_modified.CNetwork object at 0x2ca5490>]
            
        See also
        --------
        connectome, get_by_name
    
        """        
        return self.connectome_network + self.connectome_surface + \
                self.connectome_volume + self.connectome_track + \
                self.connectome_timeserie + self.connectome_data + \
                self.connectome_script + self.connectome_imagestack
    
    def get_by_name(self, name):
        """Return the list of connectome object(s) that have the given name.
        
        Parameters
        ----------
        name : string
            name of the wanted object(s)
            
        Examples
        --------
        >>> myConnectome.get_by_name('my first network')
            [<cfflib.cfflib_modified.CNetwork object at 0x2c46b10>]
            
        See also
        --------
        connectome, get_all, get_normed_name
    
        """   
        n = self.get_normed_name(name) 
        print n     
        all_cobj = self.get_all() 
        obj_list = []
        for ele in all_cobj:
            print self.get_normed_name(ele.name)
            if n ==self.get_normed_name(ele.name):
                obj_list.append(ele)
        return obj_list            

    def check_file_in_cff(self):
        """Checks if the files described in the meta.cml are contained in the connectome zip file."""  
        
        if not self.iszip:
            return
        
        all_cobj = self.get_all()
        nlist = self._zipfile.namelist()
        
        for ele in all_cobj:
            
            if not ele.src in nlist:
                msg = "Element with name %s and source path %s is not contained in the connectome file." % (ele.name, ele.src)
                raise Exception(msg)
            
    def check_names_unique(self):
        """Checks whether the names are unique."""  
        all_cobj = self.get_all()
        namelist = []
        for ele in all_cobj:
            namelist.append(ele.name)
        
        # check for non uniqueness
        while len(namelist) > 0:
            e = namelist.pop()
            if e in namelist:
                msg = "Element '%s' has a non unique name! Please change the name to make it unique." % e
                raise Exception(msg)
    
    def is_name_unique(self, name):
        """Check if the given name is unique.
        
        Parameters
        ----------
        name : string,
            the name to check if it is unique
            
        See also
        --------
        check_names_unique, get_normed_name, connectome
        """
        n = self.get_normed_name(name)
        all_cobj = self.get_all()
        namelist = []
        for ele in all_cobj:
            namelist.append(self.get_normed_name(ele.name))
        if n in namelist:
            return False
        else:
            return True
    
    def get_unique_cff_name(self):
        """Return a unique connectome file name"""
        return self.get_normed_name(self.get_connectome_meta().name)
        
    def get_normed_name(self, name):
        """Return a normed name, without space and in lower case
        
        Parameters
        ----------
        name : string,
            the name to be normed
            
        See also
        --------
        connectome
    
        """
        n = name.lower()
        n = n.replace(' ', '_')
        return n

    def _update_parent_reference(self):
        """Updates the parent reference to the connectome file super-object"""

        all_cobj = self.get_all() 
        
        for ele in all_cobj:
            ele.parent_cfile = self

    def to_xml(self):
        from StringIO import StringIO
        re = StringIO()
        re.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        ns = """xmlns="http://www.connectomics.org/2010/Connectome/xmlns"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.connectomics.org/2010/Connectome/xmlns connectome.xsd" """
        self.export(re, 0, name_= "connectome", namespacedef_=ns)
        re.seek(0)
        return re.read()
    
    def close_all(self, save = False):
        """ Close all currently loaded elements, thereby releasing occupied memory 
        
        Parameters
        ----------
        save : bool,
            Save the content before closing.
            
        """

        all_cobj = self.get_all() 
        
        for ele in all_cobj:
            
            if hasattr(ele, 'data') and hasattr(ele, 'tmpsrc') and op.exists(ele.tmpsrc):
                
                if save:
                    ele.save()
                
                # remove .data and .tmpsrc
                print "Will not remove file %s from file system" % ele.tmpsrc
                print "Remove .data attribute"
                del ele.data
                print "Remove .tmpsrc attribute"
                del ele.tmpsrc
    
    # CMetadata setter
    def set_connectome_meta(self, cmeta):
        """Set the connectome metadata object for this connectome object
        
        Parameters
        ----------
        cmeta : CMetadata,
            the connectome metadata to add to the connectome object
            
        See also
        --------
        CMetadata, connectome, is_name_unique  
        """
                
        # Check if the name is set     
        if cmeta.name is None or cmeta.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(cmeta.name):
            raise Exception('The name is not unique.')
            
        self.connectome_meta = cmeta
    
    # CNetwork
    def add_connectome_network_from_nxgraph(self, name, nxGraph, dtype='AttributeNetwork', fileformat='NXGPickle'):
        """Add a new CNetwork from the given NetworkX graph object to the connectome.
        
        Parameters
        ----------
        name : string,
            the unique name for the NetworkX graph to add to the connectome object
        nxGraph : NetworkX,
            the NetworkX graph object
        dtype : 'AttributeNetwork',
            the data type of this CNetwork
        fileformat : 'NXGPickle',
            the fileformat of the file of this CNetwork
                    
        Examples
        --------
        >>> myConnectome.add_connectome_network_from_nx(myNXGraph,'nxG1')
            
        See also
        --------
        NetworkX, CNetwork.set_with_nxgraph, CNetwork, connectome.add_connectome_network, connectome   
            
        """
        
        # Check if the name is unique
        if not self.is_name_unique(name):
            raise Exception('The name is not unique.')
            
        n = CNetwork(name)
        n.set_with_nxgraph(nxGraph, dtype, fileformat)
        self.add_connectome_network(n)
    
    def add_connectome_network_from_graphml(self, name, graphML):
        """Add a new CNetwork from the given GraphML file to the connectome object.
        
        Parameters
        ----------
        name : string,
            the unique name of the new CNetwork
        graphML : GraphML file,
            the filename of the GraphML to add to the connectome.
                    
        Examples
        --------
        >>> myConnectome.add_connectome_network_from_ml('myGraphML.graphml')
            
        See also
        --------
        GraphML, CNetwork.create_from_graphml, CNetwork, connectome.add_connectome_network, connectome
            
        """
        
        # Check if the name is unique
        if not self.is_name_unique(name):
            raise Exception('The name is not unique.')
        
        n = CNetwork.create_from_graphml(name, graphML)
        self.add_connectome_network(n)      
    
    def add_connectome_network(self, cnet):
        """Add the given CNetwork to the connectome object.
        
        Parameters
        ----------
        cnet : CNetwork,
            the connectome network to add to the connectome, the CNetwork name have to be unique.
            
        See also
        --------
        CNetwork, connectome
            
        """
              
        # Check if the name is set     
        if cnet.name is None or cnet.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(cnet.name):
            raise Exception('The name is not unique.')
            
        self.connectome_network.append(cnet)
        
    # CVolume
    def add_connectome_volume(self, cvol):
        """Add the given CVolume to the connectome object.
        
        Parameters
        ----------
        cnet : CVolume,
            the connectome volume to add to the connectome, the CVolume name have to be unique.
            
        See also
        --------
        CVolume, connectome
            
        """
              
        # Check if the name is set     
        if cvol.name is None or cvol.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(cvol.name):
            raise Exception('The name is not unique.')
            
        self.connectome_volume.append(cvol)
        
    # CSurface
    def add_connectome_surface(self, csurf):
        """Add the given CSurface to the connectome object.
        
        Parameters
        ----------
        csurf : CSurface,
            the connectome surface to add to the connectome, the CSurface name have to be unique.
            
        See also
        --------
        CSurface, connectome
            
        """
              
        # Check if the name is set     
        if csurf.name is None or csurf.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(csurf.name):
            raise Exception('The name is not unique.')
        
        self.connectome_surface.append(csurf)
    
    # CTrack
    def add_connectome_track(self, ctrack):
        """Add the given CTrack to the connectome object.
        
        Parameters
        ----------
        ctrack : CTrack,
            the connectome surface to add to the connectome, the CTrack name have to be unique.
            
        See also
        --------
        CTrack, connectome
            
        """
              
        # Check if the name is set     
        if ctrack.name is None or ctrack.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(ctrack.name):
            raise Exception('The name is not unique.')
        
        self.connectome_track.append(ctrack)
    
    # CTimeserie
    def add_connectome_timeserie(self, cts):
        """Add the given CTimeserie to the connectome object.
        
        Parameters
        ----------
        cts : CTimeserie,
            the connectome timeserie to add to the connectome, the CTimeserie name have to be unique.
            
        See also
        --------
        CTimeserie, connectome
            
        """
              
        # Check if the name is set     
        if cts.name is None or cts.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(cts.name):
            raise Exception('The name is not unique.')
        
        self.connectome_timeserie.append(cts)
    
    # CScript
    def add_connectome_script(self, cts):
        """Add the given CScript to the connectome object.
        
        Parameters
        ----------
        cscr : CScript,
            the connectome script to add to the connectome, the CScript name have to be unique.
            
        See also
        --------
        CScript, connectome
            
        """
              
        # Check if the name is set     
        if cscr.name is None or cscr.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(cscr.name):
            raise Exception('The name is not unique.')
        
        self.connectome_script.append(cscr)
    
supermod.connectome.subclass = connectome
# end class connectome


class CMetadata(supermod.CMetadata):
    """Specific metadata to the connectome object. The name is the name of the connectome. The version and the generator are required and are defined by default."""
    
    def __init__(self, name='myconnectome', version='2.0', generator='cfflib', author=None, institution=None, creation_date=None, modification_date=None, species=None, legal_notice=None, reference=None, email=None, url=None, description=None, metadata=None):
        """Creates a connectome metadata object, specific metadata to the connectome object.
        
        Parameters
        ----------
        name : 'myconnectome',
            the name of this connectome object 
        version : '2.0',  
            version of the cfflib
        generator : 'cfflib',
            generator of this connectome
        author : string, optional ,
            the author name
        institution : string, optional,
            the author institution
        creation_date : string, optional,
            the creation date of this connectome
        modification_date : string, optional,
            the date of important modification to this connectome object
        species : string, optional,
            the species of the subject
        legal_notice : string, optional,
            legal information
        reference : string, optional,
            reference
        email : string, optional,
            an email of reference (author one)
        url : string, optional,
            a related url
        description : string, optional,
            a short text description of the connectome
        metadata : Metadata, optional,
            some more metadata informations
            
        See also
        --------
        Metadata, connectome  
        """
        super(CMetadata, self).__init__(version, generator, author, institution, creation_date, modification_date, name, species, legal_notice, reference, email, url, description, metadata, )

        self.name = name
        
supermod.CMetadata.subclass = CMetadata
# end class CMetadata


class description(supermod.description):
    def __init__(self, format=None, value=None):
        super(description, self).__init__(format, value, )
supermod.description.subclass = description
# end class description


class CBaseClass(object):

    def load(self, custom_loader = None):
        """ Load the element. The loaded object is stored in the data attribute.
        
        Parameters
        ----------
        custom_loader : function, default: None
            Custom loader function that takes connectome element as
            its first argument.
            
        See Also
        --------
        See cfflib.util.load_data for example. """
        
        if not custom_loader is None:
            self.data = custom_loader(self)
        else:
            self.data = load_data(self)
    
    def save(self):
        """ Save a loaded connectome object to a temporary file, return the path """
        rval = save_data(self)
        if not rval == '':
            self.tmpsrc = rval
            print "Updated storage path of file: %s" % rval
        else:
            raise Exception('There is nothing to save.')

    # Metadata
    def get_metadata_as_dict(self): 
        """Get the metadata as a dictionary"""
        return self.metadata.get_as_dictionary()
    def update_metadata(self, metadata): 
        """Set the metadata with a dictionary"""
        if self.metadata is None:
            self.metadata = Metadata()
        self.metadata.set_with_dictionary(metadata)
        
        
    def get_type(self):
        """ Returns the class name """
        pass
        # XXX: as single string 
    

class CNetwork(supermod.CNetwork, CBaseClass):
    """A connectome network object"""
    
    def __init__(self, name='mynetwork', dtype='AttributeNetwork', fileformat='GraphML', src=None, description=None, metadataDict=None):
        """Create a new connectome network object.
        
        Parameters
        ----------
        name : 'mynetwork',
            the network unique name
        dtype : 'AttributeNetwork',
            the data type of the network. It can be: "AttributeNetwork", "DynamicNetwork", "HierarchicalNetwork" or "Other".
        fileformat : 'GraphML',
            the fileformat of the network. It can be: "GEXF", "GraphML", "NXGPickle" or "Other".
        src : string, optional,
            the source file of the network
        description : plaintext, optional,
            a text description of the CNetwork
        metadataDict : dictionary, optional,
            some metadata to the network as a dictionary
            
        See also
        --------
        Metadata, connectome
    
        """
        super(CNetwork, self).__init__(src, dtype, name, fileformat, None, description, )
        if metadataDict is not None:
            self.update_metadata(metadataDict)
        else:
            self.metadata = Metadata()
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.fileformat == 'GraphML':
            fend = '.graphml'
        elif self.fileformat == 'GEXF':
            fend = '.gexf'
        elif self.fileformat == 'NXGPickle':
            fend = '.gpickle'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CNetwork', self.name + fend)
    
    @classmethod
    def create_from_graphml(cls, name, ml_filename):
        """ Return a CNetwork object from a given ml_filename pointing to
        a GraphML file in your file system
        
        Parameters
        ----------
        name : string,
            the unique name of the CNetwork
        ml_filename : string,
            the filename of the GraphML to load
        
        Returns
        -------
        cnet : CNetwork
        
        """
        
        # Check if the GraphML file exists
        if not os.path.exists(ml_filename):
            raise Exception('Input file not found')
        
        cnet            = CNetwork(name) 
        cnet.tmpsrc     = op.abspath(ml_filename)
        cnet.fileformat = "GraphML"
        cnet.dtype      = "AttributeNetwork"
        cnet.data       = nx.read_graphml(ml_filename)
        cnet.src        = cnet.get_unique_relpath()

        return cnet
    
    def set_with_nxgraph(self, nxGraph, name=None, dtype='AttributeNetwork', fileformat='NXGPickle'):
        """Set the current CNetwork with the given NetworkX graph.

        Set the fileformat to NXGPickle and the dtype to AttributeNetwork.
        Add the NetworkX object to data.
        
        Parameters
        ----------
        nxGraph : NetworkX graph object,
            the NetworkX graph object to add to the current CNetwork.
        name : string, optional,
            the name of the network, it is optional when the CNetwork already have a name
        dtype : AttributeNetwork,
            the data type of this CNetwork
        fileformat : NXGPickle,
            the fileformat of the file of this CNetwork
                                
        See also
        --------
        NetworkX, CNetwork   
        """
        if (self.name is None or self.name == '') and (name is None or name == ''):
            raise Exception('A name has to be given.')
        if name is not None and name != '':
            self.name == name
        self.dtype      = dtype
        self.fileformat = fileformat
        self.data       = nxGraph
        import tempfile
        self.tmpsrc = tempfile.mkstemp(suffix = '.gpickle')[1]
        self.src    = self.get_unique_relpath()
    
supermod.CNetwork.subclass = CNetwork
# end class CNetwork


class CSurface(supermod.CSurface, CBaseClass):
    """A connectome surface object"""
    
    def __init__(self, name='mysurface', dtype='label', fileformat='Gifti', src=None, description=None, metadataDict=None):
        """Create a new CSurface object.
        
        Parameters
        ----------
        name : 'mysurface'
            the unique surface name
        dtype : 'label',
            the type of data that the Gifti file contain. It can be (for Gifti only): 'Labeling', 'Surfaceset', 'Surfaceset+Labeling' or 'Other'.
        fileformat : 'Gifti',
            the fileformat of the surface, use default 'Gifti' to use the only supported Gifti format by cfflib, use 'Other' for others format and custom support.
        src : string, optional,
            the source file of the surface
        description : string, optional,
            a description of the CSurface
        metadataDict : dictionary, optional,
            more metadata relative to the surface as a dictionary
            
        See also
        --------
        Metadata, connectome
    
        """
        super(CSurface, self).__init__(src, dtype, name, fileformat, description, None, )
        
        if metadataDict is not None:
            self.update_metadata(metadataDict)
        else
            self.metadata = Metadata()
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """

        if self.fileformat == 'Gifti':
            fend = '.gii'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CSurface', self.name + fend)
    
    # Create from a Gifti file
    @classmethod
    def create_from_gifti(cls, name, gii_filename, dtype='label'):
        """ Return a CSurface object from a given gii_filename pointint to
        a Gifti file in your file system
        
        Parameters
        ----------
        name : string,
            unique name of the CSurface
        gii_filename : string,
            filename of the Gifti to load
        dtype : 'label',
            the type of data the Gifti file contains
        
        Returns
        -------
        csurf : CSurface
        
        """
        
        # Check if the Gifti file exists
        if not os.path.exists(gii_filename):
            raise Exception('Input file not found')
            
        csurf            = CSurface(name) 
        csurf.tmpsrc     = op.abspath(gii_filename)
        csurf.fileformat = "Gifti"
        csurf.dtype      = dtype
        import nibabel.gifti as nig
        csurf.data       = nig.read(gii_filename)
        csurf.src        = csurf.get_unique_relpath()
        return csurf
    
supermod.CSurface.subclass = CSurface
# end class CSurface


class CVolume(supermod.CVolume, CBaseClass):
    """Connectome volume object"""
    
    def __init__(self, name='myvolume', dtype=None, fileformat='Nifti1', src=None, description=None, metadataDict=None):
        """Create a new CVolume object.
        
        Parameters
        ----------
        name : 'myvolume',
            the unique name of the volume
        dtype : string, optional,
            the data type of the volume. It can be: 'Segmentation', 'T1-weighted', 'T2-weighted', 'PD-weighted', 'fMRI', 'MD', 'FA', 'LD', 'TD', 'FLAIR', 'MRA' or 'MRS depending on your dataset.
        fileformat : 'Nifti1',
            the fileformat of the volume. Only 'Nifti1' is supported, its compressed version '.nii.gz' too.
        src : string, optional,
            the source file of the volume
        description : string, optional,
	       A description according to the format attribute syntax.
        metadataDict : dictionary, optional,
            More metadata relative to the volume as a dictionary
                                
        See also
        --------
        Metadata, connectome
        """
        super(CVolume, self).__init__(src, dtype, name, fileformat, description, None, )
        
        if metadataDict is not None:
            self.update_metadata(metadataDict)
        else:
            self.metadata = Metadata()
                  
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
    
        if self.fileformat == 'Nifti1':
            fend = '.nii.gz'
        elif self.fileformat == 'ANALYZE':
            print "Save ANALYZE file in Nifti format .nii.gz"
            fend = '.nii.gz'
        elif self.fileformat == 'DICOM':
            print "Saving in DICOM format not supported."
            fend = ''
        else:
            fend = ''
            
        return unify('CVolume', self.name + fend)
       
    # Create a CVolume from a Nifti1 file
    @classmethod
    def create_from_nifti(cls, name, nii_filename, dtype=None):
        """ Return a CVolume object from a given Nifti1 filename in your file system
        
        Parameters
        ----------
        name : string,
            the unique name of the CVolume
        nii_filename : string,
            the filename of the Nifti1 file to load
        dtype : string, optional,
            the datatype of the new CVolume
        
        Returns
        -------
        cvol : CVolume
        
        """
        
        # Check if the Nifti1 file exists
        if not os.path.exists(nii_filename):
            raise Exception('Input file not found')
            
        cvol            = CVolume(name) 
        cvol.tmpsrc     = op.abspath(nii_filename)
        cvol.fileformat = "Nifti1"
        cvol.dtype      = dtype
        cvol.data       = ni.load(nii_filename)
        cvol.src        = cvol.get_unique_relpath()
        return cvol
    
supermod.CVolume.subclass = CVolume
# end class CVolume


class CTrack(supermod.CTrack, CBaseClass):
    """ Connectome track object"""
    
    def __init__(self, name='mytrack', fileformat='TrackVis', src=None, description=None, metadataDict=None):
        """Create a new CTrack object.
            
            Parameters
            ----------
            name : 'mytrack', 
                the unique name of track
            fileformat : 'TrackVis',
                the fileformat of the track, only 'TrackVis' is supported
            src : string, optional,
                the source file of the track
            description : string, optional,
                a description of the track
            metadataDict : dictionary, optional,
                Metadata object relative to the track as a dictionary
                
            See also
            --------
            Metadata, connectome
        
        """
        super(CTrack, self).__init__(src, name, fileformat, description, None, )
        
        if metadataDict is not None:
            self.update_metadata(metadataDict)
        else:
            self.metadata = Metadata()
                        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
    
        if self.fileformat == 'TrackVis':
            fend = '.trk'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CTrack', self.name + fend)
    
    # Create a CTrack from a TrackVis file
    @classmethod
    def create_from_trackvis(cls, name, trk_filename):
        """ Return a CTrack object from a given TrackVis filename in your file system
        
        Parameters
        ----------
        name : string,
            the unique name of the CTrack
        trk_filename : string,
            the filename of the TrackVis file to load
        
        Returns
        -------
        ctrack : CTrack
        
        """
        
        # Check if the TrackVis file exists
        if not os.path.exists(trk_filename):
            raise Exception('Input file not found')
            
        ctrack            = CTrack(name) 
        ctrack.tmpsrc     = op.abspath(trk_filename)
        ctrack.fileformat = "TrackVis"
        ctrack.data       = ni.trackvis.read(trk_filename)
        ctrack.src        = ctrack.get_unique_relpath()
        return ctrack
    
supermod.CTrack.subclass = CTrack
# end class CTrack


class CTimeserie(supermod.CTimeserie, CBaseClass):
    """Connectome timeserie object"""
    
    def __init__(self, name='mytimeserie', fileformat='HDF5', src=None, description=None, metadataDict=None):
        """Create a connectome timeserie object
        
        Parameters
        ----------
        name : 'mytimeserie',
            the unique name of the timeserie
        fileformat : 'HDF5',
            the fileformat of the timeserie, only 'HDF5' is supported
        src : string, optional,
            the source file of the timeserie
        description : string, optional,
            a description of the timeserie
        metadataDict : dictionary, optional,
            some metadata related to the timeserie as a dictionary
            
        See also
        --------
        Metadata, connectome 
        """
        super(CTimeserie, self).__init__(src, name, fileformat, description, None, )
        
        if metadataDict is not None:
            self.update_metadata(metadataDict)
        else:
            self.metadata = Metadata()
                
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.fileformat == 'HDF5':
            fend = '.h5'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CTimeserie', self.name + fend)
    
    # tables.openFile
    # Create a CTimeserie from a HDF5 file
    @classmethod
    def create_from_hdf5(cls, name, hdf_filename):
        """ Return a CTimeserie object from a given HDF5 filename in your file system
        
        Parameters
        ----------
        name : string,
            the unique name of the CTimeserie
        hdf_filename : string,
            the filename of the HDF5 file to load
        
        Returns
        -------
        ctime : CTimeserie
        
        """
        
        # Check if the HDF5 file exists
        if not os.path.exists(hdf_filename):
            raise Exception('Input file not found')
            
        ctime            = CTimeserie(name) 
        ctime.tmpsrc     = op.abspath(hdf_filename)
        ctime.fileformat = "HDF5"
        ctime.data       = tables.openFile(hdf_filename)
        ctime.src        = ctime.get_unique_relpath()
        return ctime
    
supermod.CTimeserie.subclass = CTimeserie
# end class CTimeserie


class CData(supermod.CData, CBaseClass):
    """Connectome data object"""
    
    def __init__(self, name='mydata', fileformat=None, src=None, description=None, metadataDict=None):
        """Create a connectome data object
        
        Parameters
        ----------
        name : 'mydata',
            the unique name of the data
        fileformat : string,
            the fileformat of the data, it can be: 'NumPy', 'HDF5', 'XML', 'Other'
        src : string, optional,
            The path to the file according to location attribute
        description : string, optional,
            a description of the data
        metadataDict : dictionary, optional,
            some metadata related to the data as a dictionary
            
        See also
        --------
        Metadata, connectome 
        """
        super(CData, self).__init__(src, name, fileformat, description, metadata, )
        
        if metadataDict is not None:
            self.update_metadata(metadataDict)
        else:
            self.metadata = Metadata()
                
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.fileformat == 'NumPy':
            fend = '.npy'
        if self.fileformat == 'HDF5':
            fend = '.h5'
        if self.fileformat == 'XML':
            fend = '.xml'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CData', self.name + fend)
    
supermod.CData.subclass = CData
# end class CData


class CScript(supermod.CScript, CBaseClass):
    """Connectome script object"""

    def __init__(self, name='myscript', dtype='Python', fileformat='UTF-8', src=None, description=None, metadataDict=None):
        """Create a connectome script object
        
        Parameters
        ----------
        name : 'myscript',
            the unique name of the script
        dtype : 'Python',
            the data type of the script, it can be: 'Python', 'Bash', 'Matlab', 'Other'
        fileformat : 'UTF-8',
            the fileformat of the script
        src : string, optional,
            The path to the file according to location attribute
        description : string, optional,
            a description of the script
        metadataDict : dictionary, optional,
            some metadata related to the script as a dictionary
            
        See also
        --------
        Metadata, connectome 
        """
        super(CScript, self).__init__(src, dtype, name, fileformat, description, metadata, )
        
        if metadataDict is not None:
            self.update_metadata(metadataDict)
        else:
            self.metadata = Metadata()
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.dtype == 'Python':
            fend = '.py'
        elif self.dtype == 'Bash':
            fend = '.sh'
        elif self.dtype == 'Matlab':
            fend = '.m'
        else:
            fend = '.txt'
            
        return unify('CScript', self.name + fend)

    @classmethod
    def create_from_file(cls, name, filename, dtype= 'Python', fileformat = 'UTF-8'):
        """ Return a CScript object from a given script/text file
        
        Parameters
        ----------
        name : string,
            the unique name of the CScript
        filename : string,
            the absolute to the filename of the script/text file
        dtype : string, optional,
            the datatype of the new CScript
        fileformat : string, optional
            the file format of the file, usually UTF-8
        
        Returns
        -------
        cscr : CScript
        
        """
        
        # Check if the file exists
        if not os.path.exists(filename):
            raise Exception('Input file not found')
                    
        cscr            = CScript(name=name) 
        cscr.tmpsrc     = op.abspath(filename)
        cscr.fileformat = fileformat
        cscr.dtype      = dtype
        # not load it by default!
        # cscr.data       = open(filename, 'r')
        cscr.src        = cscr.get_unique_relpath()
        return cscr
    
supermod.CScript.subclass = CScript
# end class CScript


# TODO leave it for the moment
class CImagestack(supermod.CImagestack, CBaseClass):
    def __init__(self, src=None, fileformat=None, name=None, pattern=None, description=None, metadata=None):
        super(CImagestack, self).__init__(src, fileformat, name, pattern, description, metadata, )
        
    def save(self):
        """ Save a loaded connectome object to a temporary file, return the path """
        raise NotImplementedError('Saving CImagestack not implemented yet.')
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        return unify('CImagestack', self.name + '/')
    
supermod.CImagestack.subclass = CImagestack
# end class CImagestack


class Metadata(supermod.Metadata):
    def __init__(self, data=None):
        super(Metadata, self).__init__(data, )  
        
    # get the Metadata as a dictionary
    def get_as_dictionary(self):
        """Return the metadata as a dictionary"""
        dat = self.get_data()
        ret = {}
        for ele in dat:
            ret[ele.key] = ele.valueOf_
        return ret
    
    # Set the Metadata with a dictionary
    def set_with_dictionary(self, dictionary):
        """Set the metadata with a dictionary"""
        dat = self.get_data()
        for k in dictionary:
            test = False
            # check if the key already exists
            for ele in dat:
                if ele.key == k:
                    # always change the value to a string
                    ele.valueOf_ = str(dictionary[k])
                    test = True
            if not test:
                self.data.append(data(str(k),str(dictionary[k])))  
                
supermod.Metadata.subclass = Metadata
# end class Metadata


class data(supermod.data):
    def __init__(self, key=None, value=None):
        super(data, self).__init__(key, value, )
supermod.data.subclass = data
# end class data


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    if hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass
    

def parse(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    doc = None
    return rootObj
    

def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    #sys.stdout.write('<?xml version="1.0" ?>\n')
    #rootObj.export(sys.stdout, 0, name_=rootTag,
    #    namespacedef_='')
    
    # update parent references
    rootObj._update_parent_reference()
    
    return rootObj


def parseLiteral(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from cff import *\n\n')
    sys.stdout.write('import cff as model_\n\n')
    sys.stdout.write('rootObj = model_.connectome(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="connectome")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


