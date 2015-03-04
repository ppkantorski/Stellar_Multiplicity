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
            print cluster
            i == False
            break
        if prompt == 'NGC_6475' or prompt == '2':
            cluster = 'NGC_6475'
            print cluster
            i == False
            break
        if prompt == 'NGC_2451' or prompt == '3':
            cluster = 'NGC_2451'
            print cluster
            i == False
            break
        if prompt == 'NGC_2516' or prompt == '4':
            cluster = 'NGC_2516'
            print cluster
            i == False
            break
        if prompt == 'NGC_3532' or prompt == '5':
            cluster = 'NGC_3532'
            print cluster
            i == False
            break
        if prompt == 'IC_2602' or prompt == '6':
            cluster = 'IC_2602'
            print cluster
            i == False
            break
        else:
            i == True
            
    
    # Loads mass data
    data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/'+cluster+'_mass_data.npz')

    J_mass = data['J_M']
    H_mass = data['H_M']
    K_mass = data['K_M']
    s_J_mass = data['s_J_M']
    s_H_mass = data['s_H_M'] 
    s_K_mass = data['s_K_M'] 
    NG_J_mass = data['NG_J_M']
    NG_H_mass = data['NG_H_M']
    NG_K_mass = data['NG_K_M']
    NG_s_J_mass = data['NG_s_J_M']
    NG_s_H_mass = data['NG_s_H_M'] 
    NG_s_K_mass = data['NG_s_K_M']
    D_J_mass = data['D_J_M']
    D_H_mass = data['D_H_M']
    D_K_mass = data['D_K_M']
    D_s_J_mass = data['D_s_J_M']
    D_s_H_mass = data['D_s_H_M'] 
    D_s_K_mass = data['D_s_K_M']

    
    print "\nFrom Main Isochrone..."
    i = True
    while i == True:
        prompt = raw_input("J, H, K, or single? : ")
        if prompt == 'J' or prompt == 'j':
            for n in range(len(J_mass)):
                print J_mass[n]
            i == False
            break
        elif prompt == 'H' or prompt == 'h':
            for n in range(len(H_mass)):
                print H_mass[n]
            i == False
            break
        elif prompt == 'K' or prompt == 'k':
            for n in range(len(K_mass)):
                print K_mass[n]
            i == False
            break
        elif prompt == "s_J" or prompt == "s_j":
            for n in range(len(s_J_mass)):
                print s_J_mass[n]
            i == False
            break
        elif prompt == "s_H" or prompt == "s_h":        
            for n in range(len(s_H_mass)):        
                print s_H_mass[n]
            i == False
            break
        elif prompt == "s_K" or prompt == "s_k":
            for n in range(len(s_K_mass)):
                print s_K_mass[n]
            i == False
            break
        elif not prompt:
            i == False
            break
        else:
            print("Please Enter J, H, K, or single.")
            i == True
    
    print "\nFrom NG Isochrone..."
    i = True
    while i == True:
        prompt = raw_input("J, H, K, or single? : ")
        if prompt == 'J' or prompt == 'j':
            for n in range(len(NG_J_mass)):
                print NG_J_mass[n]
            i == False
            break
        elif prompt == 'H' or prompt == 'h':
            for n in range(len(NG_H_mass)):
                print NG_H_mass[n]
            i == False
            break
        elif prompt == 'K' or prompt == 'k':
            for n in range(len(NG_K_mass)):
                print NG_K_mass[n]
            i == False
            break
        elif prompt == "s_J" or prompt == "s_j":
            for n in range(len(NG_s_J_mass)):
                print NG_s_J_mass[n]
            i == False
            break
        elif prompt == "s_H" or prompt == "s_h":        
            for n in range(len(NG_s_H_mass)):        
                print NG_s_H_mass[n]
            i == False
            break
        elif prompt == "s_K" or prompt == "s_k":
            for n in range(len(NG_s_K_mass)):
                print NG_s_K_mass[n]
            i == False
            break
        elif prompt == '\n' or prompt == '\n':
            i == False
            break
        elif not prompt:
            i == False
            break
        else:
            print("Please Enter J, H, K, or single.")
            i == True
            
    
    print "\nFrom Dusty Isochrone..."
    i = True
    while i == True:
        prompt = raw_input("J, H, K, or single? : ")
        if prompt == 'J' or prompt == 'j':
            for n in range(len(D_J_mass)):
                print D_J_mass[n]
            i == False
            break
        elif prompt == 'H' or prompt == 'h':
            for n in range(len(D_H_mass)):
                print D_H_mass[n]
            i == False
            break
        elif prompt == 'K' or prompt == 'k':
            for n in range(len(D_K_mass)):
                print D_K_mass[n]
            i == False
            break
        elif prompt == "s_J" or prompt == "s_j":
            for n in range(len(D_s_J_mass)):
                print D_s_J_mass[n]
            i == False
            break
        elif prompt == "s_H" or prompt == "s_h":        
            for n in range(len(D_s_H_mass)):        
                print D_s_H_mass[n]
            i == False
            break
        elif prompt == "s_K" or prompt == "s_k":
            for n in range(len(D_s_K_mass)):
                print D_s_K_mass[n]
            i == False
            break
        elif prompt == '\n' or prompt == '\n':
            i == False
            break
        elif not prompt:
            i == False
            break
        else:
            print("Please Enter J, H, K, or single.")
            i == True        
    

    # Re-execute program.
    print("\n=====================================================================")
    again = raw_input("Run print_data.py again? (y/n): ")
    while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
        again = raw_input("Please enter (y/n): ")
    if again == 'Y' or again == 'y':
        print("\n=====================================================================")
        os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/print_data.py")
    elif again == 'N' or again == 'n':
        print('\nAll process are complete!')
   


if __name__ == '__main__':
	main()