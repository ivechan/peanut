from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
typedef uint16_t TSSymbol;
typedef uint16_t TSFieldId;
typedef struct TSLanguage TSLanguage;

typedef struct {
  TSFieldId field_id;
  uint8_t child_index;
  bool inherited;
} TSFieldMapEntry;

typedef struct {
  uint16_t index;
  uint16_t length;
} TSFieldMapSlice;

typedef uint16_t TSStateId;

typedef struct {
  bool visible : 1;
  bool named : 1;
} TSSymbolMetadata;

typedef struct TSLexer TSLexer;

struct TSLexer {
  int32_t lookahead;
  TSSymbol result_symbol;
  void (*advance)(TSLexer *, bool);
  void (*mark_end)(TSLexer *);
  uint32_t (*get_column)(TSLexer *);
  bool (*is_at_included_range_start)(TSLexer *);
};

typedef enum {
  TSParseActionTypeShift,
  TSParseActionTypeReduce,
  TSParseActionTypeAccept,
  TSParseActionTypeRecover,
} TSParseActionType;

typedef struct {
  union {
    struct {
      TSStateId state;
      bool extra : 1;
      bool repetition : 1;
    };
    struct {
      TSSymbol symbol;
      int16_t dynamic_precedence;
      uint8_t child_count;
      uint8_t production_id;
    };
  } params;
  TSParseActionType type : 4;
} TSParseAction;

typedef struct {
  uint16_t lex_state;
  uint16_t external_lex_state;
} TSLexMode;

typedef union {
  TSParseAction action;
  struct {
    uint8_t count;
    bool reusable : 1;
  };
} TSParseActionEntry;

struct TSLanguage {
  uint32_t version;
  uint32_t symbol_count;
  uint32_t alias_count;
  uint32_t token_count;
  uint32_t external_token_count;
  const char **symbol_names;
  const TSSymbolMetadata *symbol_metadata;
  const uint16_t *parse_table;
  const TSParseActionEntry *parse_actions;
  const TSLexMode *lex_modes;
  const TSSymbol *alias_sequences;
  uint16_t max_alias_sequence_length;
  bool (*lex_fn)(TSLexer *, TSStateId);
  bool (*keyword_lex_fn)(TSLexer *, TSStateId);
  TSSymbol keyword_capture_token;
  struct {
    const bool *states;
    const TSSymbol *symbol_map;
    void *(*create)(void);
    void (*destroy)(void *);
    bool (*scan)(void *, TSLexer *, const bool *symbol_whitelist);
    unsigned (*serialize)(void *, char *);
    void (*deserialize)(void *, const char *, unsigned);
  } external_scanner;
  uint32_t field_count;
  const TSFieldMapSlice *field_map_slices;
  const TSFieldMapEntry *field_map_entries;
  const char **field_names;
};




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

typedef struct {
  uint32_t start_byte;
  uint32_t old_end_byte;
  uint32_t new_end_byte;
  TSPoint start_point;
  TSPoint old_end_point;
  TSPoint new_end_point;
} TSInputEdit;

void ts_tree_edit(TSTree *, const TSInputEdit *);
""")

ffibuilder.set_source("_treesitter2",  # name of the output C extension
                      """
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <tree_sitter/api.h>
#include <tree_sitter/parser.h>

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
