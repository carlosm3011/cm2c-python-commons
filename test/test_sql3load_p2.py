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
        self.s3_template = [ ('name', 'text'), ('age', 'integer'), ('weigth', 'float') ]
        self.db_fn = get_tmp_fn(".db")
        self.s3l = sql3load(self.s3_template, self.db_fn )
        r = self.s3l.importFile("test/test-import.txt")
        self.s3l.addMetaColumn("cDoubleAge VARCHAR(80)")
    ## end

    def tearDown(self):
        pass
    ## end

    def testClassInstantiation(self):
        # test relies on logic put in the setUp method
        pass
    ## end

    def testAddColumn(self):
        r = self.s3l._rawQuery("SELECT COUNT(cDoubleAge) AS count FROM $TN$"  )
        # print "testCountNewColumn r %s" % (r)
        self.assertTrue(r[0]['count']==0)
    ## end testAddColumn

    ## begin
    def testCalculateValuesForNewColumn(self):
        self.s3l.calculateMetaColumn("cDoubleAge", lambda x : x['age'] * 2)
        r = self.s3l._rawQuery("SELECT COUNT(cDoubleAge) AS count FROM $TN$")
        # print "testCountNewColumn r %s" % (r)
        self.assertTrue(r[0]['count']==5)
        pass
    ## end

    ##begin
    def testMultipleCSVImport(self):
        self.islands_tpl = [('name', 'text'), ('pop', 'integer'), ('discovered', 'integer') ]
        self.islands_loader = sql3load(self.islands_tpl, self.db_fn, '\t', "islands")
        r = self.islands_loader.importFile("test/test-import2.txt")
    ##end

## end class Test

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    print "TEST Battery: add new columns and calculate column values"
    unittest.main()

## END File
##-----------------------------------------------------------------------------------------------------
