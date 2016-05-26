# carlos@lacnic.net 20121128
# version 0.1

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

import urllib2
import os
import sys
import time
from cm2c.commons.debug.dprint import dprint
from cm2c.commons.gen.utils import get_tmp_fn
#


## get file ########################################################################
def getfile(w_url, w_file_name = None, w_update = 3600, ch_size=0):
    """
    Downloads a file object pointed by w_url and stores it on local file w_file_name.
    The w_update parameter marks how old the file can be. Files are only downloaded
    if they are older than w_update seconds.

    :param w_url: URL of the file to get. All urllib2 URLs are supported, including file:///
    :param w_update: Freshness timer in seconds. If the file was downloeaded less than this time ago the current copy is used,
                        thus avoiding unnecessary re-downloading files.
    :param w_file_name: Full file name and path of the locally-saved copy of the file. This parameter can be empty. In this case
                        getfile will choose a random temp file name and, on success, will return this name
    :param ch_size: Progress bar ticker step.

    :return : file name of the locally-saved copy.

    """

    if w_file_name == None:
        w_file_name = get_tmp_fn()

    if ch_size == 0:
        log_level = 0
    else:
        log_level = 3

    dp = dprint(log_level)

    dp.log("entering try block\n", 5)
    try:
        dp.log("Getting "+w_url+": ")
        mtime = 0
        if os.path.exists(w_file_name):
            mtime = os.stat(w_file_name).st_mtime
        now = time.time()
        # dprint("now: %s, mtime: %s" % (now, mtime))
        if now-mtime >= w_update:
            # sys.stderr.write("opening url\n")
            uh = urllib2.urlopen(w_url)
            # sys.stderr.write("creating local file\n")
            lfh = open(w_file_name, "wb+")
            # lfh.write(uh.read())
            while True:
                # data = uh.read(ch_size)
                data = uh.read(1024)
                if not data:
                    dp.log(": done!")
                    break
                lfh.write(data)
                dp.log(".")
            #
            return w_file_name
        else:
            dp.log("File exists and still fresh (%s secs old) \n" % (now-mtime))
            return w_file_name
    except urllib2.HTTPError as e:
        # raise
        dp.log("HTTP Error %s, %s\n" % (e.code, w_url))
        return False
    except urllib2.URLError as f:
        dp.log("URL Error reason: %s, url: %s\n" % (f.reason, w_url))
        # dprint("URLError")
        return False
    except:
        raise
## end get file ########################################################################

if __name__ == "__main__":
    print "get_file should not be used directly"
