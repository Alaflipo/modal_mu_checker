from LTS import LTS
from modal_mu_formula import ModalMuFormula

def main(): 
    lts = LTS('./testcases/modal_operators/test.aut')
    print(lts)
    
    for i in range(9): 
        formula = ModalMuFormula('./testcases/boolean/form{form_number}.mcf'.format(form_number = (i + 1)))
        print(formula)

if __name__ == "__main__": 
    main() 
