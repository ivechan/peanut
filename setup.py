from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

import platform
import os.path as path
from tempfile import TemporaryDirectory
from distutils.ccompiler import new_compiler
from ctypes.util import find_library
from ctypes import cdll, c_void_p
class Language:
    @staticmethod
    def build_library(output_dir, library_name, repo_paths):
        """
        Build a dynamic library at the given path, based on the parser
        repositories at the given paths.

        Returns `True` if the dynamic library was compiled and `False` if
        the library already existed and was modified more recently than
        any of the source files.
        """


        if len(repo_paths) == 0:
            raise ValueError('Must provide at least one language folder')

        cpp = False
        source_paths = []
        for repo_path in repo_paths:
            src_path = path.join(repo_path, 'src')
            source_paths.append(path.join(src_path, "parser.c"))
            if path.exists(path.join(src_path, "scanner.cc")):
                cpp = True
                source_paths.append(path.join(src_path, "scanner.cc"))
            elif path.exists(path.join(src_path, "scanner.c")):
                source_paths.append(path.join(src_path, "scanner.c"))

        compiler = new_compiler(verbose=True)
        if cpp:
            if find_library('c++'):
                compiler.add_library('c++')
            elif find_library('stdc++'):
                compiler.add_library('stdc++')

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
            #compiler.link_shared_object(object_paths, output_path)
            compiler.create_static_lib(object_paths, 'treesitterparser', 'libs')
                # using static lib instead of dynamic
            return True

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
    Language.build_library('libs','treesitterparser',
                           ['vendor/tree-sitter-bash',
                            'vendor/tree-sitter-c',
                            'vendor/tree-sitter-cpp',
                            'vendor/tree-sitter-go',
                            'vendor/tree-sitter-lua',
                            'vendor/tree-sitter-javascript',
                            'vendor/tree-sitter-json',
                            'vendor/tree-sitter-lua',
                            'vendor/tree-sitter-python',
                            'vendor/tree-sitter-rust',
                            'vendor/tree-sitter-typescript/typescript'],)

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print("Hello, developer, how are you? :)")
        build_libs()
        install.run(self)

class CustomDevelopCommand(develop):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print("Hello, developer, how are you? :)")
        build_libs()
        develop.run(self)

setup(
    name="treesitter2",
    version="0.1",
    packages=find_packages(),
    cmdclass={
    'install': CustomInstallCommand,
    'develop': CustomDevelopCommand
    },
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["treesitter2/builder.py:ffibuilder"],
    author="Jing",    
    author_email="lhchenjw@gmail.com",
    license="MIT Lisence"

)