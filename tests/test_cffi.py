from _treesitter2.lib import *
from _treesitter2 import ffi


def test_rust():
    rust = tree_sitter_rust()
    assert rust.version > 0


def test_c():
    c = tree_sitter_c()
    assert c.version > 0

def test_cpp():
    cpp = tree_sitter_cpp()
    assert cpp.version > 0

def test_cpp():
    cpp = tree_sitter_cpp()
    assert cpp.version > 0

def test_python():
    py = tree_sitter_python()
    assert py is not ffi.NULL
    assert py.version > 0
