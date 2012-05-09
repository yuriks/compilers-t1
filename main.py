import sys
import argparse
from metagrammar_ast import metagrammar
from ast_simplify import convert_ast_to_rule
from parse import parse_grammar
from grammar import Grammar

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

    meta_gram = Grammar()
    meta_gram.load_from_ast(metagrammar)

    with open(args.grammar) as grammar_input:
        g_token_stream = meta_gram.lexer.lex_input(grammar_input.read())
        grammar_ast = parse_grammar(meta_gram, g_token_stream)

    g = Grammar()
    g.load_from_ast(grammar_ast)

    if args.source != None:
        with open(args.source) as code:
            s_token_stream = g.lexer.lex_input(f.read())
            parse_grammar(g, s_token_stream)
    else:
        parse_grammar(g, g.lexer.lex_input(sys.stdin.read()))
