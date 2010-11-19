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
    """
        Create a new connectome file.
        
        Parameters
        ----------
            connectome_meta       : list of CMetadata, optional
            connectome_network    : list of CNetwork, optional
            connectome_surface    : list of CSurface, optional
            connectome_volume     : list of CVolume, optional
            connectome_track      : list of CTrack, optional
            connectome_timeserie  : list of CTimeserie, optional
            connectome_data       : list of CData, optional
            connectome_script     : list of CScript, optional
            connectome_imagestack : list of CImagestack, optional
                    
        Examples
        --------
            Empty
            >>> myConnectome = connectome()
            Create an empty connectome object
            
            With an existing CNetwork
            >>> myConnectome = connectome(connectome_network=[CNet1])
            Create the connectome object with an existing CNetwork: CNet1
            
        See also
        --------
            CMetadata, CNetwork, CSurface, CVolume, CTrack, CTimeserie, CData, CScript, CImagestack
    
    """
    def __init__(self, connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeserie=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        super(connectome, self).__init__(connectome_meta, connectome_network, connectome_surface, connectome_volume, connectome_track, connectome_timeserie, connectome_data, connectome_script, connectome_imagestack, )
        # add parent reference to all children
        self._update_parent_reference()

    def get_all(self):
        """
        Return all connectome objects mixed as a list.
        
        Parameters
        ----------
            self : connectome
            
        Examples
        --------
            >>> myConnectome.get_all()
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
        """
        Return the list of connectome object(s) that have the given name.
        
        Parameters
        ----------
            self : connectome
            name : string
                name of the wanted object(s)
            
        Examples
        --------
            >>> myConnectome.get_by_name('my first network')
            [<cfflib.cfflib_modified.CNetwork object at 0x2c46b10>]
            
        See also
        --------
            connectome, get_all
    
        """         
        all_cobj = self.get_all() 
        
        ret = []
        
        for ele in all_cobj:
            if name == ele.name:
                ret.append(ele)
                
        if len(ret) > 1:
            warnings.warn('More than one element found. Non-unique name could lead to problems!')
            
        return ret
            

    def check_file_in_cff(self):
        """
        Checks if the files described in the meta.cml are contained in the connectome zip file
        
        Parameters
        ----------
            self : connectome
            
        Examples
        --------
            >>> myConnectome.check_file_in_cff()
            
        See also
        --------
            connectome
    
        """  
        
        if not self.iszip:
            return
        
        all_cobj = self.get_all()
        nlist = self._zipfile.namelist()
        
        for ele in all_cobj:
            
            if not ele.src in nlist:
                msg = "Element with name %s and source path %s is not contained in the connectome file." % (ele.name, ele.src)
                raise Exception(msg)
            
    def check_names_unique(self):
        """
        Checks whether the names are unique.
        
        Parameters
        ----------
            self : connectome
            
        Examples
        --------
            >>> myConnectome.check_names_unique()
            
        See also
        --------
            connectome
    
        """  
        
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
    
    def get_unique_cff_name(self):
        """
        Return a unique connectome file name
        
        Parameters
        ----------
            self : connectome
            
        Examples
        --------
            >>> myConnectome.get_unique_cff_name()
            my_first_network
            
        See also
        --------
            connectome
    
        """
        n = self.get_connectome_meta().name
        n = n.lower()
        n = n.replace(' ', '_')
        return n

    def _update_parent_reference(self):
        """ Updates the parent reference to the connectome file super-object """

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
        save : bool
            Save the content before closing.
            
        """

        all_cobj = self.get_all() 
        
        for ele in all_cobj:
            
            if hasattr(ele, 'content') and hasattr(ele, 'tmpsrc') and op.exists(ele.tmpsrc):
                
                if save:
                    ele.save()
                
                # remove .content and .tmpsrc
                print "Will not remove file %s from file system" % ele.tmpsrc
                print "Remove .content attribute"
                del ele.content
                print "Remove .tmpsrc attribute"
                del ele.tmpsrc
        
    def add_connectome_network_from_nx(self, nxGraph):
        """
        Add a new CNetwork from the given NetworkX graph to the connectome object.
        
        Parameters
        ----------
            self    : connectome
            nxGraph : a NetworkX graph
                    
        Examples
        --------
            >>> myConnectome.add_connectome_network_from_nx(myNXGraph)
            
        See also
        --------
            NetworkX, NetworkX.set_from_nx, CNetwork, connectome   
            
        """
        n = CNetwork()
        n.set_from_nx(nxGraph)
        self.add_connectome_network(n)
    
    def add_connectome_network_from_ml(self, graphML):
        """
        Add a new CNetwork from the given GraphML object to the connectome object.
        
        Parameters
        ----------
            self    : connectome
            nxGraph : a GraphML object
                    
        Examples
        --------
            >>> myConnectome.add_connectome_network_from_ml(myGraphML)
            
        See also
        --------
            GraphML, GraphML.set_from_ml, CNetwork, connectome   
            
        """
        n = CNetwork()
        n.set_from_ml(graphML)
        self.add_connectome_network(n)
        
supermod.connectome.subclass = connectome
# end class connectome


class CMetadata(supermod.CMetadata):
    """
        Creates a connectome metadata object, useful to add metadata to other object.
        
        Parameters
        ----------
            version           : string, optional, 
                version of the current object
            generator         : string, optional,
                generator of the current object
            author            : string, optional 
            institution       : string, optional 
            creation_date     : string, optional 
            modification_date : string, optional 
            name              : string, optional 
            species           : string, optional 
            legal_notice      : string, optional 
            reference         : string, optional 
            email             : string, optional 
            url               : string, optional 
            description       : description, optional 
            metadata          : Metadata, optional 
                    
        Examples
        --------
            >>> myMeta = CMetadata(name='my metadata', institution='EPFL', version='0.0.0')
            
        See also
        --------
            Metadata, description, connectome  
    """
    def __init__(self, version=None, generator=None, author=None, institution=None, creation_date=None, modification_date=None, name=None, species=None, legal_notice=None, reference=None, email=None, url=None, description=None, metadata=None):
        super(CMetadata, self).__init__(version, generator, author, institution, creation_date, modification_date, name, species, legal_notice, reference, email, url, description, metadata, )
supermod.CMetadata.subclass = CMetadata
# end class CMetadata


class description(supermod.description):
    """
        Creates a description object consisting in a format and a value.
        
        Parameters
        ----------
            format : string, 
                the format of the value
            value  : format
                    
        Examples
        --------
            >>> myDesc = description('plaintext', 'A first description')
            
        See also
        --------
            Metadata, connectome  
    """
    def __init__(self, format=None, value=None):
        super(description, self).__init__(format, value, )
supermod.description.subclass = description
# end class description


class CBaseClass(object):

    def load(self, custom_loader = None):
        """ Load the element. The loaded object is stored in the content attribute.
        
        Parameters
        ----------
        custom_loader : function, default: None
            Custom loader function that takes connectome element as
            its first argument.
            
        See Also
        --------
        See cfflib.util.load_data for example. """
        
        if not custom_loader is None:
            self.content = custom_loader(self)
        else:
            self.content = load_data(self)
    
    def save(self):
        """ Save a loaded connectome object to a temporary file, return the path """
        rval = save_data(self)
        if not rval == '':
            self.tmpsrc = rval 
            return rval
        else:
            raise Exception('There is nothing to save.')
        
#    def __repr__(self):
#        pass
        # XXX: give a representation of the object. for print
        
    def get_type(self):
        """ Returns the class name """
        pass
        # XXX: as single string 
    

class CNetwork(supermod.CNetwork, CBaseClass):
    """
        Create a new CNetwork object.
        
        Parameters
        ----------
            name              : string, optional
                the network name
            src               : string, optional,
                the source file of the network
            dtype             : string, optional,
                the data type of the network
            fileformat        : string, optional,
                the fileformat of the network
            description       : description, optional,
                a description (key, value) of the CNetwork
            metadata          : Metadata, optional,
                Metadata object relative to the network
            network_surface   : NetworkSurface, optional
            network_volume    : NetworkVolume, optional
            network_track     : NetworkTrack, optional
            network_timeserie : NetworkTimeserie, optional
            network_data      : NetworkData, optional
                    
        Examples
        --------
            Empty
            >>> myCNet1 = CNetwork()
            Create an empty CNetwork object
            
            With a name
            >>> myCNet2 = CNetwork(name='my first network')
            Create a CNetwork nammed: 'my first network'
            
        See also
        --------
            description, Metadata, NetworkData, NetworkSurface, NetworkTimeserie, NetworkTrack, NetworkVolume, connectome
    
    """
    def __init__(self, name=None, src=None, dtype='AttributeNetwork', fileformat='GraphML', description=None, metadata=None, network_surface=None, network_volume=None, network_track=None, network_timeserie=None, network_data=None):

        super(CNetwork, self).__init__(src, dtype, name, fileformat, metadata, network_surface, network_volume, network_track, network_timeserie, network_data, description, )
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.fileformat == 'GraphML':
            fend = '.graphml'
        elif self.fileformat == 'GEXF':
            fend = '.gexf'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CNetwork', self.name + fend)
    
    # GraphML treatment
    def load_graphml(self):
        """
        Load a GraphML object from the src if the fileformat is GraphML.
        
        Parameters
        ----------
            self : CNetwork
        
        Examples
        --------
            ...
                        
        See also
        --------
            load_networkx, GraphML, NetworkX    
        """
        if self.src == None:
            print "Error - the src is not define"
            return
        if self.fileformat != 'GraphML':
            print "Error - the file format is: "+self.fileformat+"; it should be GraphML"
            return
        return nx.read_graphml(self.src)
    
    def load_from_ml(self, ml_filename):
        """
        Load a graphml into the current CNetwork, adding the GraphML to contents, the ml_filename to src, if not already specified in the current CNetwork the graphML name to name, the fileformat to GraphML and the dtype to AttributeNetwork.
        
        Parameters
        ----------
            self        : CNetwork
            ml_filename : filename of the GraphML
        
        Examples
        --------
            ...
            
        See also
        --------
            set_from_ml, load_from_nx, set_from_nx, graphml, networkx    
        """
        ml = nx.read_graphml(ml_filename)
        self.src = ml_filename
        self.set_with_ml(ml)
    
    def set_with_ml(self, graphML):
        """
        Set the current CNetwork with the given GraphML object. Add the name if not already specified in the current CNetwork, set the fileformat to GraphML and the dtype to AttributeNetwork. Add the GraphML object to contents.
        
        Parameters
        ----------
            self    : CNetwork
            graphML : a graphML object
        
        Examples
        --------
            ...
                                
        See also
        --------
            set_with_nx, GraphML   
        """
        if self.name == '':
            self.name       = graphML.name
        self.dtype      = "AttributeNetwork"
        self.fileformat = "GraphML"
        self.contents   = graphML
    
    # NetworkX treatment
    def load_networkx(self):
        """
        Load a NetworkX graph from the src if the fileformat is NetworkX.
        
        Parameters
        ----------
            self: CNetwork
        
        Examples
        --------
            ...
                        
        See also
        --------
            load_graphml, NetworkX   
        """
        if self.src == None:
            print "Error - the src is not define"
            return
        if self.fileformat != 'NetworkX':
            print "Error - the file format is: "+self.fileformat+"; it should be NetworkX"
            return
        return nx.load(self.src)    
    
    def load_from_nx(self, nx_filename):
        """
        Load a NetworkX into the current CNetwork, adding the NetworkX to contents, the nx_filename to src, if not already specified in the current CNetwork the NetworkX name to name, the fileformat to NetworkX and the dtype to AttributeNetwork.
        
        Parameters
        ----------
            CNetwork
            nx_filename : filename of the NetworkX
        
        Examples
        --------
            ...
            
        See also
        --------
            set_with_nx, load_from_ml, NetworkX    
        """
        g = nx.load(nx_filename)
        self.src = nx_filename
        self.set_with_nx(g)
    
    def set_with_nx(self, nxGraph):
        """
        Set the current CNetwork with the given NetworkX graph. Add the name if not already specified in the current CNetwork, set the fileformat to NetworkX and the dtype to AttributeNetwork. Add the NetworkX object to contents.
        
        Parameters
        ----------
            self    : CNetwork
            nxGraph : a NetworkX graph object
        
        Examples
        --------
            ...
                                
        See also
        --------
            set_with_ml, NetworkX    
        """
        if self.name == '':
            self.name       = nxGraph.name
        self.dtype      = "AttributeNetwork"
        self.fileformat = "NetworkX"
        self.contents   = nxGraph
    
supermod.CNetwork.subclass = CNetwork
# end class CNetwork


class CSurface(supermod.CSurface, CBaseClass):
    def __init__(self, src=None, dtype=None, name=None, fileformat=None, description=None, metadata=None):
        super(CSurface, self).__init__(src, dtype, name, fileformat, description, metadata, )
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """

        if self.fileformat == 'Gifti':
            fend = '.gii'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CSurface', self.name + fend)
    
supermod.CSurface.subclass = CSurface
# end class CSurface


class CVolume(supermod.CVolume, CBaseClass):
    def __init__(self, src=None, dtype=None, name=None, fileformat='Nifti1', description=None, metadata=None):
        super(CVolume, self).__init__(src, dtype, name, fileformat, description, metadata, )
                  
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
    
supermod.CVolume.subclass = CVolume
# end class CVolume

class CTrack(supermod.CTrack, CBaseClass):
    def __init__(self, src=None, name=None, fileformat='TrackVis', description=None, metadata=None):
        super(CTrack, self).__init__(src, name, fileformat, description, metadata, )
                        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
    
        if self.fileformat == 'TrackVis':
            fend = '.trk'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CTrack', self.name + fend)
    
supermod.CTrack.subclass = CTrack
# end class CTrack


class CTimeserie(supermod.CTimeserie, CBaseClass):
    def __init__(self, src=None, name=None, fileformat='HDF5', description=None, metadata=None):
        super(CTimeserie, self).__init__(src, name, fileformat, description, metadata, )
                
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.fileformat == 'HDF5':
            fend = '.h5'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CTimeserie', self.name + fend)
    
supermod.CTimeserie.subclass = CTimeserie
# end class CTimeserie


class CData(supermod.CData, CBaseClass):
    def __init__(self, src=None, name=None, fileformat=None, description=None, metadata=None):
        super(CData, self).__init__(src, name, fileformat, description, metadata, )
                
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
    def __init__(self, src=None, type_='Python', name=None, description=None, metadata=None):
        super(CScript, self).__init__(src, type_, name, description, metadata, )
                
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.type == 'Python':
            fend = '.py'
        if self.type == 'Bash':
            fend = '.sh'
        if self.tyoe == 'Matlab':
            fend = '.m'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CScript', self.name + fname)

supermod.CScript.subclass = CScript
# end class CScript


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
    
    @property
    def contents(self):
        """ Returns the metadata as a dictionary """
        dat = self.get_data()
        ret = {}
        for ele in dat:
            ret[ele.key] = ele.value
        return ret
    
    
supermod.Metadata.subclass = Metadata
# end class Metadata


class data(supermod.data):
    def __init__(self, key=None, value=None):
        super(data, self).__init__(key, value, )
supermod.data.subclass = data
# end class data


class NetworkSurface(supermod.NetworkSurface):
    """
        The name of the surface as reference to an existing connectome-surface
    
        Parameters
        ----------
            name     : string,
                the name of the surface
            metadata : Metadata, optional
        
        Examples
        --------
            ...
                                
        See also
        --------
            Metadata, connectome   
            
    """
    def __init__(self, name=None, metadata=None):
        super(NetworkSurface, self).__init__(name, metadata, )
supermod.NetworkSurface.subclass = NetworkSurface
# end class NetworkSurface


class NetworkVolume(supermod.NetworkVolume):
    """
        The name of the volume as reference to an existing connectome-volume. The connectome-volume can be of any dtype.
    
        Parameters
        ----------
            name     : string,
                the name of the volume
            metadata : Metadata, optional
        
        Examples
        --------
            ...
                                
        See also
        --------
            Metadata, connectome   
            
    """
    def __init__(self, name=None, metadata=None):
        super(NetworkVolume, self).__init__(name, metadata, )
supermod.NetworkVolume.subclass = NetworkVolume
# end class NetworkVolume


class NetworkTrack(supermod.NetworkTrack):
    """
        The name of the track as reference to an existing connectome-track. 
    
        Parameters
        ----------
            name     : string,
                the name of the track
            metadata : Metadata, optional
        
        Examples
        --------
            ...
                                
        See also
        --------
            Metadata, connectome   
            
    """
    def __init__(self, name=None, metadata=None):
        super(NetworkTrack, self).__init__(name, metadata, )
supermod.NetworkTrack.subclass = NetworkTrack
# end class NetworkTrack


class NetworkTimeserie(supermod.NetworkTimeserie):
    """
        The name of the timeserie as reference to an existing connectome-timeserie. 
    
        Parameters
        ----------
            name     : string,
                the name of the timeserie
            metadata : Metadata, optional
        
        Examples
        --------
            ...
                                
        See also
        --------
            Metadata, connectome   
            
    """
    def __init__(self, name=None, metadata=None):
        super(NetworkTimeserie, self).__init__(name, metadata, )
supermod.NetworkTimeserie.subclass = NetworkTimeserie
# end class NetworkTimeserie


class NetworkData(supermod.NetworkData):
    """
        The name of the data object as reference to an existing connectome-data
    
        Parameters
        ----------
            name     : string,
                the name of the data
            metadata : Metadata, optional
        
        Examples
        --------
            ...
                                
        See also
        --------
            Metadata, connectome   
            
    """
    def __init__(self, name=None, metadata=None):
        super(NetworkData, self).__init__(name, metadata, )
supermod.NetworkData.subclass = NetworkData
# end class NetworkData



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


