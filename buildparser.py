import platform
import os.path as path
from tree_sitter_binding import Parser
from tempfile import TemporaryDirectory
from distutils.ccompiler import new_compiler
from ctypes.util import find_library
from ctypes import cdll, c_void_p
class Language:
    @staticmethod
    def build_library(output_path, repo_paths):
        """
        Build a dynamic library at the given path, based on the parser
        repositories at the given paths.

        Returns `True` if the dynamic library was compiled and `False` if
        the library already existed and was modified more recently than
        any of the source files.
        """
        output_mtime = 0
        if path.exists(output_path):
            output_mtime = path.getmtime(output_path)

        if len(repo_paths) == 0:
            raise ValueError('Must provide at least one language folder')

        cpp = False
        source_paths = []
        source_mtimes = [path.getmtime(__file__)]
        for repo_path in repo_paths:
            src_path = path.join(repo_path, 'src')
            source_paths.append(path.join(src_path, "parser.c"))
            source_mtimes.append(path.getmtime(source_paths[-1]))
            if path.exists(path.join(src_path, "scanner.cc")):
                cpp = True
                source_paths.append(path.join(src_path, "scanner.cc"))
                source_mtimes.append(path.getmtime(source_paths[-1]))
            elif path.exists(path.join(src_path, "scanner.c")):
                source_paths.append(path.join(src_path, "scanner.c"))
                source_mtimes.append(path.getmtime(source_paths[-1]))

        compiler = new_compiler(verbose=True)
        if cpp:
            if find_library('c++'):
                compiler.add_library('c++')
            elif find_library('stdc++'):
                compiler.add_library('stdc++')

        if max(source_mtimes) > output_mtime:
            with TemporaryDirectory(suffix='tree_sitter_language') as dir:
                object_paths = []
                for source_path in source_paths:
                    if platform.system() == 'Windows':
                        flags = None
                    else:
                        flags = ['-fPIC']
                        if source_path.endswith('.c'):
                            flags.append('-std=c99')
                    object_paths.append(compiler.compile(
                        [source_path],
                        output_dir=dir,
                        include_dirs=[path.dirname(source_path)],
                        extra_preargs=flags,
                        debug=False
                    )[0])
                compiler.link_shared_object(object_paths, output_path)
                #compiler.create_static_lib(object_paths, 'treesitterparser', 'libs')
                # using static lib instead of dynamic
            return True
        else:
            return False

    # def __init__(self, library_path, name):
    #     """
    #     Load the language with the given name from the dynamic library
    #     at the given path.
    #     """
    #     self.name = name
    #     self.lib = cdll.LoadLibrary(library_path)
    #     language_function = getattr(self.lib, "tree_sitter_%s" % name)
    #     language_function.restype = c_void_p
    #     self.language_id = language_function()


def build_libs():
    Language.build_library('libs/treesitterparser.dll',
                           ['vendor/tree-sitter-python',
                            'vendor/tree-sitter-c',
                            'vendor/tree-sitter-cpp',
                            'vendor/tree-sitter-rust',
                            'vendor/tree-sitter-json'],)

if __name__ == "__main__":
    build_libs()