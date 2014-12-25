__author__ = 'kbroughton'

from torpedo.core.topo import TopoColumn

class VerticaTopoColumn(TopoColumn):
    """
    torpedo-vertica subclass of TopoColumn
    """

    def _get_column_id(self):
