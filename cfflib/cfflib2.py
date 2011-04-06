#!/usr/bin/env python

#
# Generated Tue Jan 25 11:45:14 2011 by generateDS.py version 2.3b.
#

### My Imports

import warnings
from util import *
from cff import showIndent, quote_xml, tag
import tempfile
import os.path as op
import os
has_pyxnat = True
try:
    import pyxnat    
except:
    has_pyxnat = False


DEBUG_msg = False

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

class metadata(supermod.metadata):
    def __init__(self, tag=None, section=None):
        super(metadata, self).__init__(tag, section, )
        
    def get_tags_as_dictionary(self):
        """Return the metadata tags as a dictionary"""
        dat = self.get_tag()
        ret = {}
        for ele in dat:
            ret[ele.key] = ele.valueOf_
        return ret
    
    def set_tags_with_dictionary(self, dictionary):
        """Set the metadata with a dictionary"""
        tags = self.get_tag()
        if len(dictionary) == 0:
            return
        for k in dictionary:
            test = False
            # check if the key already exists
            for ele in tags:
                if ele.key == k:
                    # always change the value to a string
                    ele.valueOf_ = str(dictionary[k])
                    test = True
            if not test:
                # append to tags
                mytag = tag(str(k), str(dictionary[k]))
                self.add_tag(mytag)
                
                
supermod.metadata.subclass = metadata

class connectome(supermod.connectome):
    """The connectome object is the main object of this format.
    It contains CMetadata, and it can contain some CData, CNetwork,
    CSurface, CTimeserie, CTrack, CVolume, CScript or CImagestack
    objects that are referred to as CObjects.
    
    It is possible to store to a simple connectome markup .cml file
    with appropriate relative references to the data files, or to a 
    compressed (zipped) connectome file with ending .cff containing all
    source data objects. """
    
    def __init__(self, title = None, connectome_meta=None, connectome_network=None, connectome_surface=None, connectome_volume=None, connectome_track=None, connectome_timeseries=None, connectome_data=None, connectome_script=None, connectome_imagestack=None):
        """Create a new connectome object
        
        See also
        --------
        CMetadata, CNetwork, CSurface, CVolume, CTrack, CTimeserie, CData, CScript and CImagestack
    
        """
        super(connectome, self).__init__(connectome_meta, connectome_network, connectome_surface, connectome_volume, connectome_track, connectome_timeseries, connectome_data, connectome_script, connectome_imagestack, )

        # add parent reference to all children
        self._update_parent_reference()
        
        # add some useful attributes to the save functions
        self.iszip = False
        
        # set default title
        if title is None:
            title = 'myconnectome'
        
        self._xnat_interface = None
        
        # Default CMetadata
        if connectome_meta is None:
            self.connectome_meta = CMetadata()
            self.connectome_meta.set_title(title)
        
    def set_xnat_connection(self, interface = None):
        """ Setup this connectome container to push and pull from XNAT
        
        Parameters
        ----------
        connection_interface : { pxnat.Interface, dict }
            Set the PyXNAT interface or a dictionary
            with keys server, user, password, cachedir (optional)
            
        """
        
        if not has_pyxnat:
            raise Exception('You need to install PyXNAT to use this functionality')
        
        if isinstance(interface, dict):
            self._xnat_interface = pyxnat.Interface(**interface)
        elif isinstance(interface, pyxnat.Interface):
            self._xnat_interface = interface
        else:
            self._xnat_interface = None

        if DEBUG_msg:
            print("Connected to XNAT Server")
            
    def add_connectome_object(self, cobj):
        """ Adds an arbitrary connectome object to the container depending
        its type. This needs to be a valid connectome object
        """
        
        cname = cobj.__class__.__name__
        
        if cname == 'CNetwork':
            self.add_connectome_network(cobj)            
        elif cname == 'CSurface':
            self.add_connectome_surface(cobj)
        elif cname == 'CVolume':
            self.add_connectome_volume(cobj)
        elif cname == 'CTrack':
            self.add_connectome_track(cobj)
        elif cname == 'CData':
            self.add_connectome_data(cobj)
        elif cname == 'CScript':
            self.add_connectome_script(cobj)
        elif cname == 'CTimeseries':
            self.add_connectome_timeseries(cobj)

            
        # XXX> to be competed
        
    def pull(self, projectid, subjectid, experimentid, storagepath):
        """ Pull the complete set of files from a subject and experiment """
   
        absstoragepath = op.abspath(storagepath)
        
        # we define the unique experimental id based on the user input
        subj_id = '%s_%s' % (projectid, subjectid)
        exp_id = '%s_%s' % (subj_id, experimentid)
        
        experiment_uri = '/projects/%s/subjects/%s/experiments/%s' % (projectid, subj_id, exp_id)
        metacml_uri = '%s/resources/meta/files/meta.cml' % experiment_uri
        
        # download meta.cml
        metacmlpath = op.join(absstoragepath, 'meta.cml')
        meta_uri = '%s/resources/meta/files/meta.cml' % experiment_uri
        self._xnat_interface.select(meta_uri).get(metacmlpath)
            
        # parse meta.cml
        f = open(metacmlpath, 'rb')
        remote_connectome = parseString(f.read())
        f.close()
        if DEBUG_msg:
            print "Remote connectome", remote_connectome.to_xml()
        
        # loop over objects and download them to pyxnat cache / or path 
        for ele in remote_connectome.get_all():
            if DEBUG_msg:
                print("Downloading connectome object")
                ele.print_summary()
                
            cobj_uri = '%s/assessors/%s/out/resources/data/files/%s' % (
                    experiment_uri, 
                    '%s_%s' % (exp_id, ele.__class__.__name__),
                    quote_for_xnat(ele.name)
                    )
            # download file
            # does file folder exist?
            eleobjfolderfname = op.join(absstoragepath, ele.get_unique_relpath())
            
            if not op.exists(op.split(eleobjfolderfname)[0]):
                os.makedirs( op.split(eleobjfolderfname)[0] )
            
            self._xnat_interface.select(cobj_uri).get(eleobjfolderfname)

        # update current connectome container
        print("=============")
        print("You can load the pulled connectome file with:")
        print("import cfflib as cf; mycon = cf.load('%s')" % op.join(absstoragepath, 'meta.cml'))
        print("=============")
        
        return True
        
            
    def push(self, projectid, subjectid, experimentid, overwrite = False):
        """ Push all the connectome objects to the remote XNAT server.
        
        Parameters
        ----------
        projectid : string
            The id of the project, has to be unique across an XNAT server
        subjectid : string
            The id of the subject
        experimentid : string
            The id of the experiment
        overwrite : boolean
            Overwrite remote version of the connectome object with
            the connectome object contained in the local connectome container
            
        """
        def _push_metacml(experiment_uri):
            _, fname = tempfile.mkstemp()
            f=open(fname, 'wb')
            f.write(self.to_xml())
            f.close()

            # finally update remote meta.cml
            meta_uri = '%s/resources/meta/files/meta.cml' % experiment_uri
            self._xnat_interface.select(meta_uri).insert(fname, experiments = 'xnat:imageSessionData', \
                        use_label=True)


        if self._xnat_interface is None:
            raise Exception('You need to set the XNAT connection with set_xnat_connection')

        # we define the unique experimental id based on the user input
        subj_id = '%s_%s' % (projectid, subjectid)
        exp_id = '%s_%s' % (subj_id, experimentid)
        
        experiment_uri = '/projects/%s/subjects/%s/experiments/%s' % (projectid, subj_id, exp_id)
        metacml_uri = '%s/resources/meta/files/meta.cml' % experiment_uri
                
        # does the experiment exists                    
        if self._xnat_interface.select(metacml_uri).exists():
            # it exists, just download it
            self._remote_metacml = self._xnat_interface.select(metacml_uri).get()
            
            # compare it to the local object
            remote_metacml = open(self._remote_metacml, 'rb')
            
            remote_connectome = parseString(remote_metacml.read())
            
            # loop over local connectome objects and check if the exists remotely
            all_local_cobj = self.get_all()
            
            # connectome objects we need to add to the remote metacml
            push_objects = []
            
            for ele in all_local_cobj:
                if DEBUG_msg:
                    print "Working on element %s" % ele.name
                if (ele in remote_connectome.get_all() and overwrite) or \
                    not ele in remote_connectome.get_all():
                    if DEBUG_msg:
                        print "We push element %s" % ele.name
                        print "Element in remote?" + str(ele in remote_connectome.get_all())
                    
                    # push connectome object to remote
                    cobj_uri = '%s/assessors/%s/out/resources/data/files/%s' % (
                        experiment_uri, 
                        '%s_%s' % (exp_id, ele.__class__.__name__),
                        quote_for_xnat(ele.name)
                        )
                    # insert data file to xnat
                    self._xnat_interface.select(cobj_uri).insert(ele.get_abs_path(), experiments = 'xnat:imageSessionData', \
                        assessors = 'xnat:imageAssessorData', use_label=True)
                    # add element for updating metacml later on the remote
                    push_objects.append(ele)
                    
                    
                else:
                    # we do not push
                    if DEBUG_msg:
                        print "We do nothing with element %s (already on remote and no overwrite)" % ele.name
                    
                    
            # synchronize meta_cml
            # we need to retrieve the remote connectome objects and add it to the
            # local if they no not yet exists
            for el in remote_connectome.get_all():
                if not el in self.get_all():
                    self.add_connectome_object(el)
                    
            #for el in push_objects:
                # add all push_objects to remote meta_cml
             #   remote_connectome.add_connectome_object(el)
            
            # update cmetadata (overwriting remote with local)
            remote_connectome.connectome_meta = self.connectome_meta
            
            _push_metacml(experiment_uri)

            if DEBUG_msg:
                print "Current local connectome container", self.to_xml()
                print "Current remote connectome container", remote_connectome.to_xml()
                print "Current push objects", push_objects
            
        else:
            # create meta.cml

            # loop over local connectome objects and check if the exists remotely
            all_local_cobj = self.get_all()
            
            for ele in all_local_cobj:
                print "We push element %s" % ele.name
                
                # push connectome object to remote
                cobj_uri = '%s/assessors/%s/out/resources/data/files/%s' % (
                    experiment_uri, 
                    '%s_%s' % (exp_id, ele.__class__.__name__),
                    quote_for_xnat(ele.name)
                    )
                # insert data file to xnat
                self._xnat_interface.select(cobj_uri).insert(ele.get_abs_path(), experiments = 'xnat:imageSessionData', \
                        assessors = 'xnat:imageAssessorData', use_label=True)

            # push the current connectome object to remote
            _push_metacml(experiment_uri)
            
        
    def get_all(self):
        """ Return all connectome objects as a list
                    
        Examples
        --------
        >>> allcobj = myConnectome.get_all()
        >>> first_ele = allcobj[0]

        """        
        return self.connectome_network + self.connectome_surface + \
                self.connectome_volume + self.connectome_track + \
                self.connectome_timeseries + self.connectome_data + \
                self.connectome_script + self.connectome_imagestack

    
    def get_by_name(self, name):
        """ Return the list of connectome object(s) that have the given name
        
        Parameters
        ----------
        name : string or list of strings
            name(s) of the requested object(s)
            
        Examples
        --------
        >>> myConnectome.get_by_name('my first network')

        """        
        if isinstance(name, list):
            ret = []
            all_cobj = self.get_all()             
            for ele in all_cobj:
                if ele.name in name:
                    ret.append(ele)
            return ret
        else: 
            #n = self.get_normalised_name(name)
            all_cobj = self.get_all()             
            for ele in all_cobj:
                if name == ele.name:
                    return ele
            return None

    def get_by_src(self, src):
        """ Return the list of connectome object(s) that have the given source path

        Parameters
        ----------
        src : string or list of strings
            source paths(s) of the requested object(s)

        """
        if isinstance(src, list):
            ret = []
            all_cobj = self.get_all()
            for ele in all_cobj:
                if ele.src in src:
                    ret.append(ele)
            return ret
        else:
            all_cobj = self.get_all()
            for ele in all_cobj:
                if src == ele.src:
                    return ele
            return None
        
    def check_file_in_cff(self):
        """Checks if the files described in the meta.cml are contained in the connectome zip file."""  

        if not self.iszip:
            all_cobj = self.get_all()
            for ele in all_cobj:
                if not op.exists(ele.src):
                    msg = "Element with name %s and source path has no valid reference to an existing file." % (ele.name, ele.src)
                    raise Exception(msg)
        else:
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
        check_names_unique, connectome
        """
        n = self.get_normalised_name(name)
        all_cobj = self.get_all()
        namelist = []
        for ele in all_cobj:
            namelist.append(self.get_normalised_name(ele.name))
        if n in namelist:
            return False
        else:
            return True
    
    def get_unique_cff_name(self):
        """Return a unique connectome file title"""
        
        # create random number to append to the name
        # to enable multiple people to access the files
        import random
        rndstr = str(int(random.random()*1000000))
        n = self.get_connectome_meta().get_title()
        n = n.lower()
        n = n.replace(' ', '_') + rndstr
        return n
        
    def get_normalised_name(self, name):
        """Return a normalised name, without space and in lower case
        
        Parameters
        ----------
        name : string,
            the name to be normalised
            
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
        """Updates the parent reference to the connectome file super-object"""

        all_cobj = self.get_all() 
        
        for ele in all_cobj:
            ele.parent_cfile = self

    def to_xml(self):
        from StringIO import StringIO
        re = StringIO()
        re.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        ns = """xmlns="http://www.connectomics.org/cff-2"
      xmlns:cml="http://www.connectomics.org/cff-2"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:dcterms="http://purl.org/dc/terms/" """

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
        cmeta : CMetadata
            the connectome metadata to add to the connectome object
             
        """
                
        # Check if the name is set     
        if cmeta.title is None or cmeta.title == '':
            raise Exception('A title is required.')
        
        self.connectome_meta = cmeta
    
    # CNetwork
    def add_connectome_network_from_nxgraph(self, name, nxGraph, dtype='AttributeNetwork', fileformat='NXGPickle'):
        """Add a new CNetwork from the given NetworkX graph object to the connectome.
        
        Parameters
        ----------
        name : string,
            a unique name for the NetworkX graph to add to the connectome object
        nxGraph : NetworkX,
            a NetworkX graph object
        dtype : AttributeNetwork,
            the data type of this CNetwork
        fileformat : NXGPickle,
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
        # need to update the reference to the parent connectome file
        self._update_parent_reference()
    
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
        # need to update the reference to the parent connectome file
        self._update_parent_reference()

    def add_connectome_script_from_file(self, name, filename, dtype = 'Python', fileformat = 'UTF-8'):
        """ Add a CScript from a file """
        
        if not self.is_name_unique(name):
            raise Exception('The name is not unique.')
        
        s = CScript.create_from_file(name, filename, dtype= dtype, fileformat = dtype)
        self.add_connectome_script(s)
        # need to update the reference to the parent connectome file
        self._update_parent_reference()

        
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
        
        # update sources for correct storing
        if op.exists(cnet.src):
            cnet.tmpsrc = cnet.src
            cnet.src = cnet.get_unique_relpath()
        
        # need to update the reference to the parent connectome file
        self._update_parent_reference()

        
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
        
        # update sources for correct storing
        if op.exists(cvol.src):
            cvol.tmpsrc = cvol.src
            cvol.src = cvol.get_unique_relpath()
        
        # need to update the reference to the parent connectome file
        self._update_parent_reference()
        
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
        
        # update sources for correct storing
        if op.exists(csurf.src):
            csurf.tmpsrc = csurf.src
            csurf.src = csurf.get_unique_relpath()
        
        # need to update the reference to the parent connectome file
        self._update_parent_reference()
    
    def add_connectome_track(self, ctrack):
        """Add the given CTrack to the connectome object.
        
        Parameters
        ----------
        ctrack : CTrack,
            the connectome track to add to the connectome, the CTrack name have to be unique.
            
        """
              
        # Check if the name is set     
        if ctrack.name is None or ctrack.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(ctrack.name):
            raise Exception('The name is not unique.')
        
        self.connectome_track.append(ctrack)
        
        # update sources for correct storing
        if op.exists(ctrack.src):
            ctrack.tmpsrc = ctrack.src
            ctrack.src = ctrack.get_unique_relpath()
        
        # need to update the reference to the parent connectome file
        self._update_parent_reference()

    def add_connectome_data(self, cda):
        """Add the given CData to the connectome object.
        
        Parameters
        ----------
        cda : CData,
            the connectome data to add to the connectome, the CData name have to be unique.
            
        """
              
        # Check if the name is set     
        if cda.name is None or cda.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(cda.name):
            raise Exception('The name is not unique.')
        
        self.connectome_data.append(cda)
        
        # update sources for correct storing
        if op.exists(cda.src):
            cda.tmpsrc = cda.src
            cda.src = cda.get_unique_relpath()      
        
        # need to update the reference to the parent connectome file
        self._update_parent_reference()
        
    def add_connectome_script(self, cscri):
        """Add the given CScript to the connectome object.
        
        Parameters
        ----------
        cscri : CScript,
            the connectome script to add to the connectome, the CScript name have to be unique.
            
        """
              
        # Check if the name is set     
        if cscri.name is None or cscri.name == '':
            raise Exception('A name is required.')
        
        # Check if the name is unique
        if not self.is_name_unique(cscri.name):
            raise Exception('The name is not unique.')
        
        self.connectome_script.append(cscri)
        
        # update sources for correct storing
        if op.exists(cscri.src):
            cscri.tmpsrc = cscri.src
            cscri.src = cscri.get_unique_relpath()      
        
        # need to update the reference to the parent connectome file
        self._update_parent_reference()
        
    # Print out a summary of the connectome
    def print_summary(self):
        """Print a summary of the connectome"""
        
        # Intro
        s = '#'*60
        s+= '\n# connectome object'
        
        # Statistics
        s+= '\n#\n# Statistics\n# '+'='*56+' #'
        s+= '\n# '+str(len(self.get_connectome_network()))+' CNetwork'
        s+= '\n# '+str(len(self.get_connectome_volume()))+' CVolume'
        s+= '\n# '+str(len(self.get_connectome_track()))+' CTrack'
        s+= '\n# '+str(len(self.get_connectome_surface()))+' CSurface'
        s+= '\n# '+str(len(self.get_connectome_timeseries()))+' CTimeserie'
        s+= '\n# '+str(len(self.get_connectome_script()))+' CScript'
        s+= '\n# '+str(len(self.get_connectome_data()))+' CData'
        s+= '\n# '+str(len(self.get_connectome_imagestack()))+' CImagestack'
        
        # CMetadata
        s+= '\n#\n# CMetadata\n# '+'='*56+' #'
        cm = self.get_connectome_meta()
        s+= '\n# title : '+cm.get_title()  
        if not cm.get_species() is None and isinstance(cm.get_species(), str):
            s+= '\n# species : '+cm.get_species() 
        if not cm.get_description() is None and isinstance(cm.get_description(), str):
            s+= '\n# description : '+cm.get_description() 
        if not cm.get_creator() is None and isinstance(cm.get_creator(), str):
            s+= '\n# creator : '+cm.get_creator() 
        if not cm.get_email() is None and isinstance(cm.get_email(), str):
            s+= '\n# email : '+cm.get_email() 
        if not cm.get_created() is None and isinstance(cm.get_created(), str):
            s+= '\n# creation date : '+cm.get_created() 
        if not cm.get_modified() is None and isinstance(cm.get_modified(), str):
            s+= '\n# modification date : '+cm.get_modified() 
        if not cm.get_generator() is None and isinstance(cm.get_generator(), str):
            s+= '\n# generator : '+cm.get_generator() 
        if not cm.get_version() is None and isinstance(cm.get_version(), str):
            s+= '\n# cff version : '+cm.get_version()
        if not cm.get_license() is None and isinstance(cm.get_license(), str):
            s+= '\n# license : '+cm.get_license() 
        if not cm.get_rights() is None and isinstance(cm.get_rights(), str):
            s+= '\n# rights : '+cm.get_rights()
        if not cm.get_publisher() is None and isinstance(cm.get_publisher(), str):
            s+= '\n# publisher : '+cm.get_publisher() 
        if not cm.get_references() is None and isinstance(cm.get_references(), str):
            s+= '\n# references : '+cm.get_references() 
        if not cm.get_relation() is None and isinstance(cm.get_relation(), str):
            s+= '\n# relation : '+cm.get_relation() 
        # CNetwork
        if len(self.get_connectome_network()) > 0:
            s+= '\n#\n# CNetwork\n# '+'='*56+' #'
            for i in self.get_connectome_network():
                s+= i.print_summary(False)
                
        # CVolume
        if len(self.get_connectome_volume()) > 0:
            s+= '\n#\n# CVolume\n# '+'='*56+' #'
            for i in self.get_connectome_volume():
                s+= i.print_summary(False)
            
        # CTrack
        if len(self.get_connectome_track()) > 0:
            s+= '\n#\n# CTrack\n# '+'='*56+' #'
            for i in self.get_connectome_track():
                s+= i.print_summary(False)
            
        # CSurface
        if len(self.get_connectome_surface()) > 0:
            s+= '\n#\n# CSurface\n# '+'='*56+' #'
            for i in self.get_connectome_surface():
                s+= i.print_summary(False)
            
        # CTimeserie
        if len(self.get_connectome_timeseries()) > 0:
            s+= '\n#\n# CTimeseries\n# '+'='*56+' #'
            for i in self.get_connectome_timeseries():
                s+= i.print_summary(False)
            
        # CScript
        if len(self.get_connectome_script()) > 0:
            s+= '\n#\n# CScript\n# '+'='*56+' #'
            for i in self.get_connectome_script():
                s+= i.print_summary(False)
            
        # CData
        if len(self.get_connectome_data()) > 0:
            s+= '\n#\n# CData\n# '+'='*56+' #'
            for i in self.get_connectome_data():
                s+= i.print_summary(False)
            
        # CImagestack
        if len(self.get_connectome_imagestack()) > 0:
            s+= '\n#\n# CImagestack\n# '+'='*56+' #'
            for i in self.get_connectome_imagestack():
                s+= i.print_summary(False)
            
        s+= '\n'+'#'*60
        print(s)
        
        
supermod.connectome.subclass = connectome
# end class connectome


class CMetadata(supermod.CMetadata):
    """Specific metadata to the connectome. The name is the name of the connectome. 
    The version and the generator are required and are defined by default."""
    def __init__(self, title='myconnectome', generator='cfflib', version="2.0", creator=None, publisher=None, created=None, modified=None, rights=None, license=None, references=None, relation=None, description=None, species=None, email=None, metadata_dictionary=None ):
        """Creates a connectome metadata object, specific metadata to the connectome object.
        
        Parameters
        ----------
        title : string, default: 'myconnectome',
            the name of this connectome 
        version : string, '2.0',  
            the connectome markup version for this connectome file
            
        creator : string, optional ,
            the creator name
        publisher : string, optional,
            the publisher/institution
        created : string, optional,
            the creation date of this connectome
        modified : string, optional,
            the date of important modification to this connectome object
        license : string, optional,
            license information
        rights : string, optional,
            rights information, such as copyright
        reference : string, optional,
            reference
        relation : string, optional,
            relation
        description : string, optional,
            a text description of the connectome
            
        generator : string, 'cfflib',
            software version/converter this file was generated with
        email : string, optional,
            an email of reference (author one)
        species : string, optional,
            the specied of the subject
                        
        metadata_dictionary : dictionary, optional,
            some metadata informations as a dictionary
            
        Notes
        -----
        Most of the metadata fields are defined in the Dublin Core Terms
        http://dublincore.org/documents/dcmi-terms/
        
        """
        super(CMetadata, self).__init__(version, title, creator, publisher, created, modified, rights, license, references, relation, description, generator, species, email,  )
        
        if not metadata is None:
            if not metadata_dictionary is None:
                self.update_metadata(metadata_dictionary)
        else:
            self.metadata = metadata()
            self.update_metadata({})

    def get_metadata_as_dict(self): 
        """Return the metadata as a dictionary"""
        if not self.metadata is None:
            return self.metadata.get_tags_as_dictionary()
        else:
            return None
    
    def update_metadata(self, metadata_dictionary): 
        """Set the metadata with a dictionary"""
        if self.metadata is None:
            self.metadata = metadata()
        
        self.metadata.set_tags_with_dictionary(metadata_dictionary)
        
    def exportChildren(self, outfile, level, namespace_='', name_='CMetadata'):
        
        if self.title:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%stitle>%s</%stitle>\n' % (namespace_, self.gds_format_string(quote_xml(self.title).encode(ExternalEncoding), input_name='title'), namespace_))
            #self.title.export(outfile, level, namespace_, name_='title', )
        if self.creator:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%screator>%s</%screator>\n' % (namespace_, self.gds_format_string(quote_xml(self.creator).encode(ExternalEncoding), input_name='creator'), namespace_))
            #self.creator.export(outfile, level, namespace_, name_='creator', )
        if self.publisher:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%spublisher>%s</%spublisher>\n' % (namespace_, self.gds_format_string(quote_xml(self.publisher).encode(ExternalEncoding), input_name='publisher'), namespace_))

            #self.publisher.export(outfile, level, namespace_, name_='publisher', )
        if self.created:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%screated>%s</%screated>\n' % (namespace_, self.gds_format_string(quote_xml(self.created).encode(ExternalEncoding), input_name='created'), namespace_))

            #self.created.export(outfile, level, namespace_, name_='created', )
        if self.modified:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%smodified>%s</%smodified>\n' % (namespace_, self.gds_format_string(quote_xml(self.modified).encode(ExternalEncoding), input_name='modified'), namespace_))

            #self.modified.export(outfile, level, namespace_, name_='modified', )
        if self.rights:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%srights>%s</%srights>\n' % (namespace_, self.gds_format_string(quote_xml(self.rights).encode(ExternalEncoding), input_name='rights'), namespace_))

            #self.rights.export(outfile, level, namespace_, name_='rights')
        if self.license:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%slicense>%s</%slicense>\n' % (namespace_, self.gds_format_string(quote_xml(self.license).encode(ExternalEncoding), input_name='license'), namespace_))

            #self.license.export(outfile, level, namespace_, name_='license')
        if self.references:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%sreferences>%s</%sreferences>\n' % (namespace_, self.gds_format_string(quote_xml(self.references).encode(ExternalEncoding), input_name='references'), namespace_))

            #self.references.export(outfile, level, namespace_, name_='references')
        if self.relation:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%srelation>%s</%srelation>\n' % (namespace_, self.gds_format_string(quote_xml(self.relation).encode(ExternalEncoding), input_name='relation'), namespace_))

            #self.relation.export(outfile, level, namespace_, name_='relation')
        if self.modified:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%smodified>%s</%smodified>\n' % (namespace_, self.gds_format_string(quote_xml(self.modified).encode(ExternalEncoding), input_name='modified'), namespace_))

            #self.modified.export(outfile, level, namespace_, name_='modified')

        if self.description is not None:
            namespace_= 'dcterms:'
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))

        if self.generator is not None:
            namespace_ = "cml:"
            showIndent(outfile, level)
            outfile.write('<%sgenerator>%s</%sgenerator>\n' % (namespace_, self.gds_format_string(quote_xml(self.generator).encode(ExternalEncoding), input_name='generator'), namespace_))
        if self.species is not None:
            namespace_ = "cml:"
            showIndent(outfile, level)
            outfile.write('<%sspecies>%s</%sspecies>\n' % (namespace_, self.gds_format_string(quote_xml(self.species).encode(ExternalEncoding), input_name='species'), namespace_))
        if self.email is not None:
            namespace_ = "cml:"
            showIndent(outfile, level)
            outfile.write('<%semail>%s</%semail>\n' % (namespace_, self.gds_format_string(quote_xml(self.email).encode(ExternalEncoding), input_name='email'), namespace_))
        if self.metadata:
            namespace_ = "cml:"
            self.metadata.export(outfile, level, namespace_, name_='metadata')

        
supermod.CMetadata.subclass = CMetadata
# end class CMetadata



class CBaseClass(object):


    def get_abs_path(self):
        return op.join(op.dirname(self.parent_cfile.fname), self.src)

    def save(self):
        """ Save a loaded connectome object to a temporary file, return the path """
        rval = save_data(self)
        if not rval == '':
            self.tmpsrc = rval
            print "Updated storage path of file: %s" % rval
        else:
            raise Exception('There is nothing to save.')

    # Metadata
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
    def get_metadata_as_dict(self):
        """Return the metadata as a dictionary"""
        if not self.metadata is None:
            return self.metadata.get_tags_as_dictionary()
        else:
            return {}
    
    def update_metadata(self, metadata_dictionary): 
        """Set the metadata with a dictionary"""
        if self.metadata is None:
            self.metadata = metadata()
        self.metadata.set_tags_with_dictionary(metadata_dictionary)
      
    # Print out a summary of the CObject
    def print_summary(self, printer=True):
        """Print a summary of the CObject"""
        
        # CObject class name
        s = ''
        if printer:
            s+= '# '+'='*56+' #'+'\n# '+self.__class__.__name__+'\n# '+'='*56+' #'
              
        # Attributes  
        s+= '\n# name : ' +self.get_name()
        if not self.get_description() is None:
            s+= '\n# description : '+self.get_description()
        if hasattr(self, 'dtype') and not self.get_dtype() is None:
            s+= '\n# dtype : '+self.get_dtype()
        if not self.get_fileformat() is None:
            s+= '\n# fileformat : '+self.get_fileformat()
        if not self.get_src() is None:
            s+= '\n# src : '+self.get_src()
        if not self.get_metadata_as_dict is None and not len(self.get_metadata_as_dict()) == 0:
            s+= '\n# metadata: '
            m = self.get_metadata_as_dict()
            for i in m.keys():
                s+= '\n#\t '+i+' : '+m[i]
        s+= '\n# '+'-'*56+' #'
        
        # Print or return
        if printer:
            print s
        else:
            return s
    
    def __eq__(self, y):
        return ( self.__class__.__name__ == y.__class__.__name__ and
        self.get_name() == y.get_name() and
        self.get_dtype() == y.get_dtype() and
        self.get_description() == y.get_description() and
        self.get_fileformat() == y.get_fileformat() and
        self.get_src() == y.get_src() and
        self.get_metadata_as_dict() == y.get_metadata_as_dict() )
        
        
        

class CNetwork(supermod.CNetwork, CBaseClass):
    """A connectome network object"""
    
    def __init__(self, name='mynetwork', dtype='AttributeNetwork', fileformat='GraphML', src=None, description=None, metadata=None):
        """Create a new CNetwork object.
        
        Parameters
        ----------
        name : 'mynetwork',
            the network unique name
        dtype : 'AttributeNetwork',
            the data type of the network. It could be: "AttributeNetwork", "DynamicNetwork", "HierarchicalNetwork" or "Other".
        fileformat : 'GraphML',
            the fileformat of the network. It could be: "GEXF", "GraphML", "NXGPickle" or "Other".
        src : string, optional,
            the source file of the network
        description : plaintext, optional,
            a text description of the CNetwork
        metadata : dictionary, optional,
            Metadata dictionary relative to the network
            
        See also
        --------
        Metadata, connectome
    
        """
        super(CNetwork, self).__init__(src, dtype, name, fileformat, metadata, description, )
        if not src is None and os.path.exists(src):
            print "File given by src exists. Create a new relative path."
            self.tmpsrc = src
            self.src = self.get_unique_relpath()
        
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
        """ Return a CNetwork object from a given ml_filename pointint to
        a GraphML file in your file system (not loading the file)
        
        Parameters
        ----------
        name : string,
            unique name of the CNetwork
        ml_filename : string,
            filename of the GraphML to load
        
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
        #cnet.data       = nx.read_graphml(ml_filename)
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
        # create a path to the temporary pickled file
        self.tmpsrc = tempfile.mkstemp(suffix = '.gpickle')[1]
        self.src    = self.get_unique_relpath()
        # save the object for the first time
        self.save()
    
supermod.CNetwork.subclass = CNetwork
# end class CNetwork


class CSurface(supermod.CSurface, CBaseClass):
    """A connectome surface object"""
    
    def __init__(self, name='mysurface', dtype='Surfaceset', fileformat='Gifti', src=None, description=None, metadata=None):
        """
        Create a new CSurface object.
        
        Parameters
        ----------
        name : 'mysurface'
            the unique surface name
        dtype : 'Labeling', 'Surfaceset', 'Surfaceset+Labeling', 'Other'
            the type of data that the Gifti file contain
        fileformat : 'Gifti',
            the fileformat of the surface, use default 'Gifti' to use the 
            only supported Gifti format by cfflib, use 'Other' for others format and custom support.
        src : string, optional,
            the source file of the surface
        description : string, optional,
            a description of the CSurface
        metadata : Metadata, optional,
            more metadata relative to the surface
            
        See also
        --------
        Metadata, connectome
    
        """
        super(CSurface, self).__init__(src, dtype, name, fileformat, description, metadata, )
        if not src is None and os.path.exists(src):
            print "File given by src exists. Create a new relative path."
            self.tmpsrc = src
            self.src = self.get_unique_relpath()
        
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
        csurf            = CSurface(name) 
        csurf.tmpsrc     = op.abspath(gii_filename)
        csurf.fileformat = "Gifti"
        csurf.dtype      = dtype
        #import nibabel.gifti as nig
        #csurf.data       = nig.read(gii_filename)
        csurf.src        = csurf.get_unique_relpath()
        return csurf
    
supermod.CSurface.subclass = CSurface
# end class CSurface


class CVolume(supermod.CVolume, CBaseClass):
    """Connectome volume object"""
    
    def __init__(self, name='myvolume', dtype=None, fileformat='Nifti1', src=None, description=None, metadata=None):
        """Create a new CVolume object.
        
        Parameters
        ----------
        name : 'myvolume',
            the unique name of the volume
        dtype : string, optional,
            the data type of the volume. It could be: 'T1-weighted', 'T2-weighted', 'PD-weighted', 'fMRI', 'MD', 'FA', 'LD', 'TD', 'FLAIR', 'MRA' or 'MRS depending on your dataset.
        fileformat : 'Nifti1',
            the fileformat of the volume. It could be: 'Nifti1', 'Nifti1GZ', 'Nifti2' (not supported yet)
        src : string, optional,
            the source file of the volume
        description : string, optional,
           A description according to the format attribute syntax.
        metadata : Metadata, optional,
            More metadata relative to the volume
                                
        See also
        --------
        Metadata, connectome
        """
        super(CVolume, self).__init__(src, dtype, name, fileformat, description, metadata, )
        if not src is None and os.path.exists(src):
            print "File given by src exists. Create a new relative path."
            self.tmpsrc = src
            self.src = self.get_unique_relpath()
                  
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
    
        if self.fileformat == 'Nifti1':
            fend = '.nii'
        elif self.fileformat == 'Nifti1GZ':
            fend = '.nii.gz'
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
        cvol            = CVolume(name) 
        cvol.tmpsrc     = op.abspath(nii_filename)
        if nii_filename.endswith('.gz'):
            cvol.fileformat = "Nifti1GZ"
        else:
            cvol.fileformat = "Nifti1"
        cvol.dtype      = dtype
        #cvol.data       = ni.load(nii_filename)
        cvol.src        = cvol.get_unique_relpath()
        return cvol
    
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
    def __init__(self, name=None, src=None, fileformat='TrackVis', dtype = None, description=None, metadata=None):
        super(CTrack, self).__init__(src, dtype, name, fileformat, description, metadata, )        
        if not src is None and os.path.exists(src):
            print "File given by src exists. Create a new relative path."
            self.tmpsrc = src
            self.src = self.get_unique_relpath()
            
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
    
        if self.fileformat == 'TrackVis':
            fend = '.trk'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CTrack', self.name + fend)
    
    def get_fibers_as_numpy(self):
        """ Returns fiber array """

        if hasattr(self, 'data') and not self.data is None and self.get_fileformat() == "TrackVis":
            from numpy import object, array
            fiblist, hdr = self.data
            noscalarfiblist = [f[0] for f in fiblist]
            return array(noscalarfiblist, dtype = object)
        else:
            return None
    
supermod.CTrack.subclass = CTrack
# end class CTrack


class CTimeseries(supermod.CTimeseries, CBaseClass):
    def __init__(self, name=None, src=None, dtype=None, fileformat='HDF5', description=None, metadata=None):
        super(CTimeseries, self).__init__(src, dtype, name, fileformat, description, metadata, )
        if not src is None and os.path.exists(src):
            print "File given by src exists. Create a new relative path."
            self.tmpsrc = src
            self.src = self.get_unique_relpath()
            
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        
        if self.fileformat == 'HDF5':
            fend = '.h5'
        elif self.fileformat == 'Other':
            fend = ''
            
        return unify('CTimeserie', self.name + fend)
    
supermod.CTimeseries.subclass = CTimeseries
# end class CTimeserie


class CData(supermod.CData, CBaseClass):
    def __init__(self, name=None, src=None, dtype=None, fileformat=None, description=None, metadata=None):
        super(CData, self).__init__(src, dtype, name, fileformat, description, metadata, )
        if not src is None and os.path.exists(src):
            print "File given by src exists. Create a new relative path."
            self.tmpsrc = src
            self.src = self.get_unique_relpath()
            
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
    def __init__(self, name=None, src=None, dtype='Python', fileformat='UTF-8', description=None, metadata=None):
        super(CScript, self).__init__(src, dtype, name, fileformat, description, metadata, )
        if not src is None and os.path.exists(src):
            print "File given by src exists. Create a new relative path."
            self.tmpsrc = src
            self.src = self.get_unique_relpath()
            
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


class CImagestack(supermod.CImagestack, CBaseClass):
    def __init__(self, name=None, src=None, fileformat=None, pattern=None, description=None, metadata=None):
        super(CImagestack, self).__init__(src, fileformat, name, pattern, description, metadata, )

    def save(self):
        """ Save a loaded connectome object to a temporary file, return the path """
        raise NotImplementedError('Saving CImagestack not implemented yet.')
        
    def get_unique_relpath(self):
        """ Return a unique relative path for this element """
        return unify('CImagestack', self.name + '/')
    
supermod.CImagestack.subclass = CImagestack
# end class CImagestack

#
#
#class description(supermod.description):
#    def __init__(self, valueOf_=None):
#        super(description, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='description', namespacedef_=''):
#        super(description, self).export(outfile, level, namespace_='dcterms:', name_='description', namespacedef_='')
#supermod.description.subclass = description
## end class description
#
#
#class title(supermod.title):
#    def __init__(self, valueOf_=None):
#        super(title, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='title', namespacedef_=''):
#        super(title, self).export(outfile, level, namespace_='dcterms:', name_='title', namespacedef_='')
#        
#supermod.title.subclass = title
## end class title
#
#
#class creator(supermod.creator):
#    def __init__(self, valueOf_=None):
#        super(creator, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='creator', namespacedef_=''):
#        super(creator, self).export(outfile, level, namespace_='dcterms:', name_='creator', namespacedef_='')
#supermod.creator.subclass = creator
## end class creator
#
#class publisher(supermod.publisher):
#    def __init__(self, valueOf_=None):
#        super(publisher, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='publisher', namespacedef_=''):
#        super(publisher, self).export(outfile, level, namespace_='dcterms:', name_='publisher', namespacedef_='')
#supermod.publisher.subclass = publisher
## end class publisher
#
#class relation(supermod.relation):
#    def __init__(self, valueOf_=None):
#        super(relation, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='relation', namespacedef_=''):
#        super(relation, self).export(outfile, level, namespace_='dcterms:', name_='relation', namespacedef_='')
#supermod.relation.subclass = relation
## end class relation
#
#class rights(supermod.rights):
#    def __init__(self, valueOf_=None):
#        super(rights, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='rights', namespacedef_=''):
#        super(rights, self).export(outfile, level, namespace_='dcterms:', name_='rights', namespacedef_='')
#supermod.rights.subclass = rights
## end class rights
#
#class created(supermod.created):
#    def __init__(self, valueOf_=None):
#        super(created, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='created', namespacedef_=''):
#        super(created, self).export(outfile, level, namespace_='dcterms:', name_='created', namespacedef_='')
#supermod.created.subclass = created
## end class created
#
#class modified(supermod.modified):
#    def __init__(self, valueOf_=None):
#        super(modified, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='modified', namespacedef_=''):
#        super(modified, self).export(outfile, level, namespace_='dcterms:', name_='modified', namespacedef_='')
#supermod.modified.subclass = modified
## end class modified
#
#
#class license(supermod.license):
#    def __init__(self, valueOf_=None):
#        super(license, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='license', namespacedef_=''):
#        super(license, self).export(outfile, level, namespace_='dcterms:', name_='license', namespacedef_='')
#supermod.license.subclass = license
## end class license
#
#class references(supermod.references):
#    def __init__(self, valueOf_=None):
#        super(references, self).__init__(valueOf_, )
#    def export(self, outfile, level, namespace_='', name_='references', namespacedef_=''):
#        super(references, self).export(outfile, level, namespace_='dcterms:', name_='references', namespacedef_='')
#supermod.references.subclass = references
## end class references


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
#    sys.stdout.write('<?xml version="1.0" ?>\n')
#    rootObj.export(sys.stdout, 0, name_=rootTag,
#        namespacedef_='xmlns="http://www.connectomics.org/cff-2" xmlns:dcterms="http://purl.org/dc/terms/"')
    # update parent references
    
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


