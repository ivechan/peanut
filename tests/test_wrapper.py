from treesitter2.parser import Parser
from treesitter2.node import Node, Point
from treesitter2.tree import Tree


def test_javascript():
    from treesitter2.language import JavascriptLanguage
    parser = Parser()
    JSLANGUAGE = JavascriptLanguage()
    assert parser.set_language(JSLANGUAGE) is True
    sourceCode = b'let x = 1; console.log(x);'
    tree = parser.parse(sourceCode)
    root_node = tree.root_node
    callExpression = root_node.child(1).child(0)

    assert callExpression.kind == 'call_expression'

    assert list(root_node.children)
    assert list(root_node.named_children)

    newSourceCode = b'const x = 1; console.log(x);'
    tree.edit(0, 3, 5, Point(row=0, column=0), Point(row=0, column=0),
              Point(row=0, column=5))
    newTree = parser.parse(newSourceCode, tree)
    assert root_node.child(0).child(0).kind == 'let'
    assert newTree.root_node.child(0).child(0).kind == 'const'



def test_c():
    from treesitter2.language import CLanguage
    parser = Parser()
    CLANGUAGE = CLanguage()
    assert parser.set_language(CLANGUAGE) is True
    sourceCode = b'int i = 1;'
    tree = parser.parse(sourceCode)
    root_node = tree.root_node
    declaration = root_node.child(0)
    assert declaration.kind == 'declaration'
