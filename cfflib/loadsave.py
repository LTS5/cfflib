""" Routines to load, save and validate a connectome file

Dependencies
------------
* NetworkX
* Nibabel (Nifti, Gifti IO)
* PyTables (HDF5)
* Numexpr
* NumPy

"""

import cfflib_modified as cfflib

# only expose a few
# from cfflib_modified import *

import os.path as op
from zipfile import ZipFile, ZIP_DEFLATED

def load_from_metaxml(filename):
    """ Load connectome file from meta.xml directly. """
    
    with open(filename, 'r') as metaxml:
        metastr = metaxml.read()
        
    connectome = cfflib.parseString(metastr)
    connectome.iszip = False
    connectome.fname = op.abspath(filename)
    # check if names are unique!
    connectome.check_names_unique()
    
    # update .src and .tmpsrc depending on how the path is given!
    # people want to write the absolute path in the meta.xml
    # this has to be accounted for
    # OR: only allow relative path names in src!! would simplify a lot!
    
    return connectome

def load_from_url(url, to_filename):
    """ First downloads the connectome file to a file to_filename
    load it and return the reference to the connectome object
    
    Not tested.
    """
    
    from util import download
    
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
    _zipfile = ZipFile(fname, 'a', ZIP_DEFLATED)
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
    
    connectome._zipfile = _zipfile
    
    # check if all referenced container elements exist in the archive
    connectome.check_file_in_cff()
    
    # check if names are unique!
    connectome.check_names_unique()
    
    return connectome


def save(filename, connectome):
    """ Save connectome file to new .cff file on disk """
    
    _newzip = ZipFile(filename, 'w', ZIP_DEFLATED)
    
    allcobj = connectome.get_all()
    
    # tmpdir
    import tempfile
    import os
    tmpdir = tempfile.gettempdir()
    
    # check if names are unique!
    connectome.check_names_unique()
    
    if connectome.iszip:
    
        for ele in allcobj:
            
            if ele.src is None or ele.src == '':
                wt = ele.get_unique_relpath()
            else:
                wt = ele.src
            
            if ele.content is None:
                
                # extract zip content and add it to new zipfile
                ftmp = connectome._zipfile.extract(ele)
                
                _newzip.write(ftmp, wt)
                
                # remove file
                os.remove(ftmp)
                
                # update ele.src
                ele.src = wt
                
            else:
                
                # save content to a temporary file according to the objects specs
                ftmp = ele.save()
                
                _newzip.write(ftmp, wt)
                
                # remove file
                os.remove(ftmp)
                
                # update ele.src
                ele.src = wt
          
        # export and store meta.xml
        mpth = op.join(tmpdir, 'meta.xml')
        f = open(mpth, 'w')
        f.write(connectome.to_xml())
        f.close()
        
        _newzip.write(mpth, 'meta.xml')
        os.remove(mpth)
        
        _newzip.close()
        
        print "New connectome file written to %s " % filename
        
    else:
        # if is is not a zip file
        pass
            
    # include the temporary files in the zip file with the correct src name
    # export and store meta.xml

    
    