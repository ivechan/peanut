from _treesitter2.lib import (
    ts_node_type, ts_node_start_byte, ts_node_end_byte,
    ts_node_start_point, ts_node_end_point,
    ts_node_child_count, ts_node_child,
    ts_node_next_sibling, ts_node_prev_sibling,
    ts_node_parent, ts_node_is_null,
    ts_node_string,
    ts_node_is_named, ts_node_named_child, ts_node_named_child_count,
    ts_node_next_named_sibling, ts_node_prev_named_sibling
)
from _treesitter2 import ffi
from collections import namedtuple
Point = namedtuple('Point', ['row', 'column'])


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
        return ffi.string(ts_node_type(self._cnode)).decode('utf-8')

    @property
    def named(self):
        return ts_node_is_named(self._cnode)

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
        return Point(tspoint.row, tspoint.column)

    @property
    def end_point(self):
        """
        :returns: tuple(row, column)

        """
        tspoint = ts_node_end_point(self._cnode)
        return Point(tspoint.row, tspoint.column)

    @property
    def sexp(self):
        return ffi.string(ts_node_string(self._cnode)).decode('utf-8')

    @property
    def child_count(self):
        return ts_node_child_count(self._cnode)

    def child(self, i):
        child_node = ts_node_child(self._cnode, i)
        if ts_node_is_null(child_node):
            return None
        else:
            return Node(child_node)

    @property
    def children(self):
        for i in range(self.child_count):
            yield self.child(i)

    @property
    def named_child_count(self):
        return ts_node_named_child_count(self._cnode)

    def named_child(self, i):
        named_child_node = ts_node_named_child(self._cnode, i)
        if ts_node_is_null(named_child_node):
            return None
        else:
            return Node(named_child_node)

    @property
    def named_children(self):
        for i in range(self.named_child_count):
            yield self.named_child(i)
