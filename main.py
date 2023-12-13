from LTS import LTS
from modal_mu_formula import ModalMuFormula
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-lts", "--lts", help="File path to the labeled transtion system file (in .aut format)")
argParser.add_argument("-mcf", "--mcf", help="File path to the mu calculus formula (in .mcf format)")

def main(): 
    # folders = ['boolean', 'combined', 'fixpoints_only', 'modal_operators']
    # for folder in folders: 
    #     files = [file for file in os.listdir('./testcases/{}'.format(folder)) if file[-3:] == 'mcf']
    #     for file in files: 
    #         filepath = './testcases/{folder}/{file}'.format(folder=folder, file=file)
    #         with open(filepath) as f: 
    #             print("\n" + f.read().strip())
    #         formula = ModalMuFormula(filepath)
    #         print(formula)
    args = argParser.parse_args()
    lts = LTS(args.lts)
    print(lts)
    formula = ModalMuFormula(args.mcf)
    print(formula)

if __name__ == "__main__": 
    main() 
