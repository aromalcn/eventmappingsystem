import pymysql

pymysql.install_as_MySQLdb()

# Monkey patch version to satisfy Django's requirements
import MySQLdb
if not hasattr(MySQLdb, 'version_info') or MySQLdb.version_info < (2, 2, 1):
    MySQLdb.version_info = (2, 2, 7, 'final', 0)
    MySQLdb.__version__ = '2.2.7'
