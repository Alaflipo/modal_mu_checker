class State: 

    def __init__(self, name: int): 
        self.name: int = name 
        self.transitions: dict[str, list[State]] = {}
    
    def add_transition(self, end, label): 
        if label in self.transitions: 
            self.transitions[label].append(end)
        else: 
            self.transitions[label] = [end]
    
    def __str__(self): 
        output_string = "State {name}: \n".format(name = self.name)
        for label in self.transitions: 
            names = [state.name for state in self.transitions[label]]
            output_string += "{label}: {end_states} \n".format(label = label, end_states = names)
        return output_string

class LTS:
    
    def __init__(self, filepath):
        self.states: list[State] = []
        self.n_states: int = 0 
        self.n_trans: int = 0 
        self.initial_state: State = None 
        self.set_LTS_from_file(filepath) 

    def set_LTS_from_file(self, filepath): 
        with open(filepath) as file: 
            lines = [line.strip() for line in file.readlines()]
            info = lines[0].split(' ')[1][1:-1].split(',')
            self.n_trans = int(info[1])
            self.n_states = int(info[2])
            self.states = [State(int(number)) for number in range(self.n_states)]
            self.initial_state = self.states[int(info[0])]
            for line in lines[1:]: 
                transition = line[1:-1].split(',')
                start = int(transition[0])
                end = int(transition[2])
                label = transition[1][1:-1]
                self.states[start].add_transition(self.states[end], label)
    
    def __str__(self): 
        output_string = 'Number of states: {states} \nNumber of transitions: {trans} \nInitial state: {init}\n'.format(
            states=self.n_states, 
            trans=self.n_trans, 
            init=self.initial_state.name
        )
        for state in self.states: 
            output_string += "\n{state}".format(state=state)
        return output_string 
