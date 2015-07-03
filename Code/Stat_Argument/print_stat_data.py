#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import os


def main():
    i = True
    while i == True:
        prompt = raw_input("\nEnter Cluster Name: ")
        if prompt == 'IC_2391' or prompt == '1':
            cluster = 'IC_2391'
            print '\n', cluster, '\n'
            i == False
            break
        if prompt == 'NGC_6475' or prompt == '2':
            cluster = 'NGC_6475'
            print '\n', cluster, '\n'
            i == False
            break
        if prompt == 'NGC_2451' or prompt == '3':
            cluster = 'NGC_2451'
            print '\n', cluster, '\n'
            i == False
            break
        if prompt == 'NGC_2516' or prompt == '4':
            cluster = 'NGC_2516'
            print '\n', cluster, '\n'
            i == False
            break
        if prompt == 'NGC_3532' or prompt == '5':
            cluster = 'NGC_3532'
            print '\n', cluster, '\n'
            i == False
            break
        if prompt == 'IC_2602' or prompt == '6':
            cluster = 'IC_2602'
            print '\n', cluster, '\n'
            i == False
            break
        else:
            i == True
            
    
    # Loads stat data
    data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Stat_Argument/Stat_Data/'+cluster+'_stat_data.npz')
    
    poisson_J = data['P_J']
    poisson_H = data['P_H']
    poisson_K = data['P_K']
    comp_names = data['Comp_Names']

    i = True
    while i == True:
        prompt = raw_input("Print Companion Names? (Y|N): ")
        if prompt == 'Y' or prompt == 'y':
            print '\n'
            for n in range(len(comp_names)):
                print comp_names[n]
            i == False
            print '\n'
            break
        elif prompt == 'N' or prompt == 'n':
            i == False
            break
        else:
            print("Please Enter (Y|N). ")
            i == True
    
    i = True
    while i == True:
        prompt = raw_input("Print J, H, and K? (Y|N): ")
        if prompt == 'Y' or prompt == 'y':
            print '\nJ-band:'
            for n in range(len(poisson_J)):
                print poisson_J[n]
            i == False
            print '\nH-Band:'
            for n in range(len(poisson_H)):
                print poisson_H[n]
            i == False
            print '\nK-Band:'
            for n in range(len(poisson_K)):
                print poisson_K[n]
            i == False
            print '\n'
            break
        elif prompt == 'N' or prompt == 'n':
            i == False
            break
        else:
            print("Please Enter (Y|N).")
            i == True
    

    # Re-execute program.
    print("\n=====================================================================")
    again = raw_input("Run print_data.py again? (y/n): ")
    while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
        again = raw_input("Please enter (y/n): ")
    if again == 'Y' or again == 'y':
        print("\n=====================================================================")
        os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Stat_Argument/print_stat_data.py")
    elif again == 'N' or again == 'n':
        print('\nAll process are complete!')
  


if __name__ == '__main__':
	main()