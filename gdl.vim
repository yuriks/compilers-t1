" Vim syntax file
" Language: Grammar description language
" Maintainer: Yuri K. Schlesner
" Latest Revision: 5 May 2012

if exists("b:current_syntax")
	finish
endif

setlocal iskeyword+=-

syn region gdlComment start="/\*" end="\*/"
syn region gdlComment start="//" end="$"

syn region gdlTokenMatch start=/"/ skip=/\\"/ end=/"/ contained
syn region gdlTokenLiteral start=/'/ skip=/\\'/ end=/'/ contained

syn match gdlSkipToken /@@skip/
syn match gdlRootRule /#\k\+/
syn match gdlTokenId /@\k\+/ contained
syn match gdlRuleId /\k\+/ contained

syn match gdlOperator /|\|->\|=>\|?\|*/ contained

syn region gdlRuleRHS matchgroup=gdlAssign start=/:=/ end=/;/ transparent contains=gdlTokenLiteral,gdlTokenId,gdlRuleId,gdlOperator,gdlTokenMatch

let b:current_syntax = "gdl"
hi link gdlComment Comment
hi link gdlTokenMatch String
hi link gdlTokenLiteral String
hi link gdlTokenId Structure
hi link gdlRuleId Function
hi link gdlSkipToken Define
hi link gdlRootRule Define
hi link gdlOperator Operator
hi link gdlAssign Operator
hi link gdlTokenRHS String
hi link gdlRuleRHS Define
