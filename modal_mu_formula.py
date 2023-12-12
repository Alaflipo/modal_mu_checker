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
        return '{lhs} {opp} {rhs}'.format(lhs=self.lhs, opp=self.opp, rhs=self.rhs)
        
class ModalMuFormula: 

    def __init__(self, filepath): 
        self.formula_string = ''
        self.counter = 0 
        self.formula = self.read_and_parse_formula(filepath)
    
    def expect(self, string_to_expect): 
        start = self.counter 
        end = start + len(string_to_expect)
        if self.formula_string[start: end] != string_to_expect:
            print("error")
        else: 
            self.counter += len(string_to_expect)
    
    def skip_white_space(self): 
        while self.counter < len(self.formula_string) and self.formula_string[self.counter] == ' ' : 
            self.counter += 1
    
    def parse_literal(self, boolean, string_bool): 
        self.expect(string_bool)
        self.skip_white_space()
        return Literal(boolean)

    def parse_recursion_var(self): 
        recursion_var = RecursionVar(self.formula_string[self.counter])
        self.counter += 1 
        self.skip_white_space()
        return recursion_var
    
    def parse_operator(self): 
        if (self.formula_string[self.counter] == and_opp_first): 
            self.expect("&&")
            self.skip_white_space()
            return Operator("&&")
        elif (self.formula_string[self.counter] == or_opp_first):
            self.expect("||")
            self.skip_white_space()
            return Operator("||") 

    def parse_logic_formula(self): 
        self.expect("(")
        self.skip_white_space()
        rhs, lhs, opp = None, None, None 
        if (self.formula_string[self.counter] in formula_first):
            lhs = self.parse_formula()
        else: print('error')
        if (self.formula_string[self.counter] in opp_first): 
            opp = self.parse_operator()
        else: print('error')
        if (self.formula_string[self.counter] in formula_first): 
            rhs = self.parse_formula()
        else: print('error')
        self.expect(")")
        self.skip_white_space() 
        return LogicFormula(lhs, opp, rhs)
    
    def parse_mu_formula(self): 
        pass 

    def parse_nu_formula(self): 
        pass 

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
        elif (self.formula_string[self.counter] == mu_first): 
            return self.parse_mu_formula() 
            
    def __str__(self): 
        return '{formula}'.format(formula=self.formula)
        