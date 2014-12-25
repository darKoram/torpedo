__author__ = 'kbroughton'

entry_points={
 'torpedo.dialects': [
      'vertica = torpedo_vertica.pyodbc:Vertica_pyodbc',
      'vertica.pyodbc = torpedo_vertica.pyodbc:Vertica_pyodbc',
      ]
}