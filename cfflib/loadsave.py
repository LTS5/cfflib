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

def save_to_meta_cml(connectome, filename = 'meta.cml'):
    """ Stores a Connectome Markup File to filename """
    if connectome.get_connectome_meta() == None:
        print "ERROR - there is no connectome metadata in this connectome"
        return
    elif connectome.get_connectome_meta().name == None or connectome.get_connectome_meta().name == '':
        print "ERROR - the connectome metadata have to contain a unique name"
        return
    f = open(filename, 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    connectome.export(f, 0, namespacedef_='xmlns="http://www.connectomics.org/2010/Connectome/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.connectomics.org/2010/Connectome/xmlns connectome.xsd"')
    f.close()


def save_to_cff(connectome, filename):
    """ Save connectome file to new .cff file on disk """
    if connectome.get_connectome_meta() == None:
        print "ERROR - there is no connectome metadata in this connectome"
        return
    elif connectome.get_connectome_meta().name == None or connectome.get_connectome_meta().name == '':
        print "ERROR - the connectome metadata have to contain a unique name"
        return
    
    _newzip = ZipFile(filename, 'w', ZIP_DEFLATED)
    
    allcobj = connectome.get_all()
    
    # tmpdir
    import tempfile
    import os
    tmpdir = tempfile.gettempdir()
    
    # check if names are unique!
    connectome.check_names_unique()

    for ele in allcobj:
        print "----"
        print "Storing element: ", str(ele)
        
        # discover the relative path to use for the save
        if hasattr(ele, 'src'):
            if ele.src == '':
                wt = ele.get_unique_relpath()
                print "Created a unique path for element %s: %s" % (str(ele), wt)
            else:
                wt = ele.src
                print "Used .src attribute for relative path: %s" % wt
        else:            
            ele.src = ele.get_unique_relpath()
            wt = ele.src
            print "Element has no .src attribute. Create it and set it to %s" % ele.src
        
        if not hasattr(ele, 'content'):
            
            # Add if iszip is undefined
#            if not hasattr(connectome, 'iszip'):
#                connectome.iszip = False
            
            if connectome.iszip:
                # extract zip content and add it to new zipfile
                if not wt in connectome._zipfile.namelist():
                    msg = """There exists no file %s in the connectome file you want to save to
                    "Please create .content and set the attributes right
                    "according to the documentation"""
                    raise Exception(msg)
                else:
                    ftmp = connectome._zipfile.extract(wt)
            else:
                # connectome was not created from a zip
                # but for example in an IPython session
                
                # if now fname
                if not hasattr(connectome, 'fname'):
                    connectome.fname = op.abspath(filename)
            
                # save the element
                ele.save()
                # use the saved location
                ftmp = ele.tmpsrc
                
                # create path coming from filesystem
                #ftmp = op.join(op.dirname(connectome.fname), wt)
                
                if not op.exists(ftmp):
                    msg = """There exists no file %s for element %s. 
                    "Cannot save connectome file. Please update the element or bug report if it should work.""" % (ftmp, str(ele))
                    raise Exception(msg)
            
            _newzip.write(ftmp, wt)
            
        else:
            
            # save content to a temporary file according to the objects specs
            ele.save()
            
            # get the path
            ftmp = ele.tmpsrc
            
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
    
