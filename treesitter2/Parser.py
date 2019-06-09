from _treesitter2.lib import *
from _treesitter2 import ffi
from tree_sitter import Language

class Parser(object):
    def __init__(self):
        self.__parser = ts_parser_new()

    def set_language(self, language: Language):
        return ts_parser_set_language(self.__parser, language.get_language_id())

    def __del__(self):
        ts_parser_delete(self.parser)
