'''
Created on Sep 3, 2013

@author: marcelo
'''
#===============================================================================
# Copyright (c) 2012 LACNIC - Latin American and Caribbean Internet
# Address Registry
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#===============================================================================

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
