from _treesitter2.lib import (
    ts_node_type, ts_node_start_byte, ts_node_end_byte,
    ts_node_start_point, ts_node_end_point,
    ts_node_child_count, ts_node_child, 
    ts_node_next_sibling, ts_node_prev_sibling,
    ts_node_parent, ts_node_is_null,
    ts_node_string
)
from _treesitter2 import ffi

class Node(object):
    """docstring  for Node"""
    def __init__(self, cnode):
        super(Node, self).__init__()
        self._cnode = cnode
        if cnode is None or cnode == ffi.NULL:
            raise ValueError('cnode can not be None or cffi.NULL', cnode)
    
    @property
    def kind(self):
        """
        The type of Node.
        (while type is the keyword of python, so we uses kind here.)

        :returns: str

        """
        return ffi.string(ts_node_type(self._cnode))

    @property
    def start_byte(self):
        """
        :returns: int

        """
        return ts_node_start_byte(self._cnode)

    @property
    def end_byte(self):
        """
        :returns: int

        """
        return ts_node_end_byte(self._cnode)

    @property
    def start_point(self):
        """
        :returns: tuple(row, column)

        """
        tspoint = ts_node_start_point(self._cnode)
        return (tspoint.x, tspoint.y)

    @property
    def end_point(self):
        """
        :returns: tuple(row, column)

        """
        tspoint = ts_node_end_point(self._cnode)
        return (tspoint.x, tspoint.y)

    @property
    def sexp(self):
        return ffi.string(ts_node_string(self._cnode)).decode('utf-8')

    @property
    def children(self):
        child_count = ts_node_child_count(self._cnode)
        for i in range(child_count):
            cnode = ts_node_child(self._cnode, i)
            yield Node(cnode)
