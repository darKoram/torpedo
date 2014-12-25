__author__ = 'kbroughton'

from sqlalchemy.testing.suite import *

from sqlalchemy.testing.suite import ComponentReflectionTest as _ComponentReflectionTest

class ComponentReflectionTest(_ComponentReflectionTest):
    @classmethod
    def define_views(cls, metadata, schema):
        # bypass the "define_views" section of the
        # fixture
        return