#!/usr/bin/env python

### This code is for plotting the color diagram for the member clusters. ###

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from pylab import rcParams
import os

def main():
    # Sets default figure parameters.
    rcParams['figure.figsize'] = 14, 7
    
    """
    # Loads isochron data.
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/main/m_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/main/m_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/main/m_k.txt')
    """
    
    # Loads mag. data for J, H, & K.
    b_names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/bin_names.txt', 'r').readlines()
    b_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/bin_AbsJ.txt')
    b_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/bin_AbsH.txt')
    b_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/bin_AbsK.txt')
    
    s_names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/single_names.txt', 'r').readlines()
    s_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/single_AbsJ.txt')
    s_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/single_AbsH.txt')
    s_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/single_AbsK.txt')
    
    b_DelJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/bin_DelJ.txt')
    b_DelH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/bin_DelH.txt')
    b_DelK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/bin_DelK.txt')
    
    # Loads mass data
    data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/mass_data.npz')
    J_mass = data['J_M']
    H_mass = data['H_M']
    K_mass = data['K_M']
    s_K_mass = data['s_K_M']


    # J_mag - K_mag vs. K_mag
    KJ = []
    s_KJ = []
    for i in range(len(b_absK)):
        if b_absJ[i] != 0:
            KJ.append(b_absJ[i] - b_absK[i])
        if b_absJ[i] == 0:
            KJ.append(float('nan'))
    for i in range(len(s_absK)):
        if s_absJ[i] != 0:
            s_KJ.append(s_absJ[i] - s_absK[i])
        if s_absJ[i] == 0:
            s_KJ.append(float('nan'))
    
    # H_mag - K_mag vs. K_mag
    KH = []
    s_KH = []
    for i in range(len(b_absK)):
        if b_absH[i] != 0:
            KH.append(b_absH[i] - b_absK[i])
        if b_absH[i] == 0:
            KH.append(float('nan'))
    for i in range(len(s_absK)):
        if s_absJ[i] != 0:
            s_KH.append(s_absH[i] - s_absK[i])
        if s_absH[i] == 0:
            s_KH.append(float('nan'))
    
    sigma_J = b_DelJ[1::2]
    sigma_H = b_DelH[1::2]
    sigma_K = b_DelK[1::2]
    sigma_KJ = (sigma_J**2 + sigma_K**2)**0.5
    sigma_KH = (sigma_H**2 + sigma_K**2)**0.5
    sigma_s_J = 0.01
    sigma_s_H = 0.01
    sigma_s_K = 0.01


    # For Cluster IC 2391
    cluster = 'IC_2391'
    mass = load_main(cluster)[0]
    m_j = load_main(cluster)[1]
    m_h = load_main(cluster)[2]
    m_k = load_main(cluster)[3]
    
    NG_mass = load_NextGen(cluster)[0]
    NG_m_j = load_NextGen(cluster)[1]
    NG_m_h = load_NextGen(cluster)[2]
    NG_m_k = load_NextGen(cluster)[3]
    
    D_mass = load_Dusty(cluster)[0]
    D_m_j = load_Dusty(cluster)[1]
    D_m_h = load_Dusty(cluster)[2]
    D_m_k = load_Dusty(cluster)[3]
    
    mem_J = load_members(cluster)[0]
    mem_H = load_members(cluster)[1]
    mem_K = load_members(cluster)[2]
    mem_KJ = []
    for i in range(len(mem_K)):
        if mem_J[i] != 0:
            mem_KJ.append(mem_J[i] - mem_K[i])
        if mem_J[i] == 0:
            mem_KJ.append(float('nan'))
    mem_KH = []
    for i in range(len(mem_K)):
        if mem_H[i] != 0:
            mem_KH.append(mem_H[i] - mem_K[i])
        if mem_H[i] == 0:
            mem_KH.append(float('nan'))
    
    start = 0
    stop = 11 + 1
    s_start = 0
    s_stop = 20 + 1
    
    plt.suptitle("Cluster IC 2391", fontsize='22')
    plt.subplot(1, 2, 1)
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KJ[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color='k', label="IC 2391 (P)")
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 's', color='r', label="IC 2391 (C)")
    plt.plot(s_KJ[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="IC 2391 (S)")
    plt.plot(mem_KJ, mem_K, 'x', color='.3', label="IC 2391 (M)")
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.plot(NG_m_j - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_j - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KH[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
        
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color='k', label="IC 2391 (P)")
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 's', color='r', label="IC 2391 (C)")
    plt.plot(s_KH[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="IC 2391 (S)")
    plt.plot(mem_KH, mem_K, 'x', color='.3', label="IC 2391 (M)")

    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.plot(NG_m_h - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_h - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    

    plot = raw_input("\nPlot magnitude comparison IC 2391? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot magnitude comparison for IC 2391? (Y|N): ")
            leave = False
    
    
    # For Cluster NGC 6475
    cluster = 'NGC_6475'
    mass = load_main(cluster)[0]
    m_j = load_main(cluster)[1]
    m_h = load_main(cluster)[2]
    m_k = load_main(cluster)[3]
    
    NG_mass = load_NextGen(cluster)[0]
    NG_m_j = load_NextGen(cluster)[1]
    NG_m_h = load_NextGen(cluster)[2]
    NG_m_k = load_NextGen(cluster)[3]
    
    D_mass = load_Dusty(cluster)[0]
    D_m_j = load_Dusty(cluster)[1]
    D_m_h = load_Dusty(cluster)[2]
    D_m_k = load_Dusty(cluster)[3]
    
    mem_J = load_members(cluster)[0]
    mem_H = load_members(cluster)[1]
    mem_K = load_members(cluster)[2]
    mem_KJ = []
    for i in range(len(mem_K)):
        if mem_J[i] != 0:
            mem_KJ.append(mem_J[i] - mem_K[i])
        if mem_J[i] == 0:
            mem_KJ.append(float('nan'))
    mem_KH = []
    for i in range(len(mem_K)):
        if mem_H[i] != 0:
            mem_KH.append(mem_H[i] - mem_K[i])
        if mem_H[i] == 0:
            mem_KH.append(float('nan'))
    
    start = 12
    stop = 21 + 1
    s_start = 21
    s_stop = 23 + 1
    
    plt.suptitle("Cluster NGC 6475", fontsize='22')
    plt.subplot(1, 2, 1)
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KJ[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
        
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color='k', label='NGC 6474 (P)')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 's', color='r', label='NGC 6474 (C)')
    plt.plot(s_KJ[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 6475 (S)")
    plt.plot(mem_KJ, mem_K, 'x', color='.3', label="NGC 6475 (M)")
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.plot(NG_m_j - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_j - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KH[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
        
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color='k', label='NGC 6474 (P)')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 's', color='r', label='NGC 6474 (C)')
    plt.plot(s_KH[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 6475 (S)")
    plt.plot(mem_KH, mem_K, 'x', color='.3', label="NGC 6475 (M)")
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.plot(NG_m_h - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_h - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    plot = raw_input("\nPlot magnitude comparison NGC 6475? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot magnitude comparison for NGC 6475? (Y|N): ")
            leave = False
    
    
    # For Cluster NGC 2451
    cluster = 'NGC_2451'
    mass = load_main(cluster)[0]
    m_j = load_main(cluster)[1]
    m_h = load_main(cluster)[2]
    m_k = load_main(cluster)[3]
    
    NG_mass = load_NextGen(cluster)[0]
    NG_m_j = load_NextGen(cluster)[1]
    NG_m_h = load_NextGen(cluster)[2]
    NG_m_k = load_NextGen(cluster)[3]
    
    D_mass = load_Dusty(cluster)[0]
    D_m_j = load_Dusty(cluster)[1]
    D_m_h = load_Dusty(cluster)[2]
    D_m_k = load_Dusty(cluster)[3]
    
    mem_J = load_members(cluster)[0]
    mem_H = load_members(cluster)[1]
    mem_K = load_members(cluster)[2]
    mem_KJ = []
    for i in range(len(mem_K)):
        if mem_J[i] != 0:
            mem_KJ.append(mem_J[i] - mem_K[i])
        if mem_J[i] == 0:
            mem_KJ.append(float('nan'))
    mem_KH = []
    for i in range(len(mem_K)):
        if mem_H[i] != 0:
            mem_KH.append(mem_H[i] - mem_K[i])
        if mem_H[i] == 0:
            mem_KH.append(float('nan'))
    
    start = 22
    stop = 47 + 1
    s_start = 24
    s_stop = 51 + 1
    
    plt.suptitle("Cluster NGC 2451", fontsize='22')
    plt.subplot(1, 2, 1)
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KJ[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color = 'k', label='NGC 2451 (P)')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 's', color = 'r', label='NGC 2451 (C)')
    plt.plot(s_KJ[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 2451 (S)")
    plt.plot(mem_KJ, mem_K, 'x', color='.3', label="NGC 2451 (M)")
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.plot(NG_m_j - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_j - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KH[i], s_absH[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color = 'k', label='NGC 2451 (P)')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 's', color = 'r', label='NGC 2451 (C)')
    plt.plot(s_KH[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 2451 (S)")
    plt.plot(mem_KH, mem_K, 'x', color='.3', label="NGC 2451 (M)")
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.plot(NG_m_h - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_h - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    plot = raw_input("\nPlot magnitude comparison NGC 2451? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot magnitude comparison for NGC 2451? (Y|N): ")
            leave = False



    # For Cluster NGC 2516
    cluster = 'NGC_2516'
    mass = load_main(cluster)[0]
    m_j = load_main(cluster)[1]
    m_h = load_main(cluster)[2]
    m_k = load_main(cluster)[3]
    
    NG_mass = load_NextGen(cluster)[0]
    NG_m_j = load_NextGen(cluster)[1]
    NG_m_h = load_NextGen(cluster)[2]
    NG_m_k = load_NextGen(cluster)[3]
    
    D_mass = load_Dusty(cluster)[0]
    D_m_j = load_Dusty(cluster)[1]
    D_m_h = load_Dusty(cluster)[2]
    D_m_k = load_Dusty(cluster)[3]
    
    mem_J = load_members(cluster)[0]
    mem_H = load_members(cluster)[1]
    mem_K = load_members(cluster)[2]
    mem_KJ = []
    for i in range(len(mem_K)):
        if mem_J[i] != 0:
            mem_KJ.append(mem_J[i] - mem_K[i])
        if mem_J[i] == 0:
            mem_KJ.append(float('nan'))
    mem_KH = []
    for i in range(len(mem_K)):
        if mem_H[i] != 0:
            mem_KH.append(mem_H[i] - mem_K[i])
        if mem_H[i] == 0:
            mem_KH.append(float('nan'))

    start = 0
    stop = 0
    s_start = 52
    s_stop = 75 + 1
    
    plt.suptitle("Cluster NGC 2516", fontsize='22')
    plt.subplot(1, 2, 1)
    #for i in range(start, stop, 2):
    #    plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    #for i in range(start+1, stop, 2):
    #    plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KJ[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    #plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color = 'r', label='NGC 2451 (P)')
    #plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 's', color = 'r', label='NGC 2451 (C)')
    plt.plot(s_KJ[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 2516 (S)")
    plt.plot(mem_KJ, mem_K, 'x', color='.3', label="NGC 2516 (M)")
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.plot(NG_m_j - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_j - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    #for i in range(start, stop, 2):
    #    plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    #for i in range(start+1, stop, 2):
    #    plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
       plt.errorbar(s_KH[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    #plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color = 'r', label='NGC 2451 (P)')
    #plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 's', color = 'r', label='NGC 2451 (C)')
    plt.plot(s_KH[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 2451 (S)")
    plt.plot(mem_KH, mem_K, 'x', color='.3', label="NGC 2516 (M)")
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.plot(NG_m_h - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_h - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    plot = raw_input("\nPlot magnitude comparison NGC 2516? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot magnitude comparison for NGC 2516? (Y|N): ")
            leave = False
            


    # For Cluster NGC 3532
    cluster = 'NGC_3532'
    mass = load_main(cluster)[0]
    m_j = load_main(cluster)[1]
    m_h = load_main(cluster)[2]
    m_k = load_main(cluster)[3]
    
    NG_mass = load_NextGen(cluster)[0]
    NG_m_j = load_NextGen(cluster)[1]
    NG_m_h = load_NextGen(cluster)[2]
    NG_m_k = load_NextGen(cluster)[3]
    
    D_mass = load_Dusty(cluster)[0]
    D_m_j = load_Dusty(cluster)[1]
    D_m_h = load_Dusty(cluster)[2]
    D_m_k = load_Dusty(cluster)[3]
    
    mem_J = load_members(cluster)[0]
    mem_H = load_members(cluster)[1]
    mem_K = load_members(cluster)[2]
    mem_KJ = []
    for i in range(len(mem_K)):
        if mem_J[i] != 0:
            mem_KJ.append(mem_J[i] - mem_K[i])
        if mem_J[i] == 0:
            mem_KJ.append(float('nan'))
    mem_KH = []
    for i in range(len(mem_K)):
        if mem_H[i] != 0:
            mem_KH.append(mem_H[i] - mem_K[i])
        if mem_H[i] == 0:
            mem_KH.append(float('nan'))
    
    start = 48
    stop = 65 + 1
    s_start = 76
    s_stop = 90 + 1
    
    plt.suptitle("Cluster NGC 3532", fontsize='22')
    plt.subplot(1, 2, 1)
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KJ[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color = 'k', label='NGC 3532 (P)')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 's', color = 'r', label='NGC 3532 (C)')
    plt.plot(s_KJ[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 3532 (S)")
    plt.plot(mem_KJ, mem_K, 'x', color='.3', label="NGC 3532 (M)")
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.plot(NG_m_j - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_j - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KH[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
        
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color = 'k', label='NGC 3532 (P)')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 's', color = 'r', label='NGC 3532 (C)')
    plt.plot(s_KH[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label="NGC 3532 (S)")
    plt.plot(mem_KH, mem_K, 'x', color='.3', label="NGC 3532 (M)")
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.plot(NG_m_h - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_h - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    plot = raw_input("\nPlot magnitude comparison NGC 3532? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot magnitude comparison for NGC 3532? (Y|N): ")
            leave = False
    
    # For Cluster IC 2602
    cluster = 'IC_2602'
    mass = load_main(cluster)[0]
    m_j = load_main(cluster)[1]
    m_h = load_main(cluster)[2]
    m_k = load_main(cluster)[3]
    
    NG_mass = load_NextGen(cluster)[0]
    NG_m_j = load_NextGen(cluster)[1]
    NG_m_h = load_NextGen(cluster)[2]
    NG_m_k = load_NextGen(cluster)[3]
    
    D_mass = load_Dusty(cluster)[0]
    D_m_j = load_Dusty(cluster)[1]
    D_m_h = load_Dusty(cluster)[2]
    D_m_k = load_Dusty(cluster)[3]
    
    mem_J = load_members(cluster)[0]
    mem_H = load_members(cluster)[1]
    mem_K = load_members(cluster)[2]
    mem_KJ = []
    for i in range(len(mem_K)):
        if mem_J[i] != 0:
            mem_KJ.append(mem_J[i] - mem_K[i])
        if mem_J[i] == 0:
            mem_KJ.append(float('nan'))
    mem_KH = []
    for i in range(len(mem_K)):
        if mem_H[i] != 0:
            mem_KH.append(mem_H[i] - mem_K[i])
        if mem_H[i] == 0:
            mem_KH.append(float('nan'))
    
    start = 66
    stop = 105 + 1
    s_start = 91
    s_stop = 113 + 1
    
    plt.suptitle("Cluster IC 2602", fontsize='22')
    plt.subplot(1, 2, 1)
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KJ[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color='k', label='IC 2602 (P)')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 's', color='r', label='IC 2602 (C)')
    plt.plot(s_KJ[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label='IC 2602 (S)')
    plt.plot(mem_KJ, mem_K, 'x', color='.3', label="IC 2602 (M)")
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.plot(NG_m_j - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_j - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(s_start, s_stop):
        plt.errorbar(s_KH[i], s_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
        
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color='k', label='IC 2602 (P)')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 's', color='r', label='IC 2602 (C)')
    plt.plot(s_KH[s_start:s_stop], s_absK[s_start:s_stop], 'o', color='1.0', label='IC 2602 (S)')
    plt.plot(mem_KH, mem_K, 'x', color='.3', label="IC 2602 (M)")
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.plot(NG_m_h - NG_m_k, NG_m_k, color='r')
    plt.plot(D_m_h - D_m_k, D_m_k, color='g')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    plot = raw_input("\nPlot magnitude comparison IC 2602? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot magnitude comparison for IC 2602? (Y|N): ")
            leave = False
    
    
    # Re-execute program.
    print("\n=====================================================================")
    again = raw_input("Run plot_data.py again? (y/n): ")
    while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
        again = raw_input("Please enter (y/n): ")
    if again == 'Y' or again == 'y':
        print("\n=====================================================================")
        os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/plot_data.py")
    elif again == 'N' or again == 'n':
        print('\nAll process are complete!')
    


def load_main(cluster):
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/mass.txt')
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/M_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/M_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/M_k.txt')
    
    return mass, m_j, m_h, m_k


def load_NextGen(cluster):
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/mass.txt')
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/M_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/M_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/M_k.txt')
    
    return mass, m_j, m_h, m_k


def load_Dusty(cluster):
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/mass.txt')
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/M_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/M_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/M_k.txt')
    
    return mass, m_j, m_h, m_k


def load_members(cluster):
    absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/members/'+str(cluster)+'/absJ.txt')
    absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/members/'+str(cluster)+'/absH.txt')
    absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/Abs_Data/members/'+str(cluster)+'/absK.txt')
    
    return absJ, absH, absK


def load_stat(cluster):
    actual_area = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/actual_area.txt')
    magnitude = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/actual_mag.txt')
    J_count = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/J_count.txt')
    H_count = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/H_count.txt')
    K_count = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/K_count.txt')

    return actual_area, magnitude, J_count, H_count, K_count


if __name__ == '__main__':
	main()