""" Routines to load, save and validate a connectome file

CNetwork: Load/Parse GraphML
CVolume: Load Nifti
CSurface. Load Gifti
CTrack: Load TrackVis

Dependencies
------------
* NetworkX
* Nibabel (Nifti, Gifti IO)
* NiPy (for Nifti IO)
* DiPy (for TrackVis IO)
* ConnectomeViewer (for Gifti IO)

"""

import schema.gen.cfflib_modified2 as cfflib
import os.path as op

def load_from_metaxml(filename):
    """ Load connectome file from meta.xml directly """
    
    with open(filename, 'r') as metaxml:
        metastr = metaxml.read()
        
    connectome = cfflib.parseString(metastr)
    connectome.iszip = False
    connectome.fname = op.abspath(filename)
        
    return connectome

def load_cff_from_url(url, to_filename):
    """ First downloads the connectome file to a file to_filename
    load it and return the reference to the connectome object
    
    Not tested.
    """
    
    from schema.gen.util import download
    
    download(url, to_filename)
    
    return load_from_cff(to_filename)
    

def load_from_cff(filename, *args, **kwargs):
    """ Load connectome file given filename
    
        Returns
        -------
        connectome : ``Connectome``
                Connectome Instance
                
    """
    
    if isinstance(filename, basestring):
        # check if file exists
        from os.path import isfile, abspath
        
        if isfile(filename):
            if filename.endswith('.cff'):
                fname = abspath(filename)
            else:
                raise RuntimeError('%s must end with .cff' % filename)
            
        else:
            raise RuntimeError('%s seems not to be a valid file string' % filename)
    else:
        raise RuntimeError('%s seems not to be a valid file string' % filename)


    # extract meta.xml from connectome file
    # take care to have allowZip64 = True (but not supported by unix zip/unzip, same for ubuntu?) ?
    from zipfile import ZipFile, ZIP_DEFLATED
    _zipfile = ZipFile(fname, 'r', ZIP_DEFLATED)
    try:
        metadata_string = _zipfile.read('meta.xml')
    except: # XXX: what is the correct exception for read error?
        raise RuntimeError('Can not extract meta.xml from connectome file.')
    

    # create connectome instance
    connectome = cfflib.parseString(metadata_string)
    
    # add additional attributes
    connectome.src = fname
    
    # it is from the zip file
    connectome.iszip = True
    # if it is a zip file, we can assume that the src paths are given relatively
    
    # check if all referenced container elements exist in the archive
    # if not, raise an Exception
    
    # lazy loading strategy for individual container elements
    # add is loaded etc.
    
    return connectome


def save(filename, connectome):
    """ Save connectome file to file on disk """
    
    # create a zip file
    # loop through datasources and store them to temporary files
    # include the temporary files in the zip file with the correct src name
    # export and store meta.xml
    pass
    
    