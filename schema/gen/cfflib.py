#!/usr/bin/env python

#
# Generated Tue Jul 27 12:06:53 2010 by generateDS.py version 2.1a.
#

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
    def __init__(self, connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeserie=None):
        super(connectome, self).__init__(connectome_meta, connectome_network, connectome_surface, connectome_volume, connectome_track, connectome_timeserie, )
supermod.connectome.subclass = connectome
# end class connectome


class CMetadata(supermod.CMetadata):
    def __init__(self, version=None, generator=None, initial_creator=None, institution=None, creation_date=None, modification_date=None, name=None, species=None, legal_notice=None, reference=None, url=None, description=None, metadata=None):
        super(CMetadata, self).__init__(version, generator, initial_creator, institution, creation_date, modification_date, name, species, legal_notice, reference, url, description, metadata, )
supermod.CMetadata.subclass = CMetadata
# end class CMetadata


class networkstype(supermod.networkstype):
    def __init__(self, directed=None, src=None, name=None, network_metadata=None, network_surface=None, network_volume=None, network_track=None, network_timeserie=None, description=None):
        super(networkstype, self).__init__(directed, src, name, network_metadata, network_surface, network_volume, network_track, network_timeserie, description, )
supermod.networkstype.subclass = networkstype
# end class networkstype


class surfacestype(supermod.surfacestype):
    def __init__(self, src=None, dtype=None, name=None, fileformat=None, description=None):
        super(surfacestype, self).__init__(src, dtype, name, fileformat, description, )
supermod.surfacestype.subclass = surfacestype
# end class surfacestype


class volumestype(supermod.volumestype):
    def __init__(self, src=None, dtype=None, name=None, fileformat=None, description=None):
        super(volumestype, self).__init__(src, dtype, name, fileformat, description, )
supermod.volumestype.subclass = volumestype
# end class volumestype


class CTrack(supermod.CTrack):
    def __init__(self, src=None, name=None, fileformat=None, description=None):
        super(CTrack, self).__init__(src, name, fileformat, description, )
supermod.CTrack.subclass = CTrack
# end class CTrack


class CTimeserie(supermod.CTimeserie):
    def __init__(self, src=None, name=None, fileformat=None, description=None):
        super(CTimeserie, self).__init__(src, name, fileformat, description, )
supermod.CTimeserie.subclass = CTimeserie
# end class CTimeserie


class moremetadatatype(supermod.moremetadatatype):
    def __init__(self, data=None):
        super(moremetadatatype, self).__init__(data, )
supermod.moremetadatatype.subclass = moremetadatatype
# end class moremetadatatype


class data(supermod.data):
    def __init__(self, key=None, valueOf_=None):
        super(data, self).__init__(key, valueOf_, )
supermod.data.subclass = data
# end class data


class networksurfacetype(supermod.networksurfacetype):
    def __init__(self, labelid=None, name=None, labelname=None, valueOf_=None):
        super(networksurfacetype, self).__init__(labelid, name, labelname, valueOf_, )
supermod.networksurfacetype.subclass = networksurfacetype
# end class networksurfacetype


class networkvolumetype(supermod.networkvolumetype):
    def __init__(self, segmentationname=None, name=None, valueOf_=None):
        super(networkvolumetype, self).__init__(segmentationname, name, valueOf_, )
supermod.networkvolumetype.subclass = networkvolumetype
# end class networkvolumetype


class networktracktype(supermod.networktracktype):
    def __init__(self, name=None, valueOf_=None):
        super(networktracktype, self).__init__(name, valueOf_, )
supermod.networktracktype.subclass = networktracktype
# end class networktracktype


class networktimeserietype(supermod.networktimeserietype):
    def __init__(self, name=None, valueOf_=None):
        super(networktimeserietype, self).__init__(name, valueOf_, )
supermod.networktimeserietype.subclass = networktimeserietype
# end class networktimeserietype



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
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
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


