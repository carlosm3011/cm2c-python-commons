'''
Created on Sep 3, 2013

@author: marcelo
'''

from cm2c.etc import properties
import tempfile
import os
import json

### begin
def get_tmp_fn(w_suffix = None, **kwargs):
    '''
    returns a full path to a temp file name, using the current system properties
    :param filename: if named parameter 'filename' is None then a random name is created
    '''
    tmp_fname = kwargs.get('filename', None)
    if tmp_fname == None:
        tmp_fname = tempfile.NamedTemporaryFile().name
    fname = os.path.basename(tmp_fname)

    if w_suffix == None:
        w_suffix = ""
    tmp_file = "%s/%s%s" % (properties.paths['tmp'], fname, w_suffix)
    return tmp_file

### end

### begin
def json_load(w_file_name):
    '''
    Loads a json file from disk into a in-memory structure
    '''
    fn = "%s/%s" % (properties.srchome, w_file_name )
    try:
        cc_file = open(fn)
        cc_json = json.load(cc_file)
        return cc_json
    except:
        raise
        return "{'error': 'could not load file %s}'" % (fn)
### end json_load

if __name__ == "__main__":
    #for x in range(1,10):
    #    print "%s\n" % (get_tmp_file_name())
    print "not to be run directly"
