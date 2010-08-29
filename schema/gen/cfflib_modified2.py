#!/usr/bin/env python

#
# Generated Sun Aug 29 11:58:22 2010 by generateDS.py version 2.1a.
#

### My Imports

import warnings

from util import *



# PyTables
try:
    import tables
except ImportError:
    raise ImportError("Failed to import networkx from any known place")



# NumPy
try:
    import numpy as np
except ImportError:
    raise ImportError("Failed to import numpy from any known place")
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
    def __init__(self, connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeserie=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        super(connectome, self).__init__(connectome_meta, connectome_network, connectome_surface, connectome_volume, connectome_track, connectome_timeserie, connectome_data, connectome_script, connectome_imagestack, )

        # add parent reference to all children
        self._update_parent_reference()

    def get_all(self):
        """ Returns all connectome objects mixed """
        
        return self.connectome_network + self.connectome_surface + \
                self.connectome_volume + self.connectome_track + \
                self.connectome_timeserie + self.connectome_data + \
                self.connectome_script + self.connectome_imagestack
    
    def get_by_name(self, name):
        """ Return connectome object(s) that have given name """
        
        all_cobj = self.get_all() 
        
        ret = []
        
        for ele in all_cobj:
            if name == ele.name:
                ret.append(ele)
                
        if len(ret) > 1:
            warnings.warn('More than one element found. Non-unique name could lead to problems!')
            
        return ret
            

    def _update_parent_reference(self):
        """ Updates the parent reference to the connectome file super-object """

        all_cobj = self.get_all() 
        
        for ele in all_cobj:
            ele.parent_cfile = self

    def to_xml(self):
        from StringIO import StringIO
        re = StringIO()
        re.write('<?xml version="1.0" encoding="UTF-i"?\n')
        ns = """xmlns="http://www.connectomics.ch/2010/Connectome/xmlns"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.connectomics.ch/2010/Connectome/xmlns connectome.xsd" """
        self.export(re, 0, name_= "connectome", namespacedef_=ns)
        re.seek(0)
        return re.read()
    
supermod.connectome.subclass = connectome
# end class connectome


class CMetadata(supermod.CMetadata):
    def __init__(self, version=None, generator=None, initial_creator=None, institution=None, creation_date=None, modification_date=None, name=None, species=None, targetspace=None, legal_notice=None, reference=None, email=None, url=None, description=None, metadata=None):
        super(CMetadata, self).__init__(version, generator, initial_creator, institution, creation_date, modification_date, name, species, targetspace, legal_notice, reference, email, url, description, metadata, )
supermod.CMetadata.subclass = CMetadata
# end class CMetadata


class description(supermod.description):
    def __init__(self, format=None, valueOf_=None):
        super(description, self).__init__(format, valueOf_, )
supermod.description.subclass = description
# end class description


class CNetwork(supermod.CNetwork):
    def __init__(self, edgeless=False, src=None, name=None, dtype='AttributeNetwork', location='relpath', fileformat='GEXF', metadata=None, network_surface=None, network_volume=None, network_track=None, network_timeserie=None, network_data=None, description=None):
        super(CNetwork, self).__init__(edgeless, src, name, dtype, location, fileformat, metadata, network_surface, network_volume, network_track, network_timeserie, network_data, description, )
        
    def load(self):
        """ Loads the network into .content """
        self.content = load_data(self)
        
supermod.CNetwork.subclass = CNetwork
# end class CNetwork


class CSurface(supermod.CSurface):
    def __init__(self, src=None, fileformat=None, dtype=None, name=None, location='relpath', description=None, metadata=None):
        super(CSurface, self).__init__(src, fileformat, dtype, name, location, description, metadata, )
supermod.CSurface.subclass = CSurface
# end class CSurface


class CVolume(supermod.CVolume):
    def __init__(self, src=None, fileformat='Nifti1', dtype=None, name=None, location='relpath', description=None, metadata=None):
        super(CVolume, self).__init__(src, fileformat, dtype, name, location, description, metadata, )
        
    def load(self):
        """ Loads the volume into .content """
        self.content = load_data(self)
            
supermod.CVolume.subclass = CVolume
# end class CVolume


class CTrack(supermod.CTrack):
    def __init__(self, src=None, fileformat='TrackVis', name=None, location='relpath', description=None, metadata=None):
        super(CTrack, self).__init__(src, fileformat, name, location, description, metadata, )
supermod.CTrack.subclass = CTrack
# end class CTrack


class CTimeserie(supermod.CTimeserie):
    def __init__(self, src=None, fileformat='HDF5', name=None, location='relpath', description=None, metadata=None):
        super(CTimeserie, self).__init__(src, fileformat, name, location, description, metadata, )
supermod.CTimeserie.subclass = CTimeserie
# end class CTimeserie


class CData(supermod.CData):
    def __init__(self, src=None, fileformat=None, name=None, location='relpath', description=None, metadata=None):
        super(CData, self).__init__(src, fileformat, name, location, description, metadata, )
supermod.CData.subclass = CData
# end class CData


class CScript(supermod.CScript):
    def __init__(self, src=None, type_='Python', name=None, location='relpath', description=None, metadata=None):
        super(CScript, self).__init__(src, type_, name, location, description, metadata, )
supermod.CScript.subclass = CScript
# end class CScript


class CImagestack(supermod.CImagestack):
    def __init__(self, src=None, fileformat=None, pattern=None, name=None, location='relpath', description=None, metadata=None):
        super(CImagestack, self).__init__(src, fileformat, pattern, name, location, description, metadata, )
supermod.CImagestack.subclass = CImagestack
# end class CImagestack


class Metadata(supermod.Metadata):
    def __init__(self, data=None):
        super(Metadata, self).__init__(data, )
supermod.Metadata.subclass = Metadata
# end class Metadata


class data(supermod.data):
    def __init__(self, key=None, valueOf_=None):
        super(data, self).__init__(key, valueOf_, )
supermod.data.subclass = data
# end class data


class NetworkSurface(supermod.NetworkSurface):
    def __init__(self, name=None, metadata=None):
        super(NetworkSurface, self).__init__(name, metadata, )
supermod.NetworkSurface.subclass = NetworkSurface
# end class NetworkSurface


class NetworkVolume(supermod.NetworkVolume):
    def __init__(self, name=None, metadata=None):
        super(NetworkVolume, self).__init__(name, metadata, )
supermod.NetworkVolume.subclass = NetworkVolume
# end class NetworkVolume


class NetworkTrack(supermod.NetworkTrack):
    def __init__(self, name=None, metadata=None):
        super(NetworkTrack, self).__init__(name, metadata, )
supermod.NetworkTrack.subclass = NetworkTrack
# end class NetworkTrack


class NetworkTimeserie(supermod.NetworkTimeserie):
    def __init__(self, name=None, metadata=None):
        super(NetworkTimeserie, self).__init__(name, metadata, )
supermod.NetworkTimeserie.subclass = NetworkTimeserie
# end class NetworkTimeserie


class NetworkData(supermod.NetworkData):
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


