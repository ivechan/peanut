from _tree_sitter.lib import *
from _tree_sitter import ffi
r = test()
print(r)

js = tree_sitter_json()
print(js)

parser = ts_parser_new()
print(parser)
source_code = bytes('[1, null]', "utf-8")
r = ts_parser_set_language(parser, js)
print(r)
tree = ts_parser_parse_string(parser, ffi.NULL, source_code, len(source_code))
root_node = ts_tree_root_node(tree)
print(root_node, dir(root_node))
sexp = ffi.string(ts_node_string(root_node))
print(sexp)

array_node = ts_node_named_child(root_node, 0);
number_node = ts_node_named_child(array_node, 0);

start_point = ts_node_start_point(root_node)
end_point = ts_node_end_point(root_node)
print('start_point:', start_point.row, start_point.column)
print('end_point:', end_point.row, end_point.column)


assert ts_node_child_count(root_node) == 1
assert ts_node_child_count(array_node) == 5
assert ts_node_named_child_count(array_node) == 2
assert ts_node_child_count(number_node) == 0

ts_tree_delete(tree)
ts_parser_delete(parser)
print('end')
