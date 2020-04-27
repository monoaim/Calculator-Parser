# ------------------------------------------------------------
# calc_phase1+3.py
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
        self.result = []
        self.three = []
        self.count = 0
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
        r'(?<=\s)\S+(?=\s)|(?<=\A)\S+(?=\s)|(?<=\s)\S+(?=\Z)'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '{}'".format(t.value[0]))
        t.lexer.skip(1)

    precedence = (
        ('nonassoc', '>', 'ge', '<', 'le', 'eq',
         'ne'),  # Non-associative operators
        ('left', '+', '-'),
        ('left', '*', '/', 'Idivide'),
        ('right', '^'),
    )

    # dictionary of names (for storing variables)
    names = {}

    def p_statement_assign(self, p):
        '''statement : VAR '=' expression'''
        self.names[p[1]] = self.names[p[3]]
        self.three += ['ST {} {}'.format(p[1], p[3])]
        p[0] = p[3]

    def p_statement_expr(self, p):
        '''statement : expression'''
        self.three += ['ST print R{}'.format(self.count - 1)]
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
        op = str()
        if isinstance(self.names[p[1]], int) and isinstance(
                self.names[p[3]], int):
            op = 'i'
        elif isinstance(self.names[p[1]], int) and isinstance(
                self.names[p[3]], float):
            op = 'f'
            exec("self.names['{}'] = {}".format(p[1], float(self.names[p[1]])))
            self.three += ['FL.i {} {}'.format(p[1], p[1])]
        elif isinstance(self.names[p[1]], float) and isinstance(
                self.names[p[3]], int):
            op = 'f'
            exec("self.names['{}'] = {}".format(p[3], float(self.names[p[3]])))
            self.three += ['FL.i {} {}'.format(p[3], p[3])]
        elif isinstance(self.names[p[1]], float) and isinstance(
                self.names[p[3]], float):
            op = 'f'
        if p[2] == '+':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] + self.names[p[3]]))
            self.three += [
                'ADD.{} R{} {} {}'.format(op, self.count, p[1], p[3])
            ]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '-':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] - self.names[p[3]]))
            self.three += [
                'SUB.{} R{} {} {}'.format(op, self.count, p[1], p[3])
            ]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '*':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] * self.names[p[3]]))
            self.three += [
                'MUL.{} R{} {} {}'.format(op, self.count, p[1], p[3])
            ]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '/':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] / self.names[p[3]]))
            self.three += ['DIV.f R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '//':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] // self.names[p[3]]))
            self.three += ['DIV.i R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '^':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]]**self.names[p[3]]))
            self.three += [
                'EXP.{} R{} {} {}'.format(op, self.count, p[1], p[3])
            ]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '>':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] > self.names[p[3]]))
            self.three += ['GT.f R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '>=':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] >= self.names[p[3]]))
            self.three += ['GE.f R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '<':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] < self.names[p[3]]))
            self.three += ['LT.f R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '<=':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] <= self.names[p[3]]))
            self.three += ['LE.f R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '==':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] == self.names[p[3]]))
            self.three += ['EQ.f R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1
        elif p[2] == '!=':
            exec("self.names['R{}'] = {}".format(
                self.count, self.names[p[1]] != self.names[p[3]]))
            self.three += ['NE.f R{} {} {}'.format(self.count, p[1], p[3])]
            p[0] = 'R{}'.format(self.count)
            self.count = self.count + 1

    def p_expression_group(self, p):
        '''expression : '(' expression ')' '''
        p[0] = p[2]

    def p_expression_num(self, p):
        '''expression : NUM'''
        exec("self.names['R{}'] = {}".format(self.count, p[1]))
        self.three += ['LD R{} {}'.format(self.count, p[1])]
        p[0] = 'R{}'.format(self.count)
        self.count = self.count + 1

    def p_expression_pi(self, p):
        '''expression : PI'''
        self.names['PI'] = 3.1416
        p[0] = 'PI'

    def p_expression_name(self, p):
        '''expression : VAR'''
        exec("self.names['{}'] = 0".format(p[1]))
        exec("self.names['R{}'] = self.names['{}']".format(self.count, p[1]))
        self.three += ['LD R{} {}'.format(self.count, p[1])]
        p[0] = 'R{}'.format(self.count)
        self.count = self.count + 1

    def p_expression_err(self, p):
        '''expression : ERR'''
        p[0] = p[1]
        raise SyntaxError

    def p_error(self, p):
        raise SyntaxError

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
        for data in self.file:
            try:
                self.parser.parse(data)
                self.result += [self.three]
                self.three += ['\n']
            except Exception:
                self.result += [["ERROR\n\n"]]
            self.names.clear()
            self.count = 0
            self.three = list()
        return '\n'.join(map(str, [y for x in self.result for y in x]))

    def write(self, fileType):
        # Output file in 'type' file
        fileName = "out"
        file = codecs.open("{}.{}".format(fileName, fileType), 'w', 'utf-8')
        if fileType == 'tok':
            file.write(self.tokenize())
        elif fileType == 'asm':
            file.write(self.parse())
        file.close()


if __name__ == "__main__":
    testCases = "TestCases-2016-04-30-10.txt"  # the input text file
    m = CalculatorProject()
    m.read(testCases)
    m.write('asm')
