from collections import namedtuple
from _treesitter2.lib import (
    ts_tree_root_node, ts_tree_delete,
    ts_tree_edit
)
from _treesitter2 import ffi
from treesitter2.node import Node
Point = namedtuple('Point', ['row', 'column'])

class Tree(object):
    """docstring for Tree"""
    def __init__(self, ctree):
        super(Tree, self).__init__()
        self._ctree = ctree

    @property
    def root_node(self):
        """
        Every tree has a root node.
        """
        return Node(ts_tree_root_node(self._ctree))

    def edit(self, start_byte: int, old_end_byte: int, new_end_byte: int,
             start_point: Point, old_end_point: Point,
             new_end_point: Point):
        """

        :returns: None

        """
        ts_input_edit = ffi.new('TSInputEdit *')
        ts_input_edit.start_byte = start_byte
        ts_input_edit.old_end_byte = old_end_byte
        ts_input_edit.new_end_byte = new_end_byte

        ts_input_edit.start_point.row = start_point.row
        ts_input_edit.start_point.column = start_point.column

        ts_input_edit.old_end_point.row = old_end_point.row
        ts_input_edit.old_end_point.column = old_end_point.column

        ts_input_edit.new_end_point.row = new_end_point.row
        ts_input_edit.new_end_point.column = new_end_point.column

        ts_tree_edit(self._cnode, ts_input_edit)

    def __del__(self):
        if self._ctree is not None and self._ctree is not ffi.NULL:
            ts_tree_delete(self._ctree)
