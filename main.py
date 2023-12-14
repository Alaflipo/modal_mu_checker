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
    folder = 'dining'
    files_lts = ['dining_{}.aut'.format(i+2) for i in range(10)]
    # files_formulas = [file for file in os.listdir('./testcases/{}'.format(folder)) if file[-3:] == 'mcf']
    files_formulas = ['invariantly_inevitably_eat.mcf', 'invariantly_plato_starves.mcf', 'invariantly_possibly_eat.mcf', 'plato_infinitely_often_can_eat.mcf']
    
    results_naive = [[0] * len(files_lts) for _ in range(len(files_formulas))]
    verdicts_naive = [[False] * len(files_lts) for _ in range(len(files_formulas))]
    results_el = [[0] * len(files_lts) for _ in range(len(files_formulas))]
    verdicts_el = [[False] * len(files_lts) for _ in range(len(files_formulas))]
    for j, file_lts in enumerate(files_lts): 
        lts_filepath = './testcases/{folder}/{file}'.format(folder=folder, file=file_lts)
        print('\nLTS file:', file_lts)
        lts = LTS(lts_filepath)
        for i, file_formula in enumerate(files_formulas): 
            filepath_formula = './testcases/{folder}/{file}'.format(folder=folder, file=file_formula)
            formula = ModalMuFormula(filepath_formula)
            formula.print_results(file_formula)
            result_states = lts.check_formula(formula)
            results_naive[i][j] = lts.fixed_point_iterations
            verdicts_naive[i][j] = lts.get_verdict(result_states)
            lts.print_results(result_states, False)
            result_states = lts.check_formula_el(formula)
            results_el[i][j] = lts.fixed_point_iterations
            verdicts_el[i][j] = lts.get_verdict(result_states)
            lts.print_results(result_states, True)
    
    print('------------------------------------')
    for i, verdict_list in enumerate([verdicts_naive, verdicts_el]): 
        print('\nNaive verdict:' if i==0 else '\nEmerson lei verdict:')
        for formula_index in range(len(results_naive)):
            print(files_formulas[formula_index])
            print(verdict_list[formula_index])
    
    for formula_index in range(len(results_naive)):
        lts_numbers = [(i+2) for i in range(10)]
        plt.plot(lts_numbers, results_naive[formula_index], label = "naive") 
        plt.plot(lts_numbers, results_el[formula_index], label = "emerson-lei") 
        plt.xticks(range(lts_numbers[0], lts_numbers[-1] + 1))
        plt.xlabel('Group size')  
        plt.ylabel('Fixed point iterations')  
        plt.title(files_formulas[formula_index]) 
        plt.legend() 
        plt.savefig('results/{}.png'.format(files_formulas[formula_index]))
        plt.show()
        
    # args = argParser.parse_args()
    # lts = LTS(args.labeled_transition_system)
    # print(lts)
    # formula = ModalMuFormula(args.modal_calculus_formula)
    # print(formula)
    # print(formula.ND, formula.AD, formula.dAD)
    # print(lts.check_formula(formula))
    # print(lts.fixed_point_iterations)
    # print(lts.check_formula_el(formula))
    # print(lts.fixed_point_iterations)

if __name__ == "__main__": 
    main() 
