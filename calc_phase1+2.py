# ------------------------------------------------------------
# calc_phase1+2.py
#
# A simple calculator with variables.
#
#
# 58090046 Araya Siriadun
# ------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc
import codecs


class CalculatorProject:
    # List of token names.
    tokens = ('NUM', 'Idivide', 'ge', 'le', 'eq', 'ne', 'VAR', 'PI', 'ERR')

    literals = ['+', '-', '*', '/', '>', '^', '<', '=', '(', ')']

    operator = {
        'Idivide': '//',
        'ge': '>=',
        'le': '<=',
        'eq': '==',
        'ne': '!=',
    }

    t_ignore = ' \t'

    def __init__(self):
        self.file = None
        self.errorMsg = str()

        # Build the lexer and parser
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def t_NUM(self, t):
        r'(?:(?<=(?<=\+)|(?<=\-)|(?<=\*)|(?<=/)|(?<=//)|(?<=\^)|(?<=>)|(?<=>=)|(?<=<)|(?<=<=)|(?<===)|(?<=!=)|(?<=\()|(?<==)|(?<=\s)|(?<=\A)))-?(?=[1-9]|0(?!\d))\d+(\.\d+)?([eE][+-]?\d+)?(?=\+|\-|\*|/|//|\^|>|>=|<|<=|==|!=|\)|=|\s|\Z)'
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_PI(self, t):
        r'(?:(?<=(?<=\+)|(?<=\-)|(?<=\*)|(?<=/)|(?<=//)|(?<=\^)|(?<=>)|(?<=>=)|(?<=<)|(?<=<=)|(?<===)|(?<=!=)|(?<=\()|(?<==)|(?<=\s)|(?<=\A)))PI(?=\+|\-|\*|/|//|\^|>|>=|<|<=|==|!=|\)|=|\s|\Z)'
        return t

    def t_VAR(self, t):
        r'(?:(?<=(?<=\+)|(?<=\-)|(?<=\*)|(?<=/)|(?<=//)|(?<=\^)|(?<=>)|(?<=>=)|(?<=<)|(?<=<=)|(?<===)|(?<=!=)|(?<=\()|(?<==)|(?<=\s)|(?<=\A)))[a-zA-Z_][a-zA-Z0-9_]*(?=\+|\-|\*|/|//|\^|>|>=|<|<=|==|!=|\)|=|\s|\Z)'
        return t

    def t_Idivide(self, t):
        r'//'
        return t

    def t_ge(self, t):
        r'>='
        return t

    def t_le(self, t):
        r'<='
        return t

    def t_eq(self, t):
        r'=='
        return t

    def t_ne(self, t):
        r'!='
        return t

    def t_plus(self, t):
        r'\+'
        t.type = '+'
        return t

    def t_minus(self, t):
        r'-'
        t.type = '-'
        return t

    def t_times(self, t):
        r'\*'
        t.type = '*'
        return t

    def t_Fdivide(self, t):
        r'/'
        t.type = '/'
        return t

    def t_pow(self, t):
        r'\^'
        t.type = '^'
        return t

    def t_gt(self, t):
        r'>'
        t.type = '>'
        return t

    def t_lt(self, t):
        r'<'
        t.type = '<'
        return t

    def t_lparen(self, t):
        r'\('
        t.type = '('
        return t

    def t_rparen(self, t):
        r'\)'
        t.type = ')'
        return t

    def t_assign(self, t):
        r'='
        t.type = '='
        return t

    def t_ERR(self, t):
        #r'(?<=\s)\S+(?=\s)|(?<=\A)\S+(?=\s)|(?<=\s)\S+(?=\Z)'
        r'\S'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '{}'".format(t.value[0]))
        t.lexer.skip(1)

    # Parsing rules

    precedence = (
        ('nonassoc', '>', 'ge', '<', 'le', 'eq',
         'ne'),  # Non-associative operators
        ('left', '+', '-'),
        ('left', '*', '/', 'Idivide'),
        ('right', 'UMINUS'),  # Unary minus operator
        ('right', '^'),
    )

    # dictionary of names (for storing variables)
    names = {}

    def p_statement_assign(self, p):
        '''statement : VAR '=' expression'''
        self.names[p[1]] = p[3]
        p[0] = '({}={})'.format(p[1], p[3])

    def p_statement_expr(self, p):
        '''statement : expression'''
        p[0] = p[1]

    def p_expression_binop(self, p):
        '''expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression Idivide expression
                      | expression '^' expression
                      | expression '>' expression
                      | expression ge expression
                      | expression '<' expression
                      | expression le expression
                      | expression eq expression
                      | expression ne expression'''
        if p[2] == '+':
            p[0] = '({}+{})'.format(p[1], p[3])
        elif p[2] == '-':
            p[0] = '({}-{})'.format(p[1], p[3])
        elif p[2] == '*':
            p[0] = '({}*{})'.format(p[1], p[3])
        elif p[2] == '/':
            p[0] = '({}/{})'.format(p[1], p[3])
        elif p[2] == '//':
            p[0] = '({}//{})'.format(p[1], p[3])
        elif p[2] == '^':
            p[0] = '({}^{})'.format(p[1], p[3])
        elif p[2] == '>':
            p[0] = '({}>{})'.format(p[1], p[3])
        elif p[2] == '>=':
            p[0] = '({}>={})'.format(p[1], p[3])
        elif p[2] == '<':
            p[0] = '({}<{})'.format(p[1], p[3])
        elif p[2] == '<=':
            p[0] = '({}<={})'.format(p[1], p[3])
        elif p[2] == '==':
            p[0] = '({}=={})'.format(p[1], p[3])
        elif p[2] == '!=':
            p[0] = '({}!={})'.format(p[1], p[3])

    def p_expression_uminus(self, p):
        '''expression : '-' expression %prec UMINUS'''
        p[0] = '({}{})'.format(p[1], p[2])

    def p_expression_group(self, p):
        '''expression : '(' expression ')' '''
        p[0] = '({})'.format(p[2])

    def p_expression_num(self, p):
        '''expression : NUM'''
        p[0] = p[1]

    def p_expression_pi(self, p):
        '''expression : PI'''
        self.names[p[1]] = 3.1416
        p[0] = p[1]

    def p_expression_name(self, p):
        '''expression : VAR'''
        p[0] = p[1]

    def p_expression_err(self, p):
        '''expression : ERR'''
        p[0] = p[1]
        self.errorMsg = "Error in line {}, pos {}".format(
            p.lineno(1), p.lexpos(1))

    def p_error(self, p):
        self.errorMsg = "Error: can't assign to literal in line {}".format(
            p.lineno)

    def read(self, filename):
        # Read input from the input file line-by-line into a list
        self.file = [line.rstrip('\n') + '\n' for line in open(filename)]

    def tokenize(self):
        out = str()
        for data in self.file:
            self.lexer.input(data)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                if tok.type in self.operator:
                    out += '{}/{} '.format(tok.value, self.operator[tok.type])
                else:
                    out += '{}/{} '.format(tok.value, tok.type)
            out = out[:-1] + '\n'
        return out

    def parse(self):
        out = str()
        for data in self.file:
            parse = self.parser.parse(data)
            if self.errorMsg:
                out += self.errorMsg
                self.errorMsg = str()
            else:
                out += parse
            out += '\n'
        return out

    def write(self, fileType):
        # Output file in 'type' file
        fileName = "out"
        file = codecs.open("{}.{}".format(fileName, fileType), 'w', 'utf-8')
        if fileType == 'tok':
            file.write(self.tokenize())
        elif fileType == 'txt':
            file.write(self.parse())
        file.close()


if __name__ == "__main__":
    testCases = "TestCases-2016-04-30-10.txt"  # the input text file
    m = CalculatorProject()
    m.read(testCases)
    m.write("tok")
    m.write("txt")
