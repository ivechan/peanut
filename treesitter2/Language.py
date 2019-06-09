import abc
from abc import ABC
from _treesitter2.lib import (
    tree_sitter_bash, tree_sitter_c, tree_sitter_cpp, tree_sitter_go,
    tree_sitter_javascript, tree_sitter_json, tree_sitter_lua,
    tree_sitter_python, tree_sitter_rust, tree_sitter_typescript
)


class Language(ABC):
    @abc.abstractmethod
    def get_language_id(self):
        pass


class BashLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_bash()

    def get_language_id(self):
        return self.__language_id


class CLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_c()

    def get_language_id(self):
        return self.__language_id


class CppLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_cpp()

    def get_language_id(self):
        return self.__language_id


class GoLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_go()

    def get_language_id(self):
        return self.__language_id


class JavascriptLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_javascript()

    def get_language_id(self):
        return self.__language_id


class JsonLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_json()

    def get_language_id(self):
        return self.__language_id


class LuaLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_lua()

    def get_language_id(self):
        return self.__language_id


class PythonLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_python()

    def get_language_id(self):
        return self.__language_id


class RustLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_rust()

    def get_language_id(self):
        return self.__language_id


class TypescriptLanguage(Language):
    def __init__(self):
        self.__language_id = tree_sitter_typescript()

    def get_language_id(self):
        return self.__language_id
