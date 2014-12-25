__author__ = 'kbroughton'

import unittest
import pyodbc


class TestPyodbcConnect(unittest.TestCase):

    cnxn = pyodbc.connect('DSN=bespin')
    cursor = cnxn.cursor()
    sql = ("select * from oig_3_full_1_0_2.GNF_Bank")
    rows = cursor.execute(sql)
    r = rows.fetchall()
    print (r[0:3])

if __name__ == '__main__':
    unittest.main()
