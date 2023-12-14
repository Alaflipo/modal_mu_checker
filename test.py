class Test: 

    def __init__(self, name): 
        self.name = name
    
    def __repr__(self): 
        return self.name


A = set([Test("1")])
B = A 
A = set([Test("2")])

print(A,B)
