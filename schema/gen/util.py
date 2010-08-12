def file_exists(src, location):
    """ Checks if the file actually exists at the
    given location """
    
    pass

def validate_fileformat_type(src, location, fileformat):
    """ Try to evaluate whether the given file has the correct fileformat is given """
    pass

def validate_filedata_type(src, location, fileformat, dtype):
    """ Try to evalute whether the given file is of dtype type """
    pass 

# * [METHOD] extract all zip file content to path

def extract_file(cobj, zippath):
    """ Extracts the file given by zippath from a connectome object
    to the temporary folder and returns the absolute path """
    
    from tempfile import mkdtemp, mkstemp
    import os.path as op
    import os
    
    # mkdtemp(prefix = 'cffile')
    fname = op.basename(zippath)
    # XXX: need to preserve file ending!
    
    fhandler, fpath = mkstemp(suffix = fname)
    
    if cobj._src is None:
        raise RuntimeError('Connectome Object has to attribute _src pointing to its source file')
    
    from zipfile import ZipFile, ZIP_DEFLATED
    _zipfile = ZipFile(cobj._src, 'r', ZIP_DEFLATED)
    try:
        fileextracted = _zipfile.read(zippath)
    except: # XXX: what is the correct exception for read error?
        raise RuntimeError('Can not extract "%s" from connectome file.' % zippath)
    
    os.write(fhandler, fileextracted)
    del fileextracted
    os.close(fhandler)
    return fpath
    
def remove_file(fpath):
    """ Closes and removes the fpath file from the temporary folder """
    import os
    os.remove(fpath)

def extract_complete_cfile(path):
    """ Extract the complete connectome file to a particular path """
    pass