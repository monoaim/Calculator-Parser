# ------------------------------------------------------------
# calc_phase1+3.py
#
# A simple calculator with variables and code generator.
# Generates 3-address code from arithmetic expressions.
#
# 58090046 Araya Siriadun
# ------------------------------------------------------------
"""
Calculator Parser Phase 3: Code Generator

This module implements a lexical analyzer and parser for arithmetic
expressions, generating 3-address code output for a stack-based machine.

Supported operations:
    - Arithmetic: +, -, *, /, //, ^
    - Comparison: >, >=, <, <=, ==, !=
    - Assignment: =
    - Parentheses for grouping
    - Variables and PI constant
"""
import ply.lex as lex
import ply.yacc as yacc
import math


class CalculatorProject:
    """
    Calculator project implementing lexical analysis, parsing,
    and 3-address code generation for arithmetic expressions.
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

    # Binary operation instruction mapping
    _binop_instructions = {
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV',
        '//': 'DIV',
        '^': 'EXP',
        '>': 'GT',
        '>=': 'GE',
        '<': 'LT',
        '<=': 'LE',
        '==': 'EQ',
        '!=': 'NE',
    }

    # Operations that compute the result using corresponding Python operators
    _binop_funcs = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '//': lambda a, b: a // b,
        '^': lambda a, b: a ** b,
        '>': lambda a, b: a > b,
        '>=': lambda a, b: a >= b,
        '<': lambda a, b: a < b,
        '<=': lambda a, b: a <= b,
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b,
    }

    t_ignore = ' \t'

    def __init__(self):
        """Initialize the calculator with lexer and parser."""
        self.file = None
        self.result = []
        self.three = []
        self.count = 0
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
        r'(?<=\s)\S+(?=\s)|(?<=\A)\S+(?=\s)|(?<=\s)\S+(?=\Z)'
        """Match error tokens (invalid characters surrounded by whitespace)."""
        return t

    def t_newline(self, t):
        r'\n+'
        """Track line numbers."""
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        """Handle illegal characters by skipping them."""
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

    def _get_type_suffix(self, left_val, right_val):
        """
        Determine the type suffix ('i' for integer, 'f' for float)
        based on operand types.

        Returns:
            tuple: (suffix, needs_left_convert, needs_right_convert)
        """
        left_is_int = isinstance(left_val, int)
        right_is_int = isinstance(right_val, int)

        if left_is_int and right_is_int:
            return 'i', False, False
        elif left_is_int and not right_is_int:
            return 'f', True, False
        elif not left_is_int and right_is_int:
            return 'f', False, True
        else:
            return 'f', False, False

    def _emit_binop(self, p, operator):
        """
        Emit 3-address code for a binary operation.

        Args:
            p: Parser production
            operator: The operator string ('+', '-', '*', etc.)
        """
        left_val = self.names[p[1]]
        right_val = self.names[p[3]]

        suffix, convert_left, convert_right = self._get_type_suffix(left_val, right_val)

        # Emit type conversion instructions if needed
        if convert_left:
            self.names[p[1]] = float(left_val)
            self.three.append('FL.i {} {}'.format(p[1], p[1]))
            left_val = self.names[p[1]]
        if convert_right:
            self.names[p[3]] = float(right_val)
            self.three.append('FL.i {} {}'.format(p[3], p[3]))
            right_val = self.names[p[3]]

        # Compute result using the operator function
        result = self._binop_funcs[operator](left_val, right_val)
        reg_name = 'R{}'.format(self.count)
        self.names[reg_name] = result

        # Get instruction name
        instr = self._binop_instructions[operator]

        # Special handling for division operators (always specific type)
        if operator == '/':
            suffix = 'f'  # Float division always produces float
        elif operator == '//':
            suffix = 'i'  # Integer division always produces int

        # Comparison operators always use float suffix for instruction
        if operator in ('>', '>=', '<', '<=', '==', '!='):
            suffix = 'f'

        self.three.append('{}.{} R{} {} {}'.format(instr, suffix, self.count, p[1], p[3]))
        p[0] = reg_name
        self.count += 1

    def p_statement_assign(self, p):
        '''statement : VAR '=' expression'''
        self.names[p[1]] = self.names[p[3]]
        self.three.append('ST {} {}'.format(p[1], p[3]))
        p[0] = p[3]

    def p_statement_expr(self, p):
        '''statement : expression'''
        self.three.append('ST print R{}'.format(self.count - 1))
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
        self._emit_binop(p, p[2])

    def p_expression_group(self, p):
        '''expression : '(' expression ')' '''
        p[0] = p[2]

    def p_expression_num(self, p):
        '''expression : NUM'''
        reg_name = 'R{}'.format(self.count)
        self.names[reg_name] = p[1]
        self.three.append('LD R{} {}'.format(self.count, p[1]))
        p[0] = reg_name
        self.count += 1

    def p_expression_pi(self, p):
        '''expression : PI'''
        self.names['PI'] = math.pi
        p[0] = 'PI'

    def p_expression_name(self, p):
        '''expression : VAR'''
        if p[1] not in self.names:
            self.names[p[1]] = 0
        reg_name = 'R{}'.format(self.count)
        self.names[reg_name] = self.names[p[1]]
        self.three.append('LD R{} {}'.format(self.count, p[1]))
        p[0] = reg_name
        self.count += 1

    def p_expression_err(self, p):
        '''expression : ERR'''
        p[0] = p[1]
        raise SyntaxError

    def p_error(self, p):
        """Handle parsing errors."""
        raise SyntaxError

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
        Parse all lines in the loaded file and generate 3-address code.

        Returns:
            str: Generated assembly code, with blank lines separating statements
        """
        for data in self.file:
            try:
                self.parser.parse(data)
                self.result.append(self.three)
                self.three.append('\n')
            except SyntaxError:
                self.result.append(["ERROR\n\n"])
            self.names.clear()
            self.count = 0
            self.three = []
        return '\n'.join(str(item) for sublist in self.result for item in sublist)

    def write(self, file_type):
        """
        Write output to a file.

        Args:
            file_type: Output format ('tok' for tokens, 'asm' for assembly)
        """
        filename = "out.{}".format(file_type)
        with open(filename, 'w', encoding='utf-8') as f:
            if file_type == 'tok':
                f.write(self.tokenize())
            elif file_type == 'asm':
                f.write(self.parse())


if __name__ == "__main__":
    test_cases = "TestCases-2016-04-30-10.txt"  # the input text file
    calculator = CalculatorProject()
    calculator.read(test_cases)
    calculator.write('asm')
