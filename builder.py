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

TSParser* ts_parser_new();

bool ts_parser_set_language(TSParser *self, const TSLanguage *language);
extern const TSLanguage *tree_sitter_bash(void);
extern const TSLanguage *tree_sitter_c(void);
extern const TSLanguage *tree_sitter_cpp(void);
extern const TSLanguage *tree_sitter_go(void);
extern const TSLanguage *tree_sitter_javascript(void);
extern const TSLanguage *tree_sitter_json(void);
extern const TSLanguage *tree_sitter_lua(void);
extern const TSLanguage *tree_sitter_python(void);
extern const TSLanguage *tree_sitter_rust(void);
extern const TSLanguage *tree_sitter_typescript(void);

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

extern const TSLanguage *tree_sitter_bash(void);
extern const TSLanguage *tree_sitter_c(void);
extern const TSLanguage *tree_sitter_cpp(void);
extern const TSLanguage *tree_sitter_go(void);
extern const TSLanguage *tree_sitter_javascript(void);
extern const TSLanguage *tree_sitter_json(void);
extern const TSLanguage *tree_sitter_lua(void);
extern const TSLanguage *tree_sitter_python(void);
extern const TSLanguage *tree_sitter_rust(void);
extern const TSLanguage *tree_sitter_typescript(void);

""",
                      sources=['vendor/tree-sitter/lib/src/lib.c'],
                      include_dirs=['vendor/tree-sitter/lib/src',
                                    'vendor/tree-sitter/lib/include',
                                    'vendor/tree-sitter/lib/utf8proc',
                                    ],
                      library_dirs=['libs'],
                      libraries=['treesitterparser']

                      )





if __name__ == "__main__":
    #build_libs()
    ffibuilder.compile(verbose=True, debug=False)
