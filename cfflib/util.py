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

def validate_fileformat_type(src, location, fileformat):
    """ Try to evaluate whether the given file has the correct fileformat is given """
    pass

def validate_filedata_type(src, location, fileformat, dtype):
    """ Try to evalute whether the given file is of dtype type """
    pass 

def remove_file(fpath):
    """ Closes and removes the fpath file from the temporary folder """
    import os
    os.remove(fpath)

class NotSupportedFormat(Exception):
    def __init__(self, fileformat, objtype):
        self.fileformat = fileformat
        self.objtype = objtype
    def __str__(self):
        return "Loading %s:\nFile format '%s' not supported by cfflib. Use your custom loader." % (self.objtype, self.fileformat)

def save_data(obj):
        
    objrep = str(type(obj))
        
    if hasattr(obj, 'content'):

        # it appears that there is no remove function for zip archives implemented to date
        # http://bugs.python.org/issue6818
                
        # the file was loaded, thus it exists a .tmpsrc pointing to
        # its absolute path. Use this path to overwrite the file by the
        # current .content data
        if hasattr(obj, 'tmpsrc'):
            tmpfname = obj.tmpsrc
        else:
            raise Exception('Element %s cannot be saved. (It was never loaded)' % str(obj))
        
        dname = op.dirname(tmpfname)
        if not op.exists(dname):
            os.makedirs()

        if 'CVolume' in objrep:
            print "Saving CVolume ..."
            ni.save(obj.content, tmpfname)
            print "Done."
        elif 'CNetwork' in objrep:
            if obj.fileformat == "GraphML":
                # write graph to temporary file
                print "Saving CNetwork"
                nx.write_graphml(obj.content, tmpfname)
                print "Done."
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
                # flush the content of the buffers
                obj.content.flush()
                # close the file
                obj.content.close()
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CData' in objrep:
            
            if obj.fileformat == "NumPy":
                load = np.save(tmpfname, obj.content)
            elif obj.fileformat == "HDF5":
                # flush the content of the buffers
                obj.content.flush()
                # close the file
                obj.content.close()
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
        # assumes the .src paths are given relative to the meta.cml
        # valid for iszip = True and iszip = False
        # either path to the .cff or to the meta.cml
        # return op.join(op.dirname(obj.parent_cfile.fname), obj.src)
        print "Connectome Object is not loaded. Nothing to save."
        return ''

    
def load_data(obj):
        
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
        
        from tempfile import gettempdir
    
        # create a meaningful and unique temporary path to extract data files
        tmpdir = op.join(gettempdir(), obj.parent_cfile.get_unique_cff_name())

        # extract src from zipfile to temp
        _zipfile = ZipFile(obj.parent_cfile.src, 'r', ZIP_DEFLATED)
        try:
            exfile = _zipfile.extract(obj.src, tmpdir)
        except: # XXX: what is the correct exception for read error?
            raise RuntimeError('Can not extract %s from connectome file.' % str(obj.src) )
        finally:
            print "Created temporary file %s while loading." % exfile
            obj.tmpsrc = exfile
            _zipfile.close()
            
        return load(exfile)
        
    else:
        if hasattr(obj, 'tmpsrc'):
            # we have an absolute path
            print "Try to load object from %s" % obj.tmpsrc
            obj.tmpsrc = obj.tmpsrc
            return load(obj.tmpsrc)
        else:
            # otherwise, we need to join the meta.cml path with the current relative path
            path2file = op.join(op.dirname(obj.parent_cfile.fname), obj.src)
            print "Try to load object from %s" % path2file
            obj.tmpsrc = path2file
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
