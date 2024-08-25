import ply.lex as lex
import ply.yacc as yacc

# Tokenisation of keywords used in the program
tokens = (
    'IF', 'ELSE',
    'FOR', 'IN', 'DO', 'RANGE',
    'WHILE',
    'LOOP', 'BEGIN',
    'END',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'SINGLEQUOTE', 'DOUBLEQUOTES',
    'IDENTIFIER', 'COMMA', 'STRING', 'NUMBER',
    'EQUALS', 'EQUALS_EQUALS', 'GREATERTHAN', 'LESSTHAN', 'NOT_EQUAL', 'LESSEQUAL', 'GREATEQUAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
)

# Defining the tokens to relate each input to a particular token
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_SINGLEQUOTE = r'\''
t_DOUBLEQUOTES = r'"'
t_NUMBER = r'\d+'
t_EQUALS = r'='
t_EQUALS_EQUALS = r'=='
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'
t_NOT_EQUAL = r'!='
t_LESSEQUAL = r'<='
t_GREATEQUAL = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ignore = ' \t'

#using reserved so that these keyword dont fall under the identifier definition
reserved = {
    'if': 'IF',
    'end': 'END',
    'puts': 'IDENTIFIER',
    'else': 'ELSE',
    'print': 'IDENTIFIER',
    'for': 'FOR',
    'in': 'IN',
    'do': 'DO',
    'range': 'RANGE',
    'while': 'WHILE',
    'loop': 'LOOP',
    'begin': 'BEGIN',
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

#defining strings to be accepted without quotes
def t_STRING(t):
    r'"([^"\\]|\\.|"")*"'
    t.value = t.value[1:-1]
    return t

def t_COMMA(t):
    r','
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character: '{t.value[0]}'")
    t.lexer.skip(1)

#initialising the lexer
lexer = lex.lex()

#Sample Ruby code to check the lexer
data = 'for i in range (25) do {puts "i less than 25"} end'

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

#Grammar rules for the Ruby 'if', 'else', 'else if', 'while', 'do-while' and 'for' constructs
def p_all_constructs(p):
    '''
    all_constructs : FOR arguments IN RANGE LPAREN condition RPAREN DO LBRACE statements RBRACE END
                  | FOR arguments IN IDENTIFIER DO LBRACE statements RBRACE END
                  | FOR arguments IN IDENTIFIER LBRACE statements RBRACE END
                  | FOR arguments IN RANGE LPAREN condition RPAREN LBRACE statements RBRACE END
                  | IF LPAREN condition RPAREN LBRACE statements RBRACE else_statement END
                  | IF LPAREN condition RPAREN LBRACE statements RBRACE END
                  | IF LPAREN condition RPAREN LBRACE if_statement RBRACE END
                  | WHILE LPAREN condition RPAREN LBRACE statements RBRACE END
                  | WHILE LPAREN condition RPAREN DO LBRACE statements RBRACE END
                  | BEGIN LBRACE statements RBRACE END while_statement
                  | LOOP DO LBRACE statements RBRACE END
    '''
    p[0] = 'Valid Ruby statement'

def p_if_statement(p):
    '''
    if_statement : IF LPAREN condition RPAREN LBRACE statements RBRACE else_statement END
                 | IF LPAREN condition RPAREN LBRACE statements RBRACE END
    '''
    pass

def p_else_statement(p):
    '''
    else_statement : ELSE LBRACE statements RBRACE
                   | ELSE if_statement
                   |
    '''
    pass

def p_while_statement(p):
    '''
    while_statement : WHILE LPAREN condition RPAREN
                    | WHILE condition
    '''
    pass

def p_condition(p):
    '''
    condition : expression GREATERTHAN expression
              | expression LESSTHAN expression
              | expression EQUALS_EQUALS expression
              | expression PLUS expression
              | expression MINUS expression
              | expression TIMES expression
              | expression DIVIDE expression
              | expression LESSEQUAL expression
              | expression GREATEQUAL expression
              | expression NOT_EQUAL expression
              | NUMBER
    '''
    pass

def p_expression(p):
    '''
    expression : IDENTIFIER
               | NUMBER
               | STRING
               | function_call
    '''
    pass

def p_statements(p):
    '''
    statements : statement
               | statements statement
    '''
    pass

def p_statement(p):
    '''
    statement : function_call
              | all_constructs
    '''
    pass

def p_function_call(p):
    '''
    function_call : IDENTIFIER LPAREN arguments RPAREN SEMICOLON
                  | IDENTIFIER arguments SEMICOLON
                  | IDENTIFIER LPAREN arguments RPAREN
                  | IDENTIFIER arguments
    '''
    pass

def p_arguments(p):
    '''
    arguments :
              | expression
              | arguments COMMA expression
    '''
    pass

#Handling of error in the parser
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")
    else:
        print("Syntax error at EOF")

#initialising a parser
parser = yacc.yacc()

while True:
    try:
        s = input('Ruby-code > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)