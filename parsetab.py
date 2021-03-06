
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "nonassoc>ge<leeqneleft+-left*/Idivideright^ERR Idivide NUM PI VAR eq ge le nestatement : VAR '=' expressionstatement : expressionexpression : expression '+' expression\n                      | expression '-' expression\n                      | expression '*' expression\n                      | expression '/' expression\n                      | expression Idivide expression\n                      | expression '^' expression\n                      | expression '>' expression\n                      | expression ge expression\n                      | expression '<' expression\n                      | expression le expression\n                      | expression eq expression\n                      | expression ne expressionexpression : '(' expression ')' expression : NUMexpression : PIexpression : VARexpression : ERR"
    
_lr_action_items = {'VAR':([0,4,8,9,10,11,12,13,14,15,16,17,18,19,20,],[2,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'(':([0,4,8,9,10,11,12,13,14,15,16,17,18,19,20,],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,]),'NUM':([0,4,8,9,10,11,12,13,14,15,16,17,18,19,20,],[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,]),'PI':([0,4,8,9,10,11,12,13,14,15,16,17,18,19,20,],[6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,]),'ERR':([0,4,8,9,10,11,12,13,14,15,16,17,18,19,20,],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,]),'$end':([1,2,3,5,6,7,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[0,-18,-2,-16,-17,-19,-18,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,]),'=':([2,],[8,]),'+':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,9,-16,-17,-19,9,-18,9,-3,-4,-5,-6,-7,-8,9,9,9,9,9,9,-15,]),'-':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,10,-16,-17,-19,10,-18,10,-3,-4,-5,-6,-7,-8,10,10,10,10,10,10,-15,]),'*':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,11,-16,-17,-19,11,-18,11,11,11,-5,-6,-7,-8,11,11,11,11,11,11,-15,]),'/':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,12,-16,-17,-19,12,-18,12,12,12,-5,-6,-7,-8,12,12,12,12,12,12,-15,]),'Idivide':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,13,-16,-17,-19,13,-18,13,13,13,-5,-6,-7,-8,13,13,13,13,13,13,-15,]),'^':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,14,-16,-17,-19,14,-18,14,14,14,14,14,14,14,14,14,14,14,14,14,-15,]),'>':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,15,-16,-17,-19,15,-18,15,-3,-4,-5,-6,-7,-8,None,None,None,None,None,None,-15,]),'ge':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,16,-16,-17,-19,16,-18,16,-3,-4,-5,-6,-7,-8,None,None,None,None,None,None,-15,]),'<':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,17,-16,-17,-19,17,-18,17,-3,-4,-5,-6,-7,-8,None,None,None,None,None,None,-15,]),'le':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,18,-16,-17,-19,18,-18,18,-3,-4,-5,-6,-7,-8,None,None,None,None,None,None,-15,]),'eq':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,19,-16,-17,-19,19,-18,19,-3,-4,-5,-6,-7,-8,None,None,None,None,None,None,-15,]),'ne':([2,3,5,6,7,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-18,20,-16,-17,-19,20,-18,20,-3,-4,-5,-6,-7,-8,None,None,None,None,None,None,-15,]),')':([5,6,7,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,],[-16,-17,-19,36,-18,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([0,4,8,9,10,11,12,13,14,15,16,17,18,19,20,],[3,21,23,24,25,26,27,28,29,30,31,32,33,34,35,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> VAR = expression','statement',3,'p_statement_assign','calc_phase1+3.py',148),
  ('statement -> expression','statement',1,'p_statement_expr','calc_phase1+3.py',154),
  ('expression -> expression + expression','expression',3,'p_expression_binop','calc_phase1+3.py',159),
  ('expression -> expression - expression','expression',3,'p_expression_binop','calc_phase1+3.py',160),
  ('expression -> expression * expression','expression',3,'p_expression_binop','calc_phase1+3.py',161),
  ('expression -> expression / expression','expression',3,'p_expression_binop','calc_phase1+3.py',162),
  ('expression -> expression Idivide expression','expression',3,'p_expression_binop','calc_phase1+3.py',163),
  ('expression -> expression ^ expression','expression',3,'p_expression_binop','calc_phase1+3.py',164),
  ('expression -> expression > expression','expression',3,'p_expression_binop','calc_phase1+3.py',165),
  ('expression -> expression ge expression','expression',3,'p_expression_binop','calc_phase1+3.py',166),
  ('expression -> expression < expression','expression',3,'p_expression_binop','calc_phase1+3.py',167),
  ('expression -> expression le expression','expression',3,'p_expression_binop','calc_phase1+3.py',168),
  ('expression -> expression eq expression','expression',3,'p_expression_binop','calc_phase1+3.py',169),
  ('expression -> expression ne expression','expression',3,'p_expression_binop','calc_phase1+3.py',170),
  ('expression -> ( expression )','expression',3,'p_expression_group','calc_phase1+3.py',270),
  ('expression -> NUM','expression',1,'p_expression_num','calc_phase1+3.py',274),
  ('expression -> PI','expression',1,'p_expression_pi','calc_phase1+3.py',281),
  ('expression -> VAR','expression',1,'p_expression_name','calc_phase1+3.py',286),
  ('expression -> ERR','expression',1,'p_expression_err','calc_phase1+3.py',294),
]
