#!/usr/bin/env python

#
# Generated Thu Mar 10 14:06:17 2011 by generateDS.py version 2.4b.
#

import sys

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

class property(supermod.property):
    def __init__(self, name=None, value=None, type_=None, uncertainty=None, unit=None):
        super(property, self).__init__(name, value, type_, uncertainty, unit, )
supermod.property.subclass = property
# end class property


class section(supermod.section):
    def __init__(self, title=None, name=None, type_=None, property=None):
        super(section, self).__init__(title, name, type_, property, )
supermod.section.subclass = section
# end class section


class metadata(supermod.metadata):
    def __init__(self, tag=None, section=None):
        super(metadata, self).__init__(tag, section, )
supermod.metadata.subclass = metadata
# end class metadata


class tag(supermod.tag):
    def __init__(self, key=None, valueOf_=None):
        super(tag, self).__init__(key, valueOf_, )
supermod.tag.subclass = tag
# end class tag


class connectome(supermod.connectome):
    def __init__(self, connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeseries=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        super(connectome, self).__init__(connectome_meta, connectome_network, connectome_surface, connectome_volume, connectome_track, connectome_timeseries, connectome_data, connectome_script, connectome_imagestack, )
supermod.connectome.subclass = connectome
# end class connectome


class CMetadata(supermod.CMetadata):
    def __init__(self, version=None, title=None, creator=None, publisher=None, created=None, modified=None, rights=None, license=None, references=None, relation=None, description=None, generator=None, species=None, email=None, metadata=None):
        super(CMetadata, self).__init__(version, title, creator, publisher, created, modified, rights, license, references, relation, description, generator, species, email, metadata, )
supermod.CMetadata.subclass = CMetadata
# end class CMetadata


class CNetwork(supermod.CNetwork):
    def __init__(self, src=None, dtype='AttributeNetwork', name=None, fileformat='GraphML', metadata=None, description=None):
        super(CNetwork, self).__init__(src, dtype, name, fileformat, metadata, description, )
supermod.CNetwork.subclass = CNetwork
# end class CNetwork


class CSurface(supermod.CSurface):
    def __init__(self, src=None, dtype='Surfaceset', name=None, fileformat=None, description=None, metadata=None):
        super(CSurface, self).__init__(src, dtype, name, fileformat, description, metadata, )
supermod.CSurface.subclass = CSurface
# end class CSurface


class CVolume(supermod.CVolume):
    def __init__(self, src=None, dtype=None, name=None, fileformat='Nifti1', description=None, metadata=None):
        super(CVolume, self).__init__(src, dtype, name, fileformat, description, metadata, )
supermod.CVolume.subclass = CVolume
# end class CVolume


class CTrack(supermod.CTrack):
    def __init__(self, src=None, dtype=None, name=None, fileformat='TrackVis', description=None, metadata=None):
        super(CTrack, self).__init__(src, dtype, name, fileformat, description, metadata, )
supermod.CTrack.subclass = CTrack
# end class CTrack


class CTimeseries(supermod.CTimeseries):
    def __init__(self, src=None, dtype=None, name=None, fileformat='HDF5', description=None, metadata=None):
        super(CTimeseries, self).__init__(src, dtype, name, fileformat, description, metadata, )
supermod.CTimeseries.subclass = CTimeseries
# end class CTimeseries


class CData(supermod.CData):
    def __init__(self, src=None, dtype=None, name=None, fileformat=None, description=None, metadata=None):
        super(CData, self).__init__(src, dtype, name, fileformat, description, metadata, )
supermod.CData.subclass = CData
# end class CData


class CScript(supermod.CScript):
    def __init__(self, src=None, dtype='Python', name=None, fileformat='UTF-8', description=None, metadata=None):
        super(CScript, self).__init__(src, dtype, name, fileformat, description, metadata, )
supermod.CScript.subclass = CScript
# end class CScript


class CImagestack(supermod.CImagestack):
    def __init__(self, src=None, fileformat=None, name=None, pattern=None, description=None, metadata=None):
        super(CImagestack, self).__init__(src, fileformat, name, pattern, description, metadata, )
supermod.CImagestack.subclass = CImagestack
# end class CImagestack


class title(supermod.title):
    def __init__(self, valueOf_=None):
        super(title, self).__init__(valueOf_, )
supermod.title.subclass = title
# end class title


class creator(supermod.creator):
    def __init__(self, valueOf_=None):
        super(creator, self).__init__(valueOf_, )
supermod.creator.subclass = creator
# end class creator


class subject(supermod.subject):
    def __init__(self, valueOf_=None):
        super(subject, self).__init__(valueOf_, )
supermod.subject.subclass = subject
# end class subject


class description(supermod.description):
    def __init__(self, valueOf_=None):
        super(description, self).__init__(valueOf_, )
supermod.description.subclass = description
# end class description


class publisher(supermod.publisher):
    def __init__(self, valueOf_=None):
        super(publisher, self).__init__(valueOf_, )
supermod.publisher.subclass = publisher
# end class publisher


class contributor(supermod.contributor):
    def __init__(self, valueOf_=None):
        super(contributor, self).__init__(valueOf_, )
supermod.contributor.subclass = contributor
# end class contributor


class date(supermod.date):
    def __init__(self, valueOf_=None):
        super(date, self).__init__(valueOf_, )
supermod.date.subclass = date
# end class date


class type_(supermod.type_):
    def __init__(self, valueOf_=None):
        super(type_, self).__init__(valueOf_, )
supermod.type_.subclass = type_
# end class type_


class format(supermod.format):
    def __init__(self, valueOf_=None):
        super(format, self).__init__(valueOf_, )
supermod.format.subclass = format
# end class format


class identifier(supermod.identifier):
    def __init__(self, valueOf_=None):
        super(identifier, self).__init__(valueOf_, )
supermod.identifier.subclass = identifier
# end class identifier


class source(supermod.source):
    def __init__(self, valueOf_=None):
        super(source, self).__init__(valueOf_, )
supermod.source.subclass = source
# end class source


class language(supermod.language):
    def __init__(self, valueOf_=None):
        super(language, self).__init__(valueOf_, )
supermod.language.subclass = language
# end class language


class relation(supermod.relation):
    def __init__(self, valueOf_=None):
        super(relation, self).__init__(valueOf_, )
supermod.relation.subclass = relation
# end class relation


class coverage(supermod.coverage):
    def __init__(self, valueOf_=None):
        super(coverage, self).__init__(valueOf_, )
supermod.coverage.subclass = coverage
# end class coverage


class rights(supermod.rights):
    def __init__(self, valueOf_=None):
        super(rights, self).__init__(valueOf_, )
supermod.rights.subclass = rights
# end class rights


class alternative(supermod.alternative):
    def __init__(self, valueOf_=None):
        super(alternative, self).__init__(valueOf_, )
supermod.alternative.subclass = alternative
# end class alternative


class tableOfContents(supermod.tableOfContents):
    def __init__(self, valueOf_=None):
        super(tableOfContents, self).__init__(valueOf_, )
supermod.tableOfContents.subclass = tableOfContents
# end class tableOfContents


class abstract(supermod.abstract):
    def __init__(self, valueOf_=None):
        super(abstract, self).__init__(valueOf_, )
supermod.abstract.subclass = abstract
# end class abstract


class created(supermod.created):
    def __init__(self, valueOf_=None):
        super(created, self).__init__(valueOf_, )
supermod.created.subclass = created
# end class created


class valid(supermod.valid):
    def __init__(self, valueOf_=None):
        super(valid, self).__init__(valueOf_, )
supermod.valid.subclass = valid
# end class valid


class available(supermod.available):
    def __init__(self, valueOf_=None):
        super(available, self).__init__(valueOf_, )
supermod.available.subclass = available
# end class available


class issued(supermod.issued):
    def __init__(self, valueOf_=None):
        super(issued, self).__init__(valueOf_, )
supermod.issued.subclass = issued
# end class issued


class modified(supermod.modified):
    def __init__(self, valueOf_=None):
        super(modified, self).__init__(valueOf_, )
supermod.modified.subclass = modified
# end class modified


class dateAccepted(supermod.dateAccepted):
    def __init__(self, valueOf_=None):
        super(dateAccepted, self).__init__(valueOf_, )
supermod.dateAccepted.subclass = dateAccepted
# end class dateAccepted


class dateCopyrighted(supermod.dateCopyrighted):
    def __init__(self, valueOf_=None):
        super(dateCopyrighted, self).__init__(valueOf_, )
supermod.dateCopyrighted.subclass = dateCopyrighted
# end class dateCopyrighted


class dateSubmitted(supermod.dateSubmitted):
    def __init__(self, valueOf_=None):
        super(dateSubmitted, self).__init__(valueOf_, )
supermod.dateSubmitted.subclass = dateSubmitted
# end class dateSubmitted


class extent(supermod.extent):
    def __init__(self, valueOf_=None):
        super(extent, self).__init__(valueOf_, )
supermod.extent.subclass = extent
# end class extent


class medium(supermod.medium):
    def __init__(self, valueOf_=None):
        super(medium, self).__init__(valueOf_, )
supermod.medium.subclass = medium
# end class medium


class isVersionOf(supermod.isVersionOf):
    def __init__(self, valueOf_=None):
        super(isVersionOf, self).__init__(valueOf_, )
supermod.isVersionOf.subclass = isVersionOf
# end class isVersionOf


class hasVersion(supermod.hasVersion):
    def __init__(self, valueOf_=None):
        super(hasVersion, self).__init__(valueOf_, )
supermod.hasVersion.subclass = hasVersion
# end class hasVersion


class isReplacedBy(supermod.isReplacedBy):
    def __init__(self, valueOf_=None):
        super(isReplacedBy, self).__init__(valueOf_, )
supermod.isReplacedBy.subclass = isReplacedBy
# end class isReplacedBy


class replaces(supermod.replaces):
    def __init__(self, valueOf_=None):
        super(replaces, self).__init__(valueOf_, )
supermod.replaces.subclass = replaces
# end class replaces


class isRequiredBy(supermod.isRequiredBy):
    def __init__(self, valueOf_=None):
        super(isRequiredBy, self).__init__(valueOf_, )
supermod.isRequiredBy.subclass = isRequiredBy
# end class isRequiredBy


class requires(supermod.requires):
    def __init__(self, valueOf_=None):
        super(requires, self).__init__(valueOf_, )
supermod.requires.subclass = requires
# end class requires


class isPartOf(supermod.isPartOf):
    def __init__(self, valueOf_=None):
        super(isPartOf, self).__init__(valueOf_, )
supermod.isPartOf.subclass = isPartOf
# end class isPartOf


class hasPart(supermod.hasPart):
    def __init__(self, valueOf_=None):
        super(hasPart, self).__init__(valueOf_, )
supermod.hasPart.subclass = hasPart
# end class hasPart


class isReferencedBy(supermod.isReferencedBy):
    def __init__(self, valueOf_=None):
        super(isReferencedBy, self).__init__(valueOf_, )
supermod.isReferencedBy.subclass = isReferencedBy
# end class isReferencedBy


class references(supermod.references):
    def __init__(self, valueOf_=None):
        super(references, self).__init__(valueOf_, )
supermod.references.subclass = references
# end class references


class isFormatOf(supermod.isFormatOf):
    def __init__(self, valueOf_=None):
        super(isFormatOf, self).__init__(valueOf_, )
supermod.isFormatOf.subclass = isFormatOf
# end class isFormatOf


class hasFormat(supermod.hasFormat):
    def __init__(self, valueOf_=None):
        super(hasFormat, self).__init__(valueOf_, )
supermod.hasFormat.subclass = hasFormat
# end class hasFormat


class conformsTo(supermod.conformsTo):
    def __init__(self, valueOf_=None):
        super(conformsTo, self).__init__(valueOf_, )
supermod.conformsTo.subclass = conformsTo
# end class conformsTo


class spatial(supermod.spatial):
    def __init__(self, valueOf_=None):
        super(spatial, self).__init__(valueOf_, )
supermod.spatial.subclass = spatial
# end class spatial


class temporal(supermod.temporal):
    def __init__(self, valueOf_=None):
        super(temporal, self).__init__(valueOf_, )
supermod.temporal.subclass = temporal
# end class temporal


class audience(supermod.audience):
    def __init__(self, valueOf_=None):
        super(audience, self).__init__(valueOf_, )
supermod.audience.subclass = audience
# end class audience


class accrualMethod(supermod.accrualMethod):
    def __init__(self, valueOf_=None):
        super(accrualMethod, self).__init__(valueOf_, )
supermod.accrualMethod.subclass = accrualMethod
# end class accrualMethod


class accrualPeriodicity(supermod.accrualPeriodicity):
    def __init__(self, valueOf_=None):
        super(accrualPeriodicity, self).__init__(valueOf_, )
supermod.accrualPeriodicity.subclass = accrualPeriodicity
# end class accrualPeriodicity


class accrualPolicy(supermod.accrualPolicy):
    def __init__(self, valueOf_=None):
        super(accrualPolicy, self).__init__(valueOf_, )
supermod.accrualPolicy.subclass = accrualPolicy
# end class accrualPolicy


class instructionalMethod(supermod.instructionalMethod):
    def __init__(self, valueOf_=None):
        super(instructionalMethod, self).__init__(valueOf_, )
supermod.instructionalMethod.subclass = instructionalMethod
# end class instructionalMethod


class provenance(supermod.provenance):
    def __init__(self, valueOf_=None):
        super(provenance, self).__init__(valueOf_, )
supermod.provenance.subclass = provenance
# end class provenance


class rightsHolder(supermod.rightsHolder):
    def __init__(self, valueOf_=None):
        super(rightsHolder, self).__init__(valueOf_, )
supermod.rightsHolder.subclass = rightsHolder
# end class rightsHolder


class mediator(supermod.mediator):
    def __init__(self, valueOf_=None):
        super(mediator, self).__init__(valueOf_, )
supermod.mediator.subclass = mediator
# end class mediator


class educationLevel(supermod.educationLevel):
    def __init__(self, valueOf_=None):
        super(educationLevel, self).__init__(valueOf_, )
supermod.educationLevel.subclass = educationLevel
# end class educationLevel


class accessRights(supermod.accessRights):
    def __init__(self, valueOf_=None):
        super(accessRights, self).__init__(valueOf_, )
supermod.accessRights.subclass = accessRights
# end class accessRights


class license(supermod.license):
    def __init__(self, valueOf_=None):
        super(license, self).__init__(valueOf_, )
supermod.license.subclass = license
# end class license


class bibliographicCitation(supermod.bibliographicCitation):
    def __init__(self, valueOf_=None):
        super(bibliographicCitation, self).__init__(valueOf_, )
supermod.bibliographicCitation.subclass = bibliographicCitation
# end class bibliographicCitation


class elementOrRefinementContainer(supermod.elementOrRefinementContainer):
    def __init__(self, any=None):
        super(elementOrRefinementContainer, self).__init__(any, )
supermod.elementOrRefinementContainer.subclass = elementOrRefinementContainer
# end class elementOrRefinementContainer


class SimpleLiteral(supermod.SimpleLiteral):
    def __init__(self, lang=None, valueOf_=None):
        super(SimpleLiteral, self).__init__(lang, valueOf_, )
supermod.SimpleLiteral.subclass = SimpleLiteral
# end class SimpleLiteral


class elementContainer(supermod.elementContainer):
    def __init__(self, any=None):
        super(elementContainer, self).__init__(any, )
supermod.elementContainer.subclass = elementContainer
# end class elementContainer


class TGN(supermod.TGN):
    def __init__(self, lang=None, valueOf_=None):
        super(TGN, self).__init__(lang, valueOf_, )
supermod.TGN.subclass = TGN
# end class TGN


class Box(supermod.Box):
    def __init__(self, lang=None, valueOf_=None):
        super(Box, self).__init__(lang, valueOf_, )
supermod.Box.subclass = Box
# end class Box


class ISO3166(supermod.ISO3166):
    def __init__(self, lang=None, valueOf_=None):
        super(ISO3166, self).__init__(lang, valueOf_, )
supermod.ISO3166.subclass = ISO3166
# end class ISO3166


class Point(supermod.Point):
    def __init__(self, lang=None, valueOf_=None):
        super(Point, self).__init__(lang, valueOf_, )
supermod.Point.subclass = Point
# end class Point


class RFC4646(supermod.RFC4646):
    def __init__(self, lang=None, valueOf_=None):
        super(RFC4646, self).__init__(lang, valueOf_, )
supermod.RFC4646.subclass = RFC4646
# end class RFC4646


class RFC3066(supermod.RFC3066):
    def __init__(self, lang=None, valueOf_=None):
        super(RFC3066, self).__init__(lang, valueOf_, )
supermod.RFC3066.subclass = RFC3066
# end class RFC3066


class RFC1766(supermod.RFC1766):
    def __init__(self, lang=None, valueOf_=None):
        super(RFC1766, self).__init__(lang, valueOf_, )
supermod.RFC1766.subclass = RFC1766
# end class RFC1766


class ISO639_3(supermod.ISO639_3):
    def __init__(self, lang=None, valueOf_=None):
        super(ISO639_3, self).__init__(lang, valueOf_, )
supermod.ISO639_3.subclass = ISO639_3
# end class ISO639_3


class ISO639_2(supermod.ISO639_2):
    def __init__(self, lang=None, valueOf_=None):
        super(ISO639_2, self).__init__(lang, valueOf_, )
supermod.ISO639_2.subclass = ISO639_2
# end class ISO639_2


class URI(supermod.URI):
    def __init__(self, lang=None, valueOf_=None):
        super(URI, self).__init__(lang, valueOf_, )
supermod.URI.subclass = URI
# end class URI


class IMT(supermod.IMT):
    def __init__(self, lang=None, valueOf_=None):
        super(IMT, self).__init__(lang, valueOf_, )
supermod.IMT.subclass = IMT
# end class IMT


class DCMIType(supermod.DCMIType):
    def __init__(self, lang=None, valueOf_=None):
        super(DCMIType, self).__init__(lang, valueOf_, )
supermod.DCMIType.subclass = DCMIType
# end class DCMIType


class W3CDTF(supermod.W3CDTF):
    def __init__(self, lang=None, valueOf_=None):
        super(W3CDTF, self).__init__(lang, valueOf_, )
supermod.W3CDTF.subclass = W3CDTF
# end class W3CDTF


class Period(supermod.Period):
    def __init__(self, lang=None, valueOf_=None):
        super(Period, self).__init__(lang, valueOf_, )
supermod.Period.subclass = Period
# end class Period


class UDC(supermod.UDC):
    def __init__(self, lang=None, valueOf_=None):
        super(UDC, self).__init__(lang, valueOf_, )
supermod.UDC.subclass = UDC
# end class UDC


class LCC(supermod.LCC):
    def __init__(self, lang=None, valueOf_=None):
        super(LCC, self).__init__(lang, valueOf_, )
supermod.LCC.subclass = LCC
# end class LCC


class DDC(supermod.DDC):
    def __init__(self, lang=None, valueOf_=None):
        super(DDC, self).__init__(lang, valueOf_, )
supermod.DDC.subclass = DDC
# end class DDC


class MESH(supermod.MESH):
    def __init__(self, lang=None, valueOf_=None):
        super(MESH, self).__init__(lang, valueOf_, )
supermod.MESH.subclass = MESH
# end class MESH


class LCSH(supermod.LCSH):
    def __init__(self, lang=None, valueOf_=None):
        super(LCSH, self).__init__(lang, valueOf_, )
supermod.LCSH.subclass = LCSH
# end class LCSH



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
    if rootClass is None:
        rootTag = 'property'
        rootClass = supermod.property
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='xmlns:cml="http://www.connectomics.org/cff-2" xmlns:dcterms="http://purl.org/dc/terms/"')
    doc = None
    return rootObj


def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'property'
        rootClass = supermod.property
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='xmlns:cml="http://www.connectomics.org/cff-2" xmlns:dcterms="http://purl.org/dc/terms/"')
    return rootObj


def parseLiteral(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'property'
        rootClass = supermod.property
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from cff import *\n\n')
    sys.stdout.write('import cff as model_\n\n')
    sys.stdout.write('rootObj = model_.property(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="property")
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


