import sys
import argparse
from parse import parse_grammar
from grammar import Grammar
import grammar_parse
import lexer

#initializes the command line argument parser
def init_clp():
    parser = argparse.ArgumentParser(
            description='parses a grammar and validates syntatically user entries.')
    parser.add_argument('-g', '--grammar', metavar='grammar', type=str, 
            help='the grammar file to be parsed.', dest='grammar', required=True)
    parser.add_argument('-f', '--file', metavar='source', type=str, dest='source',
            help='path to file containing the source code to be validated') 
    return parser

if __name__ == '__main__':
    parser = init_clp()
    args = parser.parse_args()

    source = sys.stdin
    tokens_info = {"@@skip" : r"(?:\s*(?://[^\n]*\n)?)*",
        "@token-id" : r"(@@?[a-z]+(?:-[a-z]+)*)",
        "@rule-id" : r"(#?[a-z]+(?:-[a-z]+)*)",
        "@token-literal" : r"'((?:\\.|[^'\n])+)'",
        "@token-match" : '"' + r"((?:\\.|[^\"\n])+)" + '"'}
    literals = [':=', '(', ')', '?', '*', '=>', '|', ';']
    lexer.add_literal_tokens(tokens_info, literals)
    lexer_g = lexer.Tokenizer(tokens_info)

    with open(args.grammar) as grammar_input:
        g_token_stream = lexer_g.lex_input(grammar_input.read())
        grammar_ast = grammar_parse.parse_grammar(g_token_stream)
        print(str(grammar_ast))

    g = Grammar()
    g.load_from_ast(grammar_ast)

    if args.source != None:
        with open(args.source) as code:
            s_token_stream = g.lexer.lex_input(code.read())
            parse_grammar(g, s_token_stream)
    else:
        parse_grammar(g, g.lexer.lex_input(sys.stdin.read()))
