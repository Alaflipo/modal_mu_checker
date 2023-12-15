from LTS import LTS
from modal_mu_formula import ModalMuFormula
import argparse
import os 
# importing package 
import matplotlib.pyplot as plt 


argParser = argparse.ArgumentParser()
argParser.add_argument("-lts", "--labeled_transition_system", help="File path to the labeled transtion system file (in .aut format)")
argParser.add_argument("-mcf", "--modal_calculus_formula", help="File path to the mu calculus formula (in .mcf format)")

def main(): 
        
    args = argParser.parse_args()
    lts = LTS(args.labeled_transition_system)
    print(lts)
    formula = ModalMuFormula(args.modal_calculus_formula)
    formula.print_results(args.modal_calculus_formula)
    result_states = lts.check_formula(formula)
    lts.print_results(result_states, False)
    result_states = lts.check_formula_el(formula)
    lts.print_results(result_states, True)

if __name__ == "__main__": 
    main() 
