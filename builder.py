from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
typedef struct TSLanguage TSLanguage;
typedef struct TSParser TSParser;
typedef struct TSTree TSTree;
typedef struct {
  uint32_t context[4];
  const void *id;
  const TSTree *tree;
} TSNode;
typedef struct {
  uint32_t row;
  uint32_t column;
} TSPoint;

uint32_t test();
TSParser* ts_parser_new();
TSLanguage* tree_sitter_json();
TSLanguage* tree_sitter_python();

bool ts_parser_set_language(TSParser *self, const TSLanguage *language);
TSTree *ts_parser_parse_string(
  TSParser *self,
  const TSTree *old_tree,
  const char *string,
  uint32_t length
);
void ts_tree_delete(TSTree *self);
void ts_parser_delete(TSParser *parser);

TSNode ts_node_named_child(TSNode, uint32_t);

// Syntax Nodes
const char *ts_node_type(TSNode);
uint32_t ts_node_start_byte(TSNode);
uint32_t ts_node_end_byte(TSNode);
TSPoint ts_node_start_point(TSNode);
TSPoint ts_node_end_point(TSNode);
char *ts_node_string(TSNode);

// Retrieving Nodes
TSNode ts_tree_root_node(const TSTree *);


uint32_t ts_node_child_count(TSNode);
TSNode ts_node_child(TSNode, uint32_t);

TSNode ts_node_next_sibling(TSNode);
TSNode ts_node_prev_sibling(TSNode);
TSNode ts_node_parent(TSNode);
uint32_t ts_node_named_child_count(TSNode);

bool ts_node_is_null(TSNode);


""")

ffibuilder.set_source("_tree_sitter",  # name of the output C extension
"""
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <tree_sitter/api.h>
#include <tree_sitter/parser.h>

TSLanguage *tree_sitter_json();

uint32_t test() {
        TSParser *parser = ts_parser_new();
        ts_parser_set_language(parser, tree_sitter_json());
        return tree_sitter_json();
}

""",
        sources=['vendor/tree-sitter/lib/src/lib.c', 
        'vendor/tree-sitter-json/src/parser.c'],   # includes pi.c as additional sources
        include_dirs=['vendor/tree-sitter/lib/src', 'vendor/tree-sitter/lib/include', 
        'vendor/tree-sitter/lib/utf8proc'],
        libraries=[])    # on Unix, link with the math library

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)