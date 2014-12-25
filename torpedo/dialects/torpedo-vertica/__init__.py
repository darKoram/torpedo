__author__ = 'kbroughton'


__all__ = (
'vertica',
'sqlite',
)

from .. import util
def _auto_fn(name):
"""default dialect importer.
plugs into the :class:`.PluginLoader`
as a first-hit system.
"""
if "." in name:
dialect, driver = name.split(".")
else:
dialect = name
driver = "base"
try:
module = __import__('sqlalchemy.dialects.%s' % (dialect, )).dialects
except ImportError:
return None
module = getattr(module, dialect)
if hasattr(module, driver):
module = getattr(module, driver)
return lambda: module.dialect
else:
return None
registry = util.PluginLoader("sqlalchemy.dialects", auto_fn=_auto_fn)