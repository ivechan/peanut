from _treesitter2.lib import (
    ts_parser_new, ts_parser_delete, ts_parser_set_language,
    ts_parser_parse_string
)
from _treesitter2 import ffi
from treesitter2.language import Language
from treesitter2.tree import Tree


class Parser(object):
    def __init__(self):
        self._cparser = ts_parser_new()

    def set_language(self, language: Language):
        return ts_parser_set_language(self._cparser, language.get_language_id())

    def parse(self, string: bytes, old_tree: Tree = None):
        """
        string: bytes, must be utf-8 encoding.
        old_tree: Tree
        """
        if old_tree is not None:
            ctree = ts_parser_parse_string(self._cparser, old_tree._ctree,
                                           string, len(string))
        else:
            ctree = ts_parser_parse_string(self._cparser, ffi.NULL,
                                           string, len(string))
        return Tree(ctree)

    def __del__(self):
        ts_parser_delete(self._cparser)
