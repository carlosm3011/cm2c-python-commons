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

from cm2c.commons.gen.utils import get_tmp_fn
from cm2c.csvimport.sql3load import sql3load

#--
class Test(unittest.TestCase):

    def setUp(self):
        self.s3_template = [{'name': 'text'}, {'age': 'integer'}, {'weigth': 'float'}]
        self.s3_template = [ ('name', 'text'), ('age', 'integer'), ('weigth', 'float') ]
        self.s3l = sql3load(self.s3_template, get_tmp_fn(".db") )
    ## end

    def tearDown(self):
        pass
    ## end

    def testClassInstantiation(self):
        # test relies on logic put in the setUp method
        pass
## end class Test

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

## END File
##-----------------------------------------------------------------------------------------------------
