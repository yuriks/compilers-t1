from ast import *
   
metagrammar = Root([
    TokenDefinition("@@skip",
        r"(?:\s*(?://[^\n]*\n)?)*"),
    TokenDefinition("@token-id",
        r"(@@?[a-z]+(?:-[a-z]+)*)"),
    TokenDefinition("@rule-id",
        r"(#?[a-z]+(?:-[a-z]+)*)"),
    TokenDefinition("@token-literal",
        r"'((?:\\.|[^'\n])+)'"),
    TokenDefinition("@token-match",
        '"' + r"((?:\\.|[^\"\n])+)" + '"'),

    RuleDefinition("token-decl",
        FollowExpr([
            RuleTokenId("@token-id"),
            TokenLiteral(':='),
            RuleTokenId("@token-match")
        ])),
    RuleDefinition("rule-decl",
        FollowExpr([
            RuleTokenId("@rule-id"),
            TokenLiteral(':='),
            RuleTokenId("rule-expression")
        ])),

    RuleDefinition("rule-atom",
        AlternationExpr([
            RuleTokenId("@token-id"),
            RuleTokenId("@rule-id"),
            RuleTokenId("@token-literal"),
            FollowExpr([
                TokenLiteral('('),
                RuleTokenId("rule-expression"),
                TokenLiteral(')')
            ])
        ])),
    RuleDefinition("rule-postfix-expr",
        FollowExpr([
            RuleTokenId("rule-atom"),
            PostfixExpr('?',
                AlternationExpr([
                    TokenLiteral('?'),
                    TokenLiteral('*')
                ])
            )
        ])),
    RuleDefinition("rule-follow-expr",
        FollowExpr([
            RuleTokenId("rule-postfix-expr"),
            PostfixExpr('*',
                FollowExpr([
                    TokenLiteral('=>'),
                    RuleTokenId("rule-postfix-expr")
                ])
            )
        ])),
    RuleDefinition("rule-alternation-expr",
        FollowExpr([
            RuleTokenId("rule-alternation-expr"),
            PostfixExpr('*',
                FollowExpr([
                    TokenLiteral('|'),
                    RuleTokenId("rule-alternation-expr")
                ])
            )
        ])),
    RuleDefinition("rule-expression",
        RuleTokenId("rule-alternation-expr")),

    RuleDefinition("#grammar",
        PostfixExpr('*',
            FollowExpr([
                AlternationExpr([
                    RuleTokenId("token-decl"),
                    RuleTokenId("rule-decl")
                ]),
                TokenLiteral(';')
            ])
        ))
])