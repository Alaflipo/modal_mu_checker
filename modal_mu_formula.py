from __future__ import annotations
import string as string

true_first = 't'
false_first = 'f'
recursion_var_first = string.ascii_uppercase
logic_first = '('
mu_first = 'm'
nu_first = 'n'
diamond_first = '<'
box_first = '['
formula_first = true_first + false_first + recursion_var_first + logic_first + mu_first + nu_first + diamond_first + box_first
and_opp_first = '&'
or_opp_first = '|'
opp_first = and_opp_first + or_opp_first 
action_name_first = string.ascii_lowercase + '_' + string.digits

class Literal: 
    def __init__(self, boolean: bool): 
        self.literal: bool = boolean 
    
    def __str__(self): 
        return "true" if self.literal else "false"

class RecursionVar: 

    def __init__(self, variable_name: str, index: int, utype: str): 
        self.variable_name: str = variable_name
        self.index: int = index 
        self.bound: str = utype
    
    def __str__(self): 
        return self.variable_name
    
    def __repr__(self) -> str:
        return self.variable_name
    
class ActionVar: 

    def __init__(self, action_name: str): 
        self.action_name: str = action_name
    
    def __str__(self): 
        return self.action_name

class Operator: 

    def __init__(self, operator): 
        self.operator = operator

    def __str__(self): 
        return self.operator

class LogicFormula: 

    def __init__(self, lhs, opp: Operator, rhs):
        self.lhs = lhs 
        self.opp: Operator = opp 
        self.rhs = rhs  
    
    def __str__(self): 
        return '({lhs} {opp} {rhs})'.format(lhs=self.lhs, opp=self.opp, rhs=self.rhs)

def isinstance_group(formula, types: list): 
    for ftype in types: 
        if isinstance(formula, ftype): 
            return True 
    return False 

class MuFormula: 

    def __init__(self, recursion_var, formula): 
        self.recursion_var: RecursionVar = recursion_var
        self.formula = formula 
        mu_sub_formulas = self.find_all_mu_subformulas(formula)
        self.open_subformulas: list[MuFormula] = [g for g in mu_sub_formulas if self.is_open_subformula(g)]
        self.surrounding_binder = None 

    def find_all_mu_subformulas(self, formula) -> list[MuFormula]: 
        if (isinstance_group(formula, [Literal, RecursionVar])): 
            return []
        elif (isinstance_group(formula, [BoxFormula, DiamondFormula, NuFormula])): 
            return self.find_all_mu_subformulas(formula.formula)
        elif (isinstance(formula, LogicFormula)): 
            return self.find_all_mu_subformulas(formula.lhs) + self.find_all_mu_subformulas(formula.rhs)
        elif (isinstance(formula, MuFormula)): 
            return [formula] + self.find_all_mu_subformulas(formula.formula)

    def is_open_subformula(self, formula, seen_vars: list[RecursionVar] = []) -> bool: 
        if (isinstance(formula, RecursionVar)): 
            return formula not in seen_vars
        if (isinstance(formula, Literal)): 
            return False
        elif (isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            return self.is_open_subformula(formula.formula, seen_vars)
        elif (isinstance(formula, LogicFormula)): 
            return self.is_open_subformula(formula.lhs, seen_vars) or self.is_open_subformula(formula.rhs, seen_vars)
        elif (isinstance_group(formula, [MuFormula, NuFormula])): 
            return self.is_open_subformula(formula.formula, seen_vars + [formula.recursion_var])

    def __str__(self): 
        return 'mu {variable}. {formula}'.format(variable=self.recursion_var, formula=self.formula)     
    
    def __repr__(self) -> str:
        return 'mu {variable}. {formula}'.format(variable=self.recursion_var, formula=self.formula) 

class NuFormula: 

    def __init__(self, recursion_var, formula):
        self.recursion_var: RecursionVar = recursion_var
        self.formula = formula 
        nu_sub_formulas = self.find_all_nu_subformulas(formula)
        self.open_subformulas: list[NuFormula] = [g for g in nu_sub_formulas if self.is_open_subformula(g)]
        self.surrounding_binder = None 

    def find_all_nu_subformulas(self, formula) -> list[NuFormula]: 
        if (isinstance_group(formula, [Literal, RecursionVar])): 
            return []
        elif (isinstance_group(formula, [BoxFormula, DiamondFormula, MuFormula])): 
            return self.find_all_nu_subformulas(formula.formula)
        elif (isinstance(formula, LogicFormula)): 
            return self.find_all_nu_subformulas(formula.lhs) + self.find_all_nu_subformulas(formula.rhs)
        elif (isinstance(formula, NuFormula)): 
            return [formula] + self.find_all_nu_subformulas(formula.formula)

    def is_open_subformula(self, formula, seen_vars: list[RecursionVar] = []) -> bool: 
        if (isinstance(formula, RecursionVar)): 
            return formula not in seen_vars
        if (isinstance(formula, Literal)): 
            return False
        elif (isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            return self.is_open_subformula(formula.formula, seen_vars)
        elif (isinstance(formula, LogicFormula)): 
            return self.is_open_subformula(formula.lhs, seen_vars) or self.is_open_subformula(formula.rhs, seen_vars)
        elif (isinstance_group(formula, [MuFormula, NuFormula])): 
            return self.is_open_subformula(formula.formula, seen_vars + [formula.recursion_var])


    def __str__(self): 
        return 'nu {variable}. {formula}'.format(variable=self.recursion_var, formula=self.formula)     
    
    def __repr__(self) -> str:
        return 'nu {variable}. {formula}'.format(variable=self.recursion_var, formula=self.formula)   

class DiamondFormula: 
    
    def __init__(self, action, formula):
        self.action: ActionVar = action
        self.formula = formula 

    def __str__(self): 
        return '<{action}>{formula}'.format(action=self.action, formula=self.formula)     

class BoxFormula: 
    
    def __init__(self, action, formula):
        self.action: ActionVar = action
        self.formula = formula 

    def __str__(self): 
        return '[{action}]{formula}'.format(action=self.action, formula=self.formula)     

class ModalMuFormula: 

    def __init__(self, filepath): 
        self.formula_string = ''
        self.counter = 0 
        self.recursion_vars: list[RecursionVar] = []
        self.formula = self.read_and_parse_formula(filepath)
        self.ND = self.calc_ND(self.formula)
        self.AD = self.calc_AD(self.formula)
        self.dAD = self.calc_dAD(self.formula)
        self.set_surrounding_binders(self.formula)
        
    def expect(self, string_to_expect): 
        start = self.counter 
        end = start + len(string_to_expect)
        if self.formula_string[start: end] != string_to_expect:
            raise Exception("Did not find expected: {}".format(string_to_expect))
        else: 
            self.counter += len(string_to_expect)
    
    def skip_white_space(self): 
        while self.counter < len(self.formula_string) and self.formula_string[self.counter] == ' ' : 
            self.counter += 1
    
    def required_white_space(self): 
        if self.formula_string[self.counter] != ' ': 
            raise Exception("White space required!")
        self.skip_white_space()
    
    def parse_literal(self, boolean, string_bool) -> Literal: 
        self.expect(string_bool)
        self.skip_white_space()
        return Literal(boolean)

    def parse_recursion_var(self, new, utype=None) -> RecursionVar: 
        recursion_var = None 
        if new: 
            recursion_var = RecursionVar(self.formula_string[self.counter], len(self.recursion_vars), utype)
            self.recursion_vars.append(recursion_var)
        else: 
            for i, rv in enumerate(self.recursion_vars): 
                if (rv.variable_name == self.formula_string[self.counter]): 
                    recursion_var = self.recursion_vars[i]
        self.counter += 1 
        self.skip_white_space()
        return recursion_var
    
    def parse_action_name(self) -> ActionVar:
        action = '' 
        while self.counter < len(self.formula_string) and self.formula_string[self.counter] in action_name_first: 
            action += self.formula_string[self.counter]
            self.counter += 1
        return ActionVar(action)
    
    def parse_operator(self) -> Operator: 
        if (self.formula_string[self.counter] == and_opp_first): 
            self.expect("&&")
            self.skip_white_space()
            return Operator("&&")
        elif (self.formula_string[self.counter] == or_opp_first):
            self.expect("||")
            self.skip_white_space()
            return Operator("||") 

    def parse_logic_formula(self) -> LogicFormula: 
        self.expect("(")
        self.skip_white_space()
        rhs, lhs, opp = None, None, None 
        if (self.formula_string[self.counter] in formula_first):
            lhs = self.parse_formula()
        else: raise Exception("Left hand side in logic formula missing!")
        if (self.formula_string[self.counter] in opp_first): 
            opp = self.parse_operator()
        else: raise Exception("Operator in logic formula missing!")
        if (self.formula_string[self.counter] in formula_first): 
            rhs = self.parse_formula()
        else: raise Exception("Right hand side in logic formula missing!")
        self.expect(")")
        self.skip_white_space() 
        return LogicFormula(lhs, opp, rhs)
    
    def parse_mu_nu_formula(self, u_type) -> MuFormula | NuFormula: 
        self.expect(u_type)
        self.required_white_space() 
        recursion_var, formula = None, None  
        if self.formula_string[self.counter] in recursion_var_first: 
            recursion_var = self.parse_recursion_var(new=True, utype=u_type)
        else: raise Exception("No recursion variable found in {} formula".format(u_type))
        self.expect(".")
        self.skip_white_space()
        if self.formula_string[self.counter] in formula_first: 
            formula = self.parse_formula()
        else: raise Exception("No formula found in {} formula".format(u_type))
        return MuFormula(recursion_var, formula) if u_type == "mu" else NuFormula(recursion_var, formula)

    def parse_box_diamond_formula(self, expected: list[str]) -> DiamondFormula | BoxFormula: 
        self.expect(expected[0])
        self.skip_white_space()
        action, formula = None, None 
        if (self.formula_string[self.counter] in action_name_first): 
            action = self.parse_action_name()
        else: raise Exception("No action variable in {} found!".format(expected[0] + expected[1]))
        self.expect(expected[1])
        self.skip_white_space()
        if (self.formula_string[self.counter] in formula_first): 
            formula = self.parse_formula()
        else: raise Exception("No formula after {} found".format(expected[0] + expected[1]))
        return DiamondFormula(action, formula) if expected[0] == "<" else BoxFormula(action, formula)

    def read_and_parse_formula(self, filepath): 
        with open(filepath) as file: 
            self.formula_string = ''
            for line in file.readlines(): 
                if (line[0] != '%'): 
                    self.formula_string += line.strip()
        return self.parse_formula()

    def parse_formula(self):
        # Check if it is a true literal 
        if (self.formula_string[self.counter] == true_first):
            return self.parse_literal(True, 'true')
        # Check if it is a false literal 
        elif (self.formula_string[self.counter] == false_first):
            return self.parse_literal(False, 'false')
        # Check if we have found a recursion variable  
        elif (self.formula_string[self.counter] in recursion_var_first):
            return self.parse_recursion_var(new=False)
        # Check if we have found the start of a logic formula 
        elif (self.formula_string[self.counter] == logic_first): 
            return self.parse_logic_formula()
        # Check if we have found the start of a mu fixed point formula
        elif (self.formula_string[self.counter] == mu_first): 
            return self.parse_mu_nu_formula("mu") 
        # Check if we have found the start of a nu fixed point formula
        elif (self.formula_string[self.counter] == nu_first): 
            return self.parse_mu_nu_formula("nu") 
        # Check if we have found the start of a diamond modality formula
        elif (self.formula_string[self.counter] == diamond_first): 
            return self.parse_box_diamond_formula(['<', '>'])
        # Check if we have found the start of a box modality formula
        elif (self.formula_string[self.counter] == box_first): 
            return self.parse_box_diamond_formula(['[', ']'])
    
    def isinstance_group(self, formula, types: list): 
        for ftype in types: 
            if isinstance(formula, ftype): 
                return True 
        return False 
    
    def set_surrounding_binders(self, formula, last_seen=None):
        if (self.isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            self.set_surrounding_binders(formula.formula, last_seen)
        elif (isinstance(formula, LogicFormula)): 
            self.set_surrounding_binders(formula.lhs, last_seen)
            self.set_surrounding_binders(formula.rhs, last_seen)
        elif (isinstance(formula, MuFormula)): 
            formula.surrounding_binder = last_seen
            self.set_surrounding_binders(formula.formula, last_seen=formula)
        elif (isinstance(formula, NuFormula)): 
            formula.surrounding_binder = last_seen
            self.set_surrounding_binders(formula.formula, last_seen=formula)
    
    # Returns all mu or nu subformula's of a given formula 
    def search_mnu(self, formula, mu: bool): 
        if (self.isinstance_group(formula, [Literal, RecursionVar])): 
            return []
        elif (self.isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            return self.search_mnu(formula.formula, mu)
        elif (isinstance(formula, LogicFormula)): 
            return self.search_mnu(formula.lhs, mu) + self.search_mnu(formula.rhs, mu)
        elif (isinstance(formula, MuFormula)): 
            return [formula] + self.search_mnu(formula.formula, mu) if mu else self.search_mnu(formula.formula, mu)
        elif (isinstance(formula, NuFormula)): 
            return [formula] + self.search_mnu(formula.formula, mu) if not mu else self.search_mnu(formula.formula, mu)

    # Returns true if the formula has contains a recursion variable with the given name 
    def search_rec_var(self, formula, rec_var_name): 
        if (isinstance(formula, RecursionVar)):
            return rec_var_name == formula.variable_name 
        elif (self.isinstance_group(formula, [BoxFormula, DiamondFormula, MuFormula, NuFormula])): 
            return self.search_rec_var(formula.formula, rec_var_name)
        elif (isinstance(formula, LogicFormula)): 
            return self.search_rec_var(formula.lhs, rec_var_name) or self.search_rec_var(formula.rhs, rec_var_name)
        else: 
            return False 
    
    # Returns all mu or nu subformula's that depent on a given variable of a given formula 
    def search_mnu_dep(self, formula, rec_var: RecursionVar, mu: bool): 
        if (self.isinstance_group(formula, [Literal, RecursionVar])): 
            return []
        elif (self.isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            return self.search_mnu_dep(formula.formula, rec_var, mu)
        elif (isinstance(formula, LogicFormula)): 
            return self.search_mnu_dep(formula.lhs, rec_var, mu) + self.search_mnu_dep(formula.rhs, rec_var, mu)
        elif (isinstance(formula, MuFormula)): 
            return [formula] + self.search_mnu_dep(formula.formula, rec_var, mu) if mu else self.search_mnu_dep(formula.formula, rec_var, mu)
        elif (isinstance(formula, NuFormula)): 
            return [formula] + self.search_mnu_dep(formula.formula, rec_var, mu) if not mu else self.search_mnu_dep(formula.formula, rec_var, mu)

    # calculates the nesting depth 
    def calc_ND(self, formula) -> int: 
        if (self.isinstance_group(formula, [Literal, RecursionVar])): 
            return 0 
        elif (self.isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            return self.calc_ND(formula.formula)
        elif (isinstance(formula, LogicFormula)): 
            return max(self.calc_ND(formula.lhs), self.calc_ND(formula.rhs))
        elif (self.isinstance_group(formula, [MuFormula, NuFormula])): 
            return 1 + self.calc_ND(formula.formula)
    
    # calculates the alternation depth 
    def calc_AD(self, formula) -> int: 
        if (self.isinstance_group(formula, [Literal, RecursionVar])): 
            return 0 
        elif (self.isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            return self.calc_AD(formula.formula)
        elif (isinstance(formula, LogicFormula)): 
            return max(self.calc_AD(formula.lhs), self.calc_AD(formula.rhs))
        elif (isinstance(formula, MuFormula)): 
            return max(1, self.calc_AD(formula.formula), 1 + max(
                [0] + [self.calc_AD(g) for g in self.search_mnu(formula.formula, False)]))
        elif (isinstance(formula, NuFormula)): 
            return max(1, self.calc_AD(formula.formula), 1 + max(
                [0] + [self.calc_AD(g) for g in self.search_mnu(formula.formula, True)]))

    # calculates the dependent alternation depth 
    def calc_dAD(self, formula) -> int: 
        if (self.isinstance_group(formula, [Literal, RecursionVar])): 
            return 0 
        elif (self.isinstance_group(formula, [BoxFormula, DiamondFormula])): 
            return self.calc_dAD(formula.formula)
        elif (isinstance(formula, LogicFormula)): 
            return max(self.calc_dAD(formula.lhs), self.calc_dAD(formula.rhs))
        elif (isinstance(formula, MuFormula)): 
            return max(1, self.calc_dAD(formula.formula), 1 + max(
                [0] + [self.calc_dAD(g) for g in self.search_mnu_dep(formula.formula, formula.recursion_var, False) 
                       if self.search_rec_var(g, formula.recursion_var.variable_name)]))
        elif (isinstance(formula, NuFormula)): 
            return max(1, self.calc_dAD(formula.formula), 1 + max(
                [0] + [self.calc_dAD(g) for g in self.search_mnu_dep(formula.formula, formula.recursion_var, True) 
                       if self.search_rec_var(g, formula.recursion_var.variable_name)]))

    def print_results(self, filename: str): 
        print('\n----------------------------------------------')
        print('FORMULA:')
        print('Filename:', filename)
        print('Formula to check: ', self)
        print('Nesting depth:', self.ND)
        print('Alternation depth:', self.AD)
        print('Dependend alternation depth:', self.AD)

    def __str__(self): 
        return '{formula}'.format(formula=self.formula)
        