##-----------------------------------------------------------------------------------------------------
'''
Test Battery for the SQL3 CSV Import
Created on Nov 23, 2015

@author: marcelo, carlos@xt6.us

@changelog:
'''
import unittest
import sys
import uuid
import os

from cm2c.commons.gen.utils import get_tmp_fn
from cm2c.commons.gen.getfile import getfile
from cm2c.csvimport.sql3load import sql3load

#--
class Test(unittest.TestCase):

    def setUp(self):
	self.url = "http://www.lanacion.com.ar"
	self.refresh = 10
	self.local_file = "tmp/downloaded_data.txt" 
	pass
    ## end

    def tearDown(self):
        pass
    ## end

    def testFileDownloadSizeGreaterThanZero(self):
	getfile(self.url, self.local_file , self.refresh) 
	si = os.stat(self.local_file)
	self.assertTrue(si.st_size>0)


## end class Test

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    print "TEST Battery: Download files from the Internet"
    unittest.main()

## END File
##-----------------------------------------------------------------------------------------------------
