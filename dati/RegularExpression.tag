(dp0
(S'BlanklineTokenizer'
p1
I2
tp2
S'\\s*\\n\\s*\\n\\s*'
p3
s(S'Whitespace Tokenizer'
p4
I1
tp5
S'\\s+'
p6
s(S'capword tokenizer'
p7
I1
tp8
S'[A-Z]\\w+'
p9
s(S'Standard regexp tokenize'
p10
I1
tp11
S'\\w+|\\$[\\d\\.]+|\\S+'
p12
s(S'wordpunct tokenize'
p13
I1
tp14
S'\\w+|[^\\w\\s]+'
p15
s.