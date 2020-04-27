# Calculator Parser
 A simple calculator parser with variables

## Objectives
The target of this project is to make an expression evaluator. The project is divided into 3 phases, the lexical analyzer, the syntactic analyzer, and the code generator.

## Requirement

 - Read input from the input file.
 - Evaluate the expression in each line and print output to the output file.
   -  For logical expression, print “True” if the result is true and “False” otherwise.
   - For assignment operation, print the value assigned to the variable (R-value) instead.
 - Support real numbers in both the decimal and scientific notation.
 - A variable should start with any character and may follow by any alphanumeric character or underscore.
 - If there are any errors in the input format, the program should be able to report the error.
 - Supported operators are
   - Addition (+)
   - Subtraction (−)
   - Multiplication (*)
   - Floating point division (=)
   - Integer division (==)
   - Exponent (^)
   - Greater than (>)
   - Greater than or equal to (>=)
   - Less than (<)
   - Less than or equal to (<=)
   - Equal to (==)
   - Not equal to (!=)
   - Parentheses ((...))
   - Assignment (=)
  - Any number of whitespace characters between tokens and operators is valid e.g. `2 +3== 5`
  - Only one assignment per one input line.
  - PI constant value is 3.1416
  - Precedence of operation is the same as in conventional programming languages.

## 1) Lexical analyzer
Recognize all integers, real numbers, operators, variables, constants and error tokens.  
Each line in the output file should be in the following format:

    <word>/<type> [<word>/<type>]*
For example,
### Input
    23+8
    2.5 * 0
    5NUM^ 3.0
    x=5
    10*x
    x =y
    x!=5
### Output
    23/NUM +/+ 8/NUM
    2.5/NUM */* 0/NUM
    5NUM/ERR ^/pow 3.0/NUM
    x/VAR =/= 5/NUM
    10/NUM */* x/VAR
    x/VAR =/= y/VAR
    x/VAR !=/!= 5/NUM

## 2) Syntactic analyzer

 - Correct grammar/result.
 - Working parser.
 - Use previously lexical analyzer module.
 - Identify every error with its line number and position in the line.  

Each line in the output file should be either the bracketing result of the parser or the error. The result from the parser is a parse tree. All tokens in the same brackets share the same parent node. At this stage, detecting declared variable is not necessary.
For example,

### Input

    23+8
    2.5 * 0
    5NUM^ 3.0
    x=5
    10*x
    x =y
    x!=5
  ### Output

    (23+8)
    (25*0)
    Error in line 3, pos 1
    (x=5)
    (10*x)
    (x=y) or Undefined variable y at line 5, pos 3
    (x!=5)

## 3) Code generator
Convert each line of expression or statement into 3-address codes

 - Correct translation for each operator  

The generated codes for each input line is separated by a blank line. Only print “ERROR” for invalid input lines. Let `print` be an address of the variable for printing purpose. In the case of boolean expression,

 - If the result is `true`, load `print` with the integer constant 1.
 - Otherwise, load `print` with the integer constant 0.

### List of available operators

    LD R #Im // Load a constant Im to R
    LD R1 R2 // Copy data in R2 to R1
    LD R Add // Load data in address Add to R
    ST Add R // Store data in R into address Add

Integer operations. All data are integers.

    ADD.i R1 R2 R3   // R1 = R2 + R3
    SUB.i R1 R2 R3   // R1 = R2 - R3
    MUL.i R1 R2 R3   // R1 = R2 * R3
    DIV.i R1 R2 R3   // R1 = R2 // R3
    EXP.i R1 R2 R3   // R1 = R2 ^ R3

Floating-point operations. All data are floats.

    ADD.f R1 R2 R3   // R1 = R2 + R3
    SUB.f R1 R2 R3   // R1 = R2 - R3
    MUL.f R1 R2 R3   // R1 = R2 * R3
    DIV.f R1 R2 R3   // R1 = R2 / R3
    EXP.f R1 R2 R3   // R1 = R2 ^ R3

Comparisons. R2 and R3 store floats. R1 stores an integer.

    LT.f R1 R2 R3   // R1 = (R2 < R3)? 1 : 0
    LE.f R1 R2 R3   // R1 = (R2 <= R3)? 1 : 0
    GT.f R1 R2 R3   // R1 = (R2 > R3)? 1 : 0
    GE.f R1 R2 R3   // R1 = (R2 >= R3)? 1 : 0
    EQ.f R1 R2 R3   // R1 = (R2 == R3)? 1 : 0
    NE.f R1 R2 R3   // R1 = (R2 != R3)? 1 : 0

Conversion

    FL.i R1 R2      // R1 = (float)R2
    INT.f R1 R2     // R1 = (int)R2

### Example input and output
Input

    23+8
    2.5 * 0
    5NUM^ 3.0
    x=5
    10*x
    x=y
    x!=5
Output

    LD R0 23
    LD R1 8
    ADD.i R2 R0 R1
    ST print R2
    
    LD R0 2.5
    LD R1 0
    FL.i R1 R1
    MUL.f R2 R0 R1
    ST print R2
    
    ERROR
    
    LD R0 5
    ST x R0
    LD R0 x
    LD R1 10
    MUL.i R2 R0 R1
    ST print R2
    
    ERROR
    
    LD R0 x
    LD R1 5
    FL.i R1 R1
    NE.f R2 R0 R1
    ST print R2
