# ------------------------------------------------------------
# calc_phase1+2.py
#
# A simple calculator with variables and syntactic analyzer.
# Outputs parse trees showing operator precedence through bracketing.
#
# 58090046 Araya Siriadun
# ------------------------------------------------------------
"""
Calculator Parser Phase 2: Syntactic Analyzer

This module implements a lexical analyzer and parser for arithmetic
expressions, outputting parse trees in fully-bracketed notation.

Supported operations:
    - Arithmetic: +, -, *, /, //, ^
    - Comparison: >, >=, <, <=, ==, !=
    - Assignment: =
    - Parentheses for grouping
    - Variables and PI constant
"""
import ply.lex as lex
import ply.yacc as yacc


class CalculatorProject:
    """
    Calculator project implementing lexical analysis and parsing
    for arithmetic expressions with parse tree output.
    """
    # List of token names
    tokens = ('NUM', 'Idivide', 'ge', 'le', 'eq', 'ne', 'VAR', 'PI', 'ERR')

    literals = ['+', '-', '*', '/', '>', '^', '<', '=', '(', ')']

    # Mapping from token types to operator symbols for output formatting
    operator = {
        'Idivide': '//',
        'ge': '>=',
        'le': '<=',
        'eq': '==',
        'ne': '!=',
    }

    t_ignore = ' \t'

    def __init__(self):
        """Initialize the calculator with lexer and parser."""
        self.file = None
        self.errorMsg = ''

        # Build the lexer and parser
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def t_NUM(self, t):
        r'-?(?:[1-9]\d*|0)(?:\.\d+)?(?:[eE][+-]?\d+)?'
        """Match integer or floating-point numbers, including scientific notation."""
        if '.' in t.value or 'e' in t.value.lower():
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_PI(self, t):
        r'PI\b'
        """Match the PI constant."""
        return t

    def t_VAR(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        """Match variable names (identifiers)."""
        return t

    def t_Idivide(self, t):
        r'//'
        """Match integer division operator."""
        return t

    def t_ge(self, t):
        r'>='
        """Match greater-than-or-equal operator."""
        return t

    def t_le(self, t):
        r'<='
        """Match less-than-or-equal operator."""
        return t

    def t_eq(self, t):
        r'=='
        """Match equality operator."""
        return t

    def t_ne(self, t):
        r'!='
        """Match not-equal operator."""
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
        r'\S'
        """Match any non-whitespace character as an error token."""
        return t

    def t_newline(self, t):
        r'\n+'
        """Track line numbers."""
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        """Handle illegal characters by skipping them."""
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
        # Output bracketed expression with the operator
        p[0] = '({}{}{})'  .format(p[1], p[2], p[3])

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
        """Handle parsing errors."""
        self.errorMsg = "Error: can't assign to literal in line {}".format(
            p.lineno)

    def read(self, filename):
        """
        Read input from a file line-by-line.

        Args:
            filename: Path to the input file
        """
        with open(filename, 'r', encoding='utf-8') as f:
            self.file = [line.rstrip('\n') + '\n' for line in f]

    def tokenize(self):
        """
        Tokenize all lines in the loaded file.

        Returns:
            str: Formatted token output, one line per input line
        """
        output_lines = []
        for data in self.file:
            self.lexer.input(data)
            tokens = []
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                if tok.type in self.operator:
                    tokens.append('{}/{}'.format(tok.value, self.operator[tok.type]))
                else:
                    tokens.append('{}/{}'.format(tok.value, tok.type))
            output_lines.append(' '.join(tokens))
        return '\n'.join(output_lines) + '\n'

    def parse(self):
        """
        Parse all lines in the loaded file.

        Returns:
            str: Parse tree output or error messages
        """
        output_lines = []
        for data in self.file:
            result = self.parser.parse(data)
            if self.errorMsg:
                output_lines.append(self.errorMsg)
                self.errorMsg = ''
            else:
                output_lines.append(str(result))
        return '\n'.join(output_lines) + '\n'

    def write(self, file_type):
        """
        Write output to a file.

        Args:
            file_type: Output format ('tok' for tokens, 'txt' for parse tree)
        """
        filename = "out.{}".format(file_type)
        with open(filename, 'w', encoding='utf-8') as f:
            if file_type == 'tok':
                f.write(self.tokenize())
            elif file_type == 'txt':
                f.write(self.parse())


if __name__ == "__main__":
    test_cases = "TestCases-2016-04-30-10.txt"  # the input text file
    calculator = CalculatorProject()
    calculator.read(test_cases)
    calculator.write("tok")
    calculator.write("txt")
