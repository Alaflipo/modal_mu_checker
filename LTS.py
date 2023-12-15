from modal_mu_formula import ModalMuFormula, Literal, RecursionVar, ActionVar, Operator
from modal_mu_formula import LogicFormula, MuFormula, NuFormula, DiamondFormula, BoxFormula

class State: 

    def __init__(self, name: int): 
        self.name: int = name 
        self.transitions: dict[str, set[State]] = {}
    
    def add_transition(self, end, label): 
        if label in self.transitions: 
            self.transitions[label].add(end)
        else: 
            self.transitions[label] = set([end])
    
    def get_all_out(self): 
        all_out = set()
        for action in self.transitions: 
            all_out = all_out | self.transitions[action]
        return set(all_out)
    
    def __str__(self): 
        output_string = "State {name}: \n".format(name = self.name)
        for label in self.transitions: 
            names = [state.name for state in self.transitions[label]]
            output_string += "{label}: {end_states} \n".format(label = label, end_states = names)
        return output_string
    
    def __repr__(self): 
        return str(self.name)

class LTS:
    
    def __init__(self, filepath):
        self.states: set[State] = set()
        self.n_states: int = 0 
        self.n_trans: int = 0 
        self.initial_state: State = None 
        self.recursion_vars: list[RecursionVar] = []
        self.recursion_sets: list[set[State]] = []
        self.fixed_point_iterations: int = 0 
        self.set_LTS_from_file(filepath) 
    
    def check_formula(self, formula: ModalMuFormula) -> set[State]: 
        self.recursion_vars = formula.recursion_vars
        self.recursion_sets = [None] * len(self.recursion_vars)
        self.fixed_point_iterations = 0 
        return self.eval(formula.formula)
    
    def check_formula_el(self, formula: ModalMuFormula) -> set[State]: 
        self.recursion_vars = formula.recursion_vars
        self.recursion_sets = []
        self.fixed_point_iterations = 0 
        for var in self.recursion_vars: 
            if (var.bound == "mu"): 
                self.recursion_sets.append(set())
            else: 
                self.recursion_sets.append(self.states)
        assert len(self.recursion_sets) == len(self.recursion_vars)
        return self.eval_el(formula.formula)
    
    def eval(self, formula) -> set[State]: 
        if (isinstance(formula, RecursionVar)): 
            return self.recursion_sets[formula.index]
        elif (isinstance(formula, Literal)): 
            return self.states if formula.literal else set()
        elif (isinstance(formula, LogicFormula)): 
            if (formula.opp.operator == "&&"): 
                return self.eval(formula.lhs) & self.eval(formula.rhs)
            elif (formula.opp.operator == "||"): 
                return self.eval(formula.rhs) | self.eval(formula.lhs) 
        elif (isinstance(formula, BoxFormula)): 
            found_states = set() 
            for state in self.states: 
                if formula.action.action_name in state.transitions: 
                    end_states = state.transitions[formula.action.action_name]
                    all_transitions_hold = True 
                    for end_state in end_states: 
                        if (end_state not in self.eval(formula.formula)): 
                            all_transitions_hold = False 
                            break 
                    if all_transitions_hold: found_states.add(state)
                else: 
                    found_states.add(state)
            return found_states 
        elif (isinstance(formula, DiamondFormula)): 
            found_states = set() 
            for state in self.states: 
                if formula.action.action_name in state.transitions: 
                    end_states = state.transitions[formula.action.action_name]
                    transition_holds = False 
                    for end_state in end_states: 
                        if (end_state in self.eval(formula.formula)): 
                            transition_holds = True 
                            break 
                    if transition_holds: found_states.add(state)
            return found_states 
        elif (isinstance(formula, NuFormula)): 
            self.recursion_sets[formula.recursion_var.index] = self.states
            rv_prime = set() 
            while (self.recursion_sets[formula.recursion_var.index] != rv_prime): 
                rv_prime = self.recursion_sets[formula.recursion_var.index]
                self.recursion_sets[formula.recursion_var.index] = self.eval(formula.formula)
                self.fixed_point_iterations += 1
            return self.recursion_sets[formula.recursion_var.index]
        elif (isinstance(formula, MuFormula)): 
            self.recursion_sets[formula.recursion_var.index] = set()
            rv_prime = None
            while (self.recursion_sets[formula.recursion_var.index] != rv_prime): 
                rv_prime = self.recursion_sets[formula.recursion_var.index]
                self.recursion_sets[formula.recursion_var.index] = self.eval(formula.formula)
                self.fixed_point_iterations += 1
            return self.recursion_sets[formula.recursion_var.index]

    def eval_el(self, formula) -> set[State]: 
        if (isinstance(formula, RecursionVar)): 
            return self.recursion_sets[formula.index]
        elif (isinstance(formula, Literal)): 
            return self.states if formula.literal else set()
        elif (isinstance(formula, LogicFormula)): 
            if (formula.opp.operator == "&&"): 
                return self.eval_el(formula.lhs) & self.eval_el(formula.rhs)
            elif (formula.opp.operator == "||"): 
                return self.eval_el(formula.rhs) | self.eval_el(formula.lhs) 
        elif (isinstance(formula, BoxFormula)): 
            found_states = set() 
            for state in self.states: 
                if formula.action.action_name in state.transitions: 
                    end_states = state.transitions[formula.action.action_name]
                    all_transitions_hold = True 
                    for end_state in end_states: 
                        if (end_state not in self.eval_el(formula.formula)): 
                            all_transitions_hold = False 
                            break 
                    if all_transitions_hold: found_states.add(state)
                else: 
                    found_states.add(state)
            return found_states 
        elif (isinstance(formula, DiamondFormula)): 
            found_states = set() 
            for state in self.states: 
                if formula.action.action_name in state.transitions: 
                    end_states = state.transitions[formula.action.action_name]
                    transition_holds = False 
                    for end_state in end_states: 
                        if (end_state in self.eval_el(formula.formula)): 
                            transition_holds = True 
                            break 
                    if transition_holds: found_states.add(state)
            return found_states 
        elif (isinstance(formula, NuFormula)): 
            if (isinstance(formula.surrounding_binder, MuFormula)):
                for open_sub_formulae in formula.open_subformulas: 
                    self.recursion_sets[open_sub_formulae.recursion_var.index] = set()
            X_old = None 
            while (X_old != self.recursion_sets[formula.recursion_var.index]):
                X_old = self.recursion_sets[formula.recursion_var.index]
                self.recursion_sets[formula.recursion_var.index] = self.eval_el(formula.formula)
                self.fixed_point_iterations += 1
            return self.recursion_sets[formula.recursion_var.index]
        
        elif (isinstance(formula, MuFormula)): 
            if (isinstance(formula.surrounding_binder, NuFormula)):
                for open_sub_formulae in formula.open_subformulas: 
                    self.recursion_sets[open_sub_formulae.recursion_var.index] = set()
            X_old = None 
            while (X_old != self.recursion_sets[formula.recursion_var.index]):
                X_old = self.recursion_sets[formula.recursion_var.index]
                self.recursion_sets[formula.recursion_var.index] = self.eval_el(formula.formula)
                self.fixed_point_iterations += 1
            return self.recursion_sets[formula.recursion_var.index]

    def set_LTS_from_file(self, filepath): 
        with open(filepath) as file: 
            lines = [line.strip() for line in file.readlines()]
            info = lines[0].split(' ')[1][1:-1].split(',')
            self.n_trans = int(info[1])
            self.n_states = int(info[2])
            states_list = [State(int(number)) for number in range(self.n_states)]
            self.initial_state = states_list[int(info[0])]
            for line in lines[1:]: 
                transition = line[1:-1].split(',')
                start = int(transition[0])
                end = int(transition[2])
                label = transition[1][1:-1]
                states_list[start].add_transition(states_list[end], label)
            self.states = set(states_list)
            

    def get_verdict(self, results): 
        return self.initial_state in results

    def print_results(self, results, el: bool): 
        print('\nLTS CHECK {}'.format("Emerson-Lei" if el else "Naive"))
        print('Amount of states the formula holds:', len(results))
        print('Verdict:', self.get_verdict(results))
        print('Fix point iterations:', self.fixed_point_iterations)
    
    def __str__(self): 
        output_string = 'Number of states: {states} \nNumber of transitions: {trans} \nInitial state: {init}\n'.format(
            states=self.n_states, 
            trans=self.n_trans, 
            init=self.initial_state.name
        )
        for state in self.states: 
            output_string += "\n{state}".format(state=state)
        return output_string 
