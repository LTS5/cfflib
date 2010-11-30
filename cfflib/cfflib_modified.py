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
    """The connectome object is the main object of this format. It contains CMetadata, it can contain some CData, CNetwork, CSurface, CTimeserie, CTrack and CVolume. It is possible to store it to a simple CML file or to a complete compressed CFF file with all sources."""
    def __init__(self, connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeserie=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        """Create a new connectome file.
        
        Parameters
        ----------
        connectome_meta       : list of CMetadata
        connectome_network    : list of CNetwork
        connectome_surface    : list of CSurface
        connectome_volume     : list of CVolume
        connectome_track      : list of CTrack
        connectome_timeserie  : list of CTimeserie
        connectome_data       : list of CData
        connectome_script     : list of CScript
        connectome_imagestack : list of CImagestack
            
        See also
        --------
            CMetadata, CNetwork, CSurface, CVolume, CTrack, CTimeserie, CData, CScript, CImagestack
    
        """
        super(connectome, self).__init__(connectome_meta, connectome_network, connectome_surface, connectome_volume, connectome_track, connectome_timeserie, connectome_data, connectome_script, connectome_imagestack, )
        # add parent reference to all children
        self._update_parent_reference()
        # add some useful attributes to the save functions
        self.iszip = False

    def get_all(self):
        """Return all connectome objects mixed as a list.
        
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
        """Return the list of connectome object(s) that have the given name.
        
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
        """Checks if the files described in the meta.cml are contained in the connectome zip file
        
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
        """Checks whether the names are unique.
        
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
    
    def is_name_unique(self, name):
        """Check if the given name is unique.
        
        Parameters
        ----------
        self : connectome
        name : string
            
        See also
        --------
            check_names_unique, connectome
        """
        all_cobj = self.get_all()
        namelist = []
        for ele in all_cobj:
            namelist.append(ele.name)
        if name in namelist:
            return False
        else:
            return True
    
    def get_unique_cff_name(self):
        """Return a unique connectome file name
        
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
        
    def get_normalised_name(self, name):
        """Return a normalised name, without space and in lower case
        
        Parameters
        ----------
            self : connectome
            name : string
            
        Examples
        --------
            >>> myConnectome.get_unique_cff_name()
            my_first_network
            
        See also
        --------
            connectome
    
        """
        n = name.lower()
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
        
    def add_connectome_network_from_nxgraph(self, nxGraph, name):
        """Add a new CNetwork from the given NetworkX graph object to the connectome.
        
        Parameters
        ----------
        self    : connectome
        nxGraph : NetworkX,
            a NetworkX graph object
        name : string,
            a unique name for the NetworkX graph to add to the connectome object
                    
        Examples
        --------
            >>> myConnectome.add_connectome_network_from_nx(myNXGraph)
            
        See also
        --------
            NetworkX, CNetwork.set_from_nx, CNetwork, connectome.add_connectome_network, connectome   
            
        """
        nName = self.get_normalised_name(name)
        if self.is_name_unique(nName):
            n = CNetwork()
            n.name = nName
            n.set_with_nxgraph(nxGraph)
            self.add_connectome_network(n)
        else:
            print "ERROR - Name is not unique"
            return
    
    def add_connectome_network_from_graphml(self, graphML, name):
        """
        Add a new CNetwork from the given GraphML file to the connectome object.
        
        Parameters
        ----------
        self    : connectome
        nxGraph : GraphML file,
            a GraphML file
                    
        Examples
        --------
            >>> myConnectome.add_connectome_network_from_ml('myGraphML.graphml')
            
        See also
        --------
            GraphML, GraphML.load_from_ml, CNetwork, connectome.add_connectome_network, connectome
            
        """
        nName = self.get_normalised_name(name)
        if self.is_name_unique(nName):
            n = CNetwork()
            n.name = nName
            n.load_from_graphml(graphML)
            self.add_connectome_network(n)
        else:
            print "ERROR - Name is not unique"
            return            
        
supermod.connectome.subclass = connectome
# end class connectome


class CMetadata(supermod.CMetadata):
    """Specific metadata to the connectome. The name is the name of the connectome. The version and the generator are required and are defined by default."""
    
    def __init__(self, name, version='2.0', generator='cfflib', author=None, institution=None, creation_date=None, modification_date=None, species=None, legal_notice=None, reference=None, email=None, url=None, description=None, metadata=None):
        """Creates a connectome metadata object, specific metadata to the connectome object.
        
        Parameters
        ----------
        name : string,
            the name of this connectome object 
        version : 2.0,  
            version of the cfflib
        generator : cfflib,
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
            the specied of the subject
        legal_notice : string, optional,
            legal information
        reference : string, optional,
            reference
        email : string, optional,
            an email of reference (author one)
        url : string, optional,
            an related url
        description : plaintext, optional,
            a text description of the connectome
        metadata : dictionary, optional,
            some metadata informations as a dictionary
                    
        Examples
        --------
            >>> myMeta = CMetadata(name='Lausanne 2010', institution='EPFL', author='Your Name')
            
        See also
        --------
            Metadata, connectome  
        """
        # TODO put it in connectome (cff) because I need the connectome object...
        # Check for nam uniqueness
#        name = name.lower()
#        name = name.replace(' ', '_')
#        if not connectome.is_name_unique(name):
#            raise Exception('Name %s in not unique!', name)
        super(CMetadata, self).__init__(version, generator, author, institution, creation_date, modification_date, name, species, legal_notice, reference, email, url, description, metadata, )

    # Description object hide as property
    @property
    def description(self):
        return self.value
    def description(self, value):
        d = description('plaintext', value)
        
supermod.CMetadata.subclass = CMetadata
# end class CMetadata


class description(supermod.description):
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
    """Create a new CNetwork object.
        
        Parameters
        ----------
        name : string
            the network unique name
        src : string, optional,
            the source file of the network
        dtype : 'AttributeNetwork',
            the data type of the network. It could be: ''
        fileformat : 'GraphML',
            the fileformat of the network. It could be: ''
        description : plaintext, optional,
            a text description of the CNetwork
        metadata : dictionary, optional,
            Metadata dictionary relative to the network
            
        See also
        --------
        Metadata, connectome
    
    """
    def __init__(self, name=None, src=None, dtype='AttributeNetwork', fileformat='GraphML', description=None, metadata=None):

        super(CNetwork, self).__init__(src, dtype, name, fileformat, metadata, description, )

    # Description object hide as a property
    @property
    def description(self):
        return self.value
    def description(self, value):
        d = description('plaintext', value)
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.fileformat == 'GraphML':
            fend = '.graphml'
        elif self.fileformat == 'GEXF':
            fend = '.gexf'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CNetwork', self.name + fend)
    
    def load_from_graphml(self, ml_filename):
        """Load a graphml into the current CNetwork, adding the GraphML to contents, the ml_filename to src, if not already specified in the current CNetwork the graphML name to name, the fileformat to GraphML and the dtype to AttributeNetwork.
        
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
    
    def set_with_nxgraph(self, nxGraph):
        """Set the current CNetwork with the given NetworkX graph. Add the name if not already specified in the current CNetwork, set the fileformat to NetworkX and the dtype to AttributeNetwork. Add the NetworkX object to contents.
        
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
    """
        Create a new CSurface object.
        
        Parameters
        ----------
            name              : string, optional
                the surface name
            src               : string, optional,
                the source file of the surface
            dtype             : string, optional,
                the data type of the surface
            fileformat        : string, optional,
                the fileformat of the surface
            description       : description, optional,
                a description (key, value) of the CSurface
            metadata          : Metadata, optional,
                Metadata object relative to the surface
                    
        Examples
        --------
            Empty
            >>> myCSurf1 = CSurface()
            Create an empty CSurface object
            
        See also
        --------
            description, Metadata, connectome
    
    """
    def __init__(self, name=None, src=None, dtype=None, fileformat=None, description=None, metadata=None):
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
    """
        Create a new CVolume object.
        
        Parameters
        ----------
            name              : string, optional
                the volume name
            src               : string, optional,
                the source file of the volume
            dtype             : string, optional,
                the data type of the volume
            fileformat        : string, optional,
                the fileformat of the volume
            description       : description, optional,
                a description (key, value) of the CVolume
            metadata          : Metadata, optional,
                Metadata object relative to the volume
                    
        Examples
        --------
            Empty
            >>> myCVol1 = CVolume()
            Create an empty CVolume object
            
        See also
        --------
            description, Metadata, connectome
    
    """
    def __init__(self, name=None, src=None, dtype=None, fileformat='Nifti1', description=None, metadata=None):
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
    """
        Create a new CTrack object.
        
        Parameters
        ----------
            name              : string, optional
                the track name
            src               : string, optional,
                the source file of the track
            fileformat        : string, optional,
                the fileformat of the track
            description       : description, optional,
                a description (key, value) of the CTrack
            metadata          : Metadata, optional,
                Metadata object relative to the track
                    
        Examples
        --------
            Empty
            >>> myCVol1 = CTrack()
            Create an empty CTrack object
            
        See also
        --------
            description, Metadata, connectome
    
    """
    def __init__(self, name=None, src=None, fileformat='TrackVis', description=None, metadata=None):
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


