from zipfile import ZipFile, ZIP_DEFLATED
from glob import glob
import os.path as op
import os
import json
import pickle

# NumPy
try:
    import numpy as np
except ImportError:
    raise ImportError("Failed to import numpy from any known place")

# Nibabel
try:
    import nibabel as ni
except ImportError:
    raise ImportError("Failed to import nibabel from any known place")

# NetworkX
try:
    import networkx as nx
except ImportError:
    pass
    #raise ImportError("Failed to import networkx from any known place")

# PyTables
try:
    import tables
except ImportError:
    pass
    #raise ImportError("Failed to import pytables from any known place")

def quote_for_xnat(name):
    """ Quote mapping from connectome object name to a valid XNAT filename
    that can be used for PyXNAT queries """
    n = name.lower()
    # XXX: might need update
    remove_characters = [' ', '/', '\\', '[', ']', '*', '"', '?', '\'', '%', '(', ')'] 
    for c in remove_characters:
        n = n.replace(c, '_')    
    return n
    

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
        
    if hasattr(obj, 'data'):

        # it appears that there is no remove function for zip archives implemented to date
        # http://bugs.python.org/issue6818
                
        # the file was loaded, thus it exists a .tmpsrc pointing to
        # its absolute path. Use this path to overwrite the file by the
        # current .data data
        if hasattr(obj, 'tmpsrc'):
            tmpfname = obj.tmpsrc
        else:
            # if it has no .tmpsrc, i.e. it is not loaded from a file path
            # but it has a .data set
            raise Exception('Element %s cannot be saved. (It was never loaded)' % str(obj))
        
        dname = op.dirname(tmpfname)
        if not op.exists(dname):
            os.makedirs()

        if 'CVolume' in objrep:
            print "Saving CVolume ..."
            ni.save(obj.data, tmpfname)
            print "Done."
        elif 'CNetwork' in objrep:
            print "Saving CNetwork"
            if obj.fileformat == "GraphML":
                # write graph to temporary file
                nx.write_graphml(obj.data, tmpfname)
            elif obj.fileformat == "GEXF":
                nx.write_gexf(obj.data, tmpfname)
            elif obj.fileformat == "NXGPickle":
                nx.write_gpickle(obj.data, tmpfname)
            else:
                raise NotSupportedFormat("Other", str(obj))
            print "Done."
            
        elif 'CSurface' in objrep:
            if obj.fileformat == "Gifti":
                import nibabel.gifti as nig
                nig.write(obj.data, tmpfname)
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CTrack' in objrep:
            if obj.fileformat == "TrackVis":
                ni.trackvis.write(tmpfname, obj.data[0], obj.data[1])
                # XXX: correct?
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CTimeserie' in objrep:
            if obj.fileformat == "HDF5":
                # flush the data of the buffers
                obj.data.flush()
                # close the file
                obj.data.close()
            elif obj.fileformat == "NumPy":
                load = np.save(tmpfname, obj.data)
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CData' in objrep:
            
            if obj.fileformat == "NumPy":
                load = np.save(tmpfname, obj.data)
            elif obj.fileformat == "HDF5":
                # flush the data of the buffers
                obj.data.flush()
                # close the file
                obj.data.close()
            elif obj.fileformat == "XML":
                f = open(tmpfname, 'w')
                f.write(obj.data)
                f.close()
            elif obj.fileformat == "JSON":
                f = open(tmpfname, 'w')
                json.dump(obj.data, f)
                f.close()
            elif obj.fileformat == "Pickle":
                f = open(tmpfname, 'w')
                pickle.dump(obj.data, f)
                f.close()
            elif obj.fileformat == "CSV" or obj.fileformat == "TXT":
                # write as text
                f = open(tmpfname, 'w')
                f.write(obj.data)
                f.close()
            else:
                raise NotSupportedFormat("Other", str(obj))
            
        elif 'CScript' in objrep:
                f = open(tmpfname, 'w')
                f.write(obj.data)
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
            # works with networkx 1.4
            load = nx.read_gexf
        elif obj.fileformat == "NXGPickle":
            load = nx.read_gpickle
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
        elif obj.fileformat == "NumPy":
            load = np.load 
        else:
            raise NotSupportedFormat("Other", str(obj))
        
    elif 'CData' in objrep:
        if obj.fileformat == "NumPy":
            load = np.load
        elif obj.fileformat == "HDF5":
            load = tables.openFile
        elif obj.fileformat == "XML":
            load = open
        elif obj.fileformat == "JSON":
            load = json.load
        elif obj.fileformat == "Pickle":
            load = pickle.load
        elif obj.fileformat == "CSV" or obj.fileformat == "TXT":
            # can use import csv on the returned object
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

def group_by_tagkey(cobj_list, tagkey, cobj_type = None, exclude_values = None):
    """ Specifying the connectome object type and metadata key, a
    dictionary is returned keyed by the values of the given metadata
    key.
    
    Parameter
    ---------
    cobj_list : list of connectome objects
        This list is filtered by the tagging key
    tagkey : string
        The metadata tag key you want to use for grouping
    cobj_type : string
        If you want to confine your result to a particular connectome
        object type such as 'CNetwork', 'CVolume' etc.
    exclude_values : list of string
        If you want to discard particular metadata values
        in the returned dictionary.
    
    Notes
    -----
    This function is helpful to retrieve groups of connectome
    objects for further analysis, e.g. statistical comparison.
    The metadata works as a kind of "intersubject" grouping
    criteria. For example you can have a metadata key "sex" with
    values M, F and unknown. You can exclude the unknown value
    by setting exclude_values = ['unknown'].
    
    If the metadata key does not exists for the connectome
    object, just skip this object.
    """
    rdict = {}
    for cob in cobj_list:
        if cobj_type is None or cobj_type in cob.__class__:
            mdi = cob.get_metadata_as_dict()
            if not mdi is None and tagkey in mdi.keys():
                if rdict.has_key(mdi[tagkey]):
                    rdict[mdi[tagkey]].append(cob)
                else:
                    rdict[mdi[tagkey]] = [cob]
    # eventually, remove not desired values
    if not exclude_values is None:
        for k in exclude_values:
            if rdict.has_key(k):
                del rdict[k]
            
    return rdict
