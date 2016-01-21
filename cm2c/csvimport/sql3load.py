'''
Created on Sep 18, 2013

Updates:

20151109: integrated into cm2c-commons module

@author: marcelo

@todo: better automation
'''

import sqlite3
import gzip
import sys
import csv
from cm2c.commons.debug.statkeeper import statkeeper

class sql3load(object):
    '''
    This class implements a generic delimited text file importer into an sqlite3 backend. Allows for limited, SQL-like querying.
    '''

    ### begin
    def __init__(self, w_record_tpl, w_file_name = None, w_delimiter=",", w_table_name = "imported_data", **kwargs):
        '''
        Default constructor
        :param w_record_tpl : record template, an array of tuples with the format ('col name', 'col type', 'col desc') where col_type is a valid sqlite3 type and col_desc is an optional column description.
        :param w_file_name  : file name for the database. If None the database will be created in RAM.
        :param as_cache     : If True no DROP/CREATE of the database tables will occur and an attempt will be made to use already existing data. Defaults to False.
        '''
        #
        self.table_name = w_table_name
        self.delimiter = w_delimiter
        #
        self.record_tpl = w_record_tpl
        self.columns = []
        self.sk = statkeeper()
        #
        self.as_cache = kwargs.get('as_cache', False)
        #
        try:
            if w_file_name:
                self.conn = sqlite3.connect(w_file_name)
            else:
                self.conn = sqlite3.connect(':memory:')

            # set row factory to dictionary
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            #
            if not self.as_cache:
                self.cursor.execute(" DROP TABLE IF EXISTS %s" % (self.table_name) )
                self.conn.commit()
                self.cursor.execute(" CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY)" % (self.table_name) )

                # loop and add columns
                # for col_name in w_record_tpl.keys():
                for col in self.record_tpl:
                    col_name = col[0]
                    col_type = col[1]
                    sql = "ALTER TABLE %s ADD COLUMN %s %s" % (self.table_name, col_name, col_type)
                    self.columns.append(col_name)
                    self.cursor.execute(sql)
                # end for
                self.conn.commit()
            else:
                return self.get_rowcount()

        except:
            raise
    ### end

    ## begin
    def getTableName(self):
        return self.table_name
    ## end

    ## begin
    def __del__(self):
        self.conn.close()
    ## end

    ## begin
    def _insert_row(self, w_record):
        '''
        Inserts a single row into the database.

        :param w_record: A dictionary containing {col_name: col_value} entries.
        '''
        r = False
        try:
            # produce something like insert into mytable (col1,col2) values (:col1, :col2) so a dictionary can be used as parameter
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.table_name, ",".join(self.columns), ",".join([ ':'+x for x in self.columns ])  )
            # sys.stderr.write(sql)
            self.cursor.execute(sql, w_record)
            r = True
        except:
            raise
        #
        # self.conn.commit() // committing here makes everything slooooow
        return r
    ## end

    ## begin
    def get_rowcount(self):
        '''
        Returns the current number of rows in the in-memory database.
        '''
        sql = "SELECT count(*) AS CNT FROM %s" % (self.table_name)
        r1 = self.cursor.execute(sql)
        row = r1.fetchone()
        return dict(row)['CNT']
    ## end

    ## begin query
    def query(self, w_query, w_parameters = {}):
        """
        Runs an arbitrary SQL query against the newly created database.

        :param w_query: the query itself (what comes after the WHERE SQL keyword) using named parameters for column values, as in:
                        'origin_as=:oas'

        :param w_parameters: an associative array with parameter values. Must be consistent with the names used for wquery, as in:
                            {'oas': '28000'}
        """
        sql = "SELECT * FROM %s WHERE %s" % (self.table_name, w_query)
        try:
            qr = self.cursor.execute(sql, w_parameters)
            ar = []
            for x in qr:
                ar.append(dict(x))
            return ar
        except sqlite3.Error as e:
            raise e
            return None
        except:
            raise
    ## end

    ## begin query
    def _rawQuery(self, w_query, w_parameters = {}):
        """
        Runs an arbitrary FULL SQL query against the newly created database.

        :param w_query: the query itself using named parameters for column values, as in:
                        'origin_as=:oas'
                        the query string should include a $TN$ as a placeholder for the table name, it will
                        be automatically replaced by the current table name

        :param w_parameters: an associative array with parameter values. Must be consistent with the names used for wquery, as in:
                            {'oas': '28000'}
        """
        sql = w_query.replace("$TN$", self.table_name)
        try:
            qr = self.cursor.execute(sql, w_parameters)
            ar = []
            for x in qr:
                ar.append(dict(x))
            return ar
        except sqlite3.Error as e:
            raise e
            return None
        except:
            raise
    ## end


    ## begin
    def importFile(self, w_file_name, w_callback= lambda x:x, w_callback_steps=10):
        '''
        Imports delimiter-separated file into memory database. If the filename ends in '.gz', importFile()
        will try to open it using the gzip module.

        :param w_fname: file name of the CSV file to import.
        :param w_delimiter: delimiter char, defaults to comma but can be also \t
        :param w_callback: function to call when adding calculated values
        '''
        #
        # init variables
        try:
            if w_file_name.endswith(".gz"):
                self.file = gzip.open(w_file_name)
            else:
                self.file = open(w_file_name, 'rb')
            #
            self._stats = {}
            csv_r = csv.reader(self.file, delimiter=self.delimiter)
            # row = True
            for row in csv_r:
                record = {}
                ix = 0
                # if len(row) == len(self.record_tpl):
                for col in self.record_tpl:
                    if ix<len(row):
                        record[col[0]] = row[ix].strip()
                        ix = ix + 1
                    else:
                        record[col[0]] = None
                        # print "invalid row: %s, len %s, expected len %s" % (str(row), len(row), len(self.record_tpl))
                        self.sk.incKey('invalid-rows')
                #
                self._insert_row(record)
                self.sk.incKey('inserted-rows')
                if self.sk.getKey('inserted-rows') % w_callback_steps == 0:
                    w_callback(self.sk)
                #
            #
            self.conn.commit()
            return self.sk.getKey('inserted-rows')
        except:
            raise
    ## end

    ## begin
    def getStats(self):
        '''
        Returns a dictionary with all collected statistics
        '''
        return self.sk.getAllKeys()
    ## end

    ## begin
    def addMetaColumn(self, w_column_def = "colName VARCHAR(80)"):
        '''
        Adds a new column to the database. After the structure is modified, the column values will be updated
        by calling the w_callback function on all records.

        Example: addMetaColumn("age INTEGER")
        '''
        res = False
        try:
            sql = "ALTER TABLE %s ADD COLUMN %s " % (self.table_name, w_column_def)
            self._rawQuery(sql)
            res = True
        except:
            raise
        #
        return res
    ## end

    ## begin
    def calculateMetaColumn(self, w_column, w_callback):
        '''
        Calculates values for one of the columns as a function of the remaining columns.
        :param w_callback: a callback function that returns a new value for a given row.
        '''
        try:
            sql = "SELECT * FROM %s WHERE %s" % (self.table_name, "1=1")
            self.cursor2 = self.conn.cursor()
            qr = self.cursor.execute(sql)
            for row in qr:
                new_value = w_callback(row)
                sql_update = "UPDATE %s SET %s = :value WHERE id = :id" % (self.table_name, w_column)
                sql_update_parameters = {"id": row['id'], "column": w_column, "value": new_value}
                # print "sqlu par %s\n" % sql_update_parameters
                self.cursor2.execute(sql_update, sql_update_parameters)
                #
            # end for
            r = self.conn.commit()
            return r
        except OverflowError:
            print "Number too large in row %s, update parameters %s " % (dict(row), sql_update_parameters)
        except:
            raise
        return False
    ## end

## end class sql3load
