'''
Test Battery for the SQL3 CSV Import
Created on Sep 18, 2013

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
        #sys.stderr.write("Creating sql3load class instance\n")
        # self.s3_template = [{'name': 'text'}, {'age': 'integer'}, {'weigth': 'float'}]
        self.s3_template = [ ('name', 'text'), ('age', 'integer'), ('weigth', 'float') ]
        #se    lf.s3l = sql3load(self.s3_template)
        self.s3l = sql3load(self.s3_template, get_tmp_fn(".db") )
    ## end

    def tearDown(self):
        pass
    ## end

    def testClassInstantiation(self):
        # test relies on logic put in the setUp method
        pass

    def testRowInsertion(self):
        r = self.s3l._insert_row({'name': 'marcelo', 'age': 41, 'weigth': 125.0})
        self.assertTrue(r, "record not inserted succesfully")
        r = self.s3l.get_rowcount()
        self.assertEqual(r, 1, "rows should be exactly one, but instead count %s" % (r))

    def testRowRetrieval(self):
        self.s3l._insert_row({'name': 'marcelo', 'age': 41, 'weigth': 125.0})
        r = self.s3l.query("1=1")
        self.assertTrue(r, 'query did not return a valid value')
        #sys.stderr.write(str(r[0]))
        dr = dict(r[0])
        # sys.stderr.write("%s" % (dr))
        self.assertTrue( dr['age'] == 41, 'age should be 41' )
        pass

    def testImportCommaSeparatedFile(self):
        r = self.s3l.importFile("test/test-import.txt")
        self.assertTrue(r>0, "Number of lines read should be larger than 0 but is %s" % (r))
        #
        r = self.s3l.query("name = 'marcelo'")
        self.assertTrue(r[0]['age']==41, "marcelo's age should be 41 but is %s" % (r[0]['age']))

    def testImportTabSeparatedFile(self):
        self.s3l2 = sql3load(self.s3_template, get_tmp_fn("islas.db"), "\t")
        r = self.s3l2.importFile("test/test-import2.txt")
        # print "imported rows %s" % (r)
        self.assertTrue(r>3, "Number of lines read should be larger than 3 but is %s" % (r))

    #def testRowCount1(self):
    #    r = self.s3l.get_rowcount()
    #    self.assertEqual(r, 1, "rows should be exactly one, but instead count %s" % (r))


## end class Test

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
