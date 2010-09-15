from zipfile import ZipFile, ZIP_DEFLATED
from glob import glob
import os.path as op
import os


# NetworkX
try:
    import networkx as nx
except ImportError:
    raise ImportError("Failed to import networkx from any known place")

# Nibabel
try:
    import nibabel as ni
except ImportError:
    raise ImportError("Failed to import nibabel from any known place")

# PyTables
try:
    import tables
except ImportError:
    raise ImportError("Failed to import pytables from any known place")

# NumPy
try:
    import numpy as np
except ImportError:
    raise ImportError("Failed to import numpy from any known place")


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

class NotSupportedFormat(Exception):
    def __init__(self, fileformat, objtype):
        self.fileformat = fileformat
        self.objtype = objtype
    def __str__(self):
        return "Loading %s:\nFile format '%s' not supported by cfflib. Use your custom loader." % (self.objtype, self.fileformat)

def save_data(obj):
    
    import tempfile
    tmpdir = tempfile.gettempdir()
    
    objrep = str(type(obj))
        
    if not obj.content is None:

        # it appears that there is no remove function for zip archives implemented to date
        # http://bugs.python.org/issue6818
        
        tmpfname = op.join(tmpdir, obj.get_unique_relpath())
        
        dname = op.dirname(tmpfname)
        if not op.exists(dname):
            os.makedirs()

        if 'CVolume' in objrep:
            ni.save(ele.content, tmpfname)
        elif 'CNetwork' in objrep:
            if obj.fileformat == "GraphML":
                # write graph to temporary file
                nx.write_graphml(obj.content, tmpfname)
            elif obj.fileformat == "GEXF":
                # XXX: networkx 1.4 / read_gexf
                pass
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CSurface' in objrep:
            if obj.fileformat == "Gifti":
                import nibabel.gifti as nig
                nig.write(obj.content, tmpfname)
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CTrack' in objrep:
            if obj.fileformat == "TrackVis":
                ni.trackvis.write(tmpfname, obj.content[0], obj.content[1])
                # XXX: correct?
                
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CTimeserie' in objrep:
            if obj.fileformat == "HDF5":
                # XXX: load = tables.openFile
                pass
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CData' in objrep:
            
            if obj.fileformat == "NumPy":
                load = np.save(tmpfname, obj.content)
            elif obj.fileformat == "HDF5":
                # load = tables.openFile
                pass
            elif obj.fileformat == "XML":
                f = open(tmpfname, 'w')
                f.write(obj.content)
                f.close()
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CScript' in objrep:
            
                f = open(tmpfname, 'w')
                f.write(obj.content)
                f.close()
            
            
        
        return tmpfname
    
    else:
        print "No content loaded. Nothing to save to a temporary file"
        


    
def load_data(obj):
    
    import tempfile
    tmpdir = tempfile.gettempdir()
    
    objrep = str(type(obj))
    if 'CVolume' in objrep:
        load = ni.load
    elif 'CNetwork' in objrep:
        if obj.fileformat == "GraphML":
            load = nx.read_graphml
        elif obj.fileformat == "GEXF":
            # XXX: networkx 1.4 / read_gexf
            pass
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CSurface' in objrep:
        if obj.fileformat == "Gifti":
            import nibabel.gifti as nig
            load = nig.read
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CTrack' in objrep:
        if obj.fileformat == "TrackVis":
            load = ni.trackvis.read
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CTimeserie' in objrep:
        if obj.fileformat == "HDF5":
            load = tables.openFile
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CData' in objrep:
        
        if obj.fileformat == "NumPy":
            load = np.load
        elif obj.fileformat == "HDF5":
            load = tables.openFile
        elif obj.fileformat == "XML":
            load = open
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CScript' in objrep:
        load = open
        
    elif 'CImagestack' in objrep:
        
        if obj.parent_cfile.iszip:
            _zipfile = ZipFile(obj.parent_cfile.src, 'r', ZIP_DEFLATED)
            try:
                namelist = _zipfile.namelist()
            except: # XXX: what is the correct exception for read error?
                raise RuntimeError('Can not extract %s from connectome file.' % str(obj.src) )
            finally:
                _zipfile.close()
            import fnmatch
            ret = []
            for ele in namelist:
                if fnmatch.fnmatch(ele, op.join(obj.src, obj.pattern)):
                    ret.append(ele)
            return ret
        else:
            # returned list should be absolute path
            if op.isabs(obj.src):
                return sorted(glob(op.join(obj.src, obj.pattern)))
            else:
                path2files = op.join(op.dirname(obj.parent_cfile.fname), obj.src, obj.pattern)
                return sorted(glob(path2files))

    ######
        
    if obj.parent_cfile.iszip:
        # extract src from zipfile to temp
        _zipfile = ZipFile(obj.parent_cfile.src, 'r', ZIP_DEFLATED)
        try:
            exfile = _zipfile.extract(obj.src, tmpdir)
        except: # XXX: what is the correct exception for read error?
            raise RuntimeError('Can not extract %s from connectome file.' % str(obj.src) )
        finally:
            print "Created temporary file %s while loading. Store path in .tmpsrc" % exfile
            obj.tmpsrc = exfile
            _zipfile.close()
            
        return load(exfile)
        
    else:
        if not obj.tmpsrc is None and op.isabs(obj.tmpsrc):
            # we have an absolute path
            return load(obj.tmpsrc)
        else:
            # otherwise, we need to join the meta.xml path with the current relative path
            path2file = op.join(op.dirname(obj.parent_cfile.fname), obj.src)
            return load(path2file)

def unify(t, n):
    """ Unify type and name """

    n = n.lower()
    n = n.replace(' ', '_')
        
    return '%s/%s' % (t, n)
        

import urllib2

def download(url, fileName=None):
    def getFileName(url,openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                openUrl.info().split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        # if no filename was found above, parse it out of the final URL.
        return basename(urlsplit(openUrl.url)[2])

    r = urllib2.urlopen(urllib2.Request(url))
    try:
        fileName = fileName or getFileName(url,r)
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r,f)
    finally:
        r.close()
