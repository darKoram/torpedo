__author__ = 'kbroughton'

from torpedo.dialects import registry

registry.register("vertica", "torpedo_vertica.pyodbc", "Vertica_pyodbc")
registry.register("access.pyodbc", "torpedo_vertica.pyodbc", "Vertica_pyodbc")

from sqlalchemy.testing.plugin.pytestplugin import *