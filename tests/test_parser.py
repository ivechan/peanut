from treesitter2.Language import (BashLanguage, CLanguage, CppLanguage,
                                  GoLanguage, JavascriptLanguage,
                                  JsonLanguage, LuaLanguage,
                                  PythonLanguage, RustLanguage,
                                  TypescriptLanguage)


def test_bash():
    bash = BashLanguage().get_language_id()
    assert bash.version > 0


def test_c():
    c = CLanguage().get_language_id()
    assert c.version > 0


def test_cpp():
    cpp = CppLanguage().get_language_id()
    assert cpp.version > 0


def test_go():
    go = GoLanguage().get_language_id()
    assert go.version > 0


def test_javascript():
    javascript = JavascriptLanguage().get_language_id()
    assert javascript.version > 0


def test_json():
    json = JsonLanguage().get_language_id()
    assert json.version > 0


def test_lua():
    lua = LuaLanguage().get_language_id()
    assert lua.version > 0


def test_python():
    python = PythonLanguage().get_language_id()
    assert python.version > 0


def test_typescript():
    typescript = TypescriptLanguage().get_language_id()
    assert typescript.version > 0


def test_rust():
    rust = RustLanguage().get_language_id()
    assert rust.version > 0
