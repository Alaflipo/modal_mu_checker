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
action_name_first = string.ascii_lowercase

class Literal: 
    def __init__(self, boolean: bool): 
        self.literal: bool = boolean 
    
    def __str__(self): 
        return "true" if self.literal else "false"

class RecursionVar: 

    def __init__(self, variable_name: str): 
        self.variable_name: str = variable_name
    
    def __str__(self): 
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

    def __init__(self, lhs, opp, rhs):
        self.lhs = lhs 
        self.opp = opp 
        self.rhs = rhs  
    
    def __str__(self): 
        return '({lhs} {opp} {rhs})'.format(lhs=self.lhs, opp=self.opp, rhs=self.rhs)

class MuFormula: 

    def __init__(self, recursion_var, formula): 
        self.recursion_var = recursion_var
        self.formula = formula 

    def __str__(self): 
        return 'mu {variable}. {formula}'.format(variable=self.recursion_var, formula=self.formula)     

class NuFormula: 

    def __init__(self, recursion_var, formula):
        self.recursion_var = recursion_var
        self.formula = formula 

    def __str__(self): 
        return 'nu {variable}. {formula}'.format(variable=self.recursion_var, formula=self.formula)     

class DiamondFormula: 
    
    def __init__(self, action, formula):
        self.action = action
        self.formula = formula 

    def __str__(self): 
        return '<{action}>{formula}'.format(action=self.action, formula=self.formula)     

class BoxFormula: 
    
    def __init__(self, action, formula):
        self.action = action
        self.formula = formula 

    def __str__(self): 
        return '[{action}]{formula}'.format(action=self.action, formula=self.formula)     



class ModalMuFormula: 

    def __init__(self, filepath): 
        self.formula_string = ''
        self.counter = 0 
        self.formula = self.read_and_parse_formula(filepath)
    
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

    def parse_recursion_var(self) -> RecursionVar: 
        recursion_var = RecursionVar(self.formula_string[self.counter])
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
            recursion_var = self.parse_recursion_var()
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
            self.formula_string = file.read().strip()
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
            return self.parse_recursion_var()
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
            
    def __str__(self): 
        return '{formula}'.format(formula=self.formula)
        