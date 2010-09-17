""" Routines to load, save a connectome file

Dependencies
------------
* NetworkX
* Nibabel (Nifti, Gifti IO)
* PyTables (HDF5)
* Numexpr
* NumPy

"""

import cfflib_modified as cfflib

import os.path as op
from zipfile import ZipFile, ZIP_DEFLATED

def load_from_meta_cml(filename):
    """ Load connectome file from a meta.cml file. """
    
    with open(filename, 'r') as metacml:
        metastr = metacml.read()
        
    connectome = cfflib.parseString(metastr)
    connectome.iszip = False
    connectome.fname = op.abspath(filename)
    # check if names are unique!
    connectome.check_names_unique()
    
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

    # XXX: take care to have allowZip64 = True (but not supported by unix zip/unzip, same for ubuntu?) ?
    _zipfile = ZipFile(fname, 'a', ZIP_DEFLATED)
    try:
        metadata_string = _zipfile.read('meta.cml')
    except: # XXX: what is the correct exception for read error?
        raise RuntimeError('Can not extract meta.cml from connectome file.')
    
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


def save_to_cff(filename, connectome):
    """ Save connectome file to new .cff file on disk """
    
    _newzip = ZipFile(filename, 'w', ZIP_DEFLATED)
    
    allcobj = connectome.get_all()
    
    # tmpdir
    import tempfile
    import os
    tmpdir = tempfile.gettempdir()
    
    # check if names are unique!
    connectome.check_names_unique()

    for ele in allcobj:
        
        if not hasattr(ele, 'src') or ele.src == '':
            wt = ele.get_unique_relpath()
        else:
            wt = ele.src
        
        if not hasattr(ele, 'content'):
            
            if connectome.iszip:
                # extract zip content and add it to new zipfile
                if not wt in connectome._zipfile.namelist():
                    msg = "There exists no file %s in the connectome file from where " + \
                    "you want to save. Please create .content and set the attributes right" + \
                    "according to the documentation"
                    raise Exception(msg)
                else:
                    ftmp = connectome._zipfile.extract(wt)
            else:
                # create path coming from filesystem
                ftmp = op.join(op.dirname(connectome.fname), wt)
                
                if not op.exists(ftmp):
                    msg = "There exists no file %s for element %s. " + \
                    "Cannot save it. Either create it or assign a valid .content to element. " % (ftmp, str(ele))
                    raise Exception(msg)
            
            _newzip.write(ftmp, wt)
            
        else:
            
            # save content to a temporary file according to the objects specs
            ftmp = ele.save()
            
            _newzip.write(ftmp, wt)
        
        if connectome.iszip:
            # remove file
            os.remove(ftmp)
        
        # update ele.src
        ele.src = wt
  
    # export and store meta.cml
    mpth = op.join(tmpdir, 'meta.cml')
    f = open(mpth, 'w')
    f.write(connectome.to_xml())
    f.close()
    
    _newzip.write(mpth, 'meta.cml')
    os.remove(mpth)
    
    _newzip.close()
    
    print "New connectome file written to %s " % op.abspath(filename)
    
