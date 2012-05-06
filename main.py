import sys
import argparse

#Initializes the command line argument parser
def init_clp():
    parser = argparse.ArgumentParser(
            description='Parses a grammar and validates syntatically user entries.')
    parser.add_argument('-g', '--grammar', metavar='GRAMMAR', type=str, 
            help='The grammar file to be parsed.', dest='grammar', required=True)
    parser.add_argument('-f', '--file', metavar='SOURCE', type=str, dest='source',
            help='Path to file containing the source code to be validated') 
    return parser

def validate_src(src, grammar):
    #for line in src:
    #    grammar.validate(line)
    pass #TODO

if __name__ == '__main__':
    parser = init_clp()
    args = parser.parse_args()
    
    grammar = None #TODO grammar object
    source = sys.stdin
    if args.source != None:
        with open(args.source) as f:
            validate_src(source, grammar)
    else:
        validate_src(sys.stdin, grammar)
