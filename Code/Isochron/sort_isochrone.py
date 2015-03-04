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
            #J_cross = 6.00
            #_cross = 5.17
            #K_cross = 5.50
            start = 0
            stop = 13 + 1
            print stop
            s_start = 0
            s_stop = 19 + 1
            i == False
            break
        if prompt == 'NGC_6475' or prompt == '2':
            cluster = 'NGC_6475'
            print cluster
            #J_cross = 6.50
            #H_cross = 5.50
            #K_cross = 5.60
            start = 14
            stop = 23 + 1
            s_start = 20
            s_stop = 22 + 1
            i == False
            break
        if prompt == 'NGC_2451' or prompt == '3':
            cluster = 'NGC_2451'
            print cluster
            #J_cross = 6.00
            #H_cross = 5.15
            #K_cross = 5.25
            start = 24
            stop = 49 + 1
            s_start = 23
            s_stop = 50 + 1
            i == False
            break
        if prompt == 'NGC_2516' or prompt == '4':
            cluster = 'NGC_2516'
            print cluster
            #J_cross = 6.50
            #H_cross = 5.50
            #K_cross = 5.60
            start = 0
            stop = 0
            s_start = 51
            s_stop = 74 + 1
            i == False
            break
        if prompt == 'NGC_3532' or prompt == '5':
            cluster = 'NGC_3532'
            print cluster
            #J_cross = 6.40
            #H_cross = 5.50
            #K_cross = 5.50
            start = 52
            stop = 67 + 1
            s_start = 75
            s_stop = 91 + 1
            i == False
            break
        if prompt == 'IC_2602' or prompt == '6':
            cluster = 'IC_2602'
            print cluster
            #J_cross = 6.00
            #H_cross = 5.00
            #K_cross = 5.10
            start = 68
            stop = 107 + 1
            s_start = 92
            s_stop = 114 + 1
            i == False
            break
        else:
            i == True
    
    
    M_cutoff = 0.5
    
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
    
    b_names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_names.txt', 'r').readlines()
    b_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsJ.txt')
    b_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsH.txt')
    b_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsK.txt')
    
    s_names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_names.txt', 'r').readlines()
    s_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsJ.txt')
    s_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsH.txt')
    s_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsK.txt')
    
    b_DelJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelJ.txt')
    b_DelH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelH.txt')
    b_DelK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelK.txt')
    
    
    b_J = []; b_H = []; b_K = []
    s_J = []; s_H = []; s_K = []
    for i in range(start, stop):
        b_J.append(b_absJ[i])
        b_H.append(b_absH[i])
        b_K.append(b_absK[i])
    for i in range(s_start, s_stop):
        s_J.append(s_absJ[i])
        s_H.append(s_absH[i])
        s_K.append(s_absK[i])
    
    print "b_J length:", len(b_J)
    print "J_mass length:", len(J_mass)
    print "b_H length:", len(b_H)
    print "H_mass length:", len(H_mass)
    print "b_K length:", len(b_K)
    print "K_mass length:", len(K_mass)
    
    
    fix_J_mass = []; fix_H_mass = []; fix_K_mass = []
    for i in range(len(J_mass)):
        if J_mass[i] <= M_cutoff:
            fix_J_mass.append(NG_J_mass[i])
        if J_mass[i] > M_cutoff:
            fix_J_mass.append(J_mass[i])
        if H_mass[i] <= M_cutoff:
            fix_H_mass.append(NG_H_mass[i])
        if H_mass[i] > M_cutoff:
            fix_H_mass.append(H_mass[i])
        if K_mass[i] <= M_cutoff:
            fix_K_mass.append(NG_K_mass[i])
        if K_mass[i] > M_cutoff:
            fix_K_mass.append(K_mass[i])
    fix_s_J_mass = []; fix_s_H_mass =[]; fix_s_K_mass = []
    for i in range(len(s_J_mass)):
        if s_J_mass[i] <= M_cutoff:
            fix_s_J_mass.append(NG_s_J_mass[i])
        if s_J_mass[i] > M_cutoff:
            fix_s_J_mass.append(s_J_mass[i])
        if s_H_mass[i] <= M_cutoff:
            fix_s_H_mass.append(NG_s_H_mass[i])
        if s_H_mass[i] > M_cutoff:
            fix_s_H_mass.append(s_H_mass[i])
        if s_K_mass[i] <= M_cutoff:
            fix_s_K_mass.append(NG_s_K_mass[i])
        if s_K_mass[i] > M_cutoff:
            fix_s_K_mass.append(s_K_mass[i])
    
    print "Saving sorted mass data..."
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Masses/'+cluster+'_fixed_mass',
    J_M= fix_J_mass, H_M= fix_H_mass, K_M= fix_K_mass, s_J_M= fix_s_J_mass, s_H_M= fix_s_H_mass, s_K_M= fix_s_K_mass,
    b_J= b_J, b_H= b_H, b_K= b_K, s_J= s_J, s_H= s_H, s_K= s_K)
    print "Save complete!"
    
    i = True
    while i == True:
        prompt = raw_input("Print binary star J, H, and K masses? (Y|N): ")
        if prompt == 'Y' or prompt == 'y':
            print '\nJ-mass:'
            for n in range(len(fix_J_mass)):
                print fix_J_mass[n]
            print '\nH-mass:'
            for n in range(len(fix_H_mass)):
                print fix_H_mass[n]
            print '\nK-mass:'
            for n in range(len(fix_K_mass)):
                print fix_K_mass[n]
            i == False
            print '\n'
            break
        elif prompt == 'N' or prompt == 'n':
            i == False
            break
        else:
            print("Please Enter (Y|N).")
            i == True
    i = True
    while i == True:
        prompt = raw_input("Print single star J, H, and K masses? (Y|N): ")
        if prompt == 'Y' or prompt == 'y':
            print '\nJ-mass:'
            for n in range(len(fix_s_J_mass)):
                print fix_s_J_mass[n]
            print '\nH-mass:'
            for n in range(len(fix_s_H_mass)):
                print fix_s_H_mass[n]
            print '\nK-mass:'
            for n in range(len(fix_s_K_mass)):
                print fix_s_K_mass[n]
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
    again = raw_input("Run sort_isochrone.py again? (y/n): ")
    while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
        again = raw_input("Please enter (y/n): ")
    if again == 'Y' or again == 'y':
        print("\n=====================================================================")
        os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/sort_isochrone.py")
    elif again == 'N' or again == 'n':
        print('\nAll process are complete!')
  


if __name__ == '__main__':
	main()