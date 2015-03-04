#!/usr/bin/env python

### This code is for plotting the color diagram for the member clusters. ###

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from pylab import rcParams

def main():
    # Sets default figure parameters.
    rcParams['figure.figsize'] = 14, 7
    
    # Loads isochron data.
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_k.txt')
    
    # Loads mag. data for J, H, & K.
    b_names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_names.txt', 'r').readlines()
    b_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsJ.txt')
    b_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsH.txt')
    b_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsK.txt')
    s_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsK.txt')
    
    b_DelJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelJ.txt')
    b_DelH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelH.txt')
    b_DelK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelK.txt')
    
    # Loads mass data
    data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/mass_data.npz')
    J_mass = data['J_M']
    H_mass = data['H_M']
    K_mass = data['K_M']
    s_K_mass = data['s_K_M']


    # J_mag - K_mag vs. K_mag
    KJ = []
    for i in range(len(b_absK)):
        if b_absJ[i] != 0:
            KJ.append(b_absJ[i] - b_absK[i])
        if b_absJ[i] == 0:
            KJ.append(float('nan'))
    
    # H_mag - K_mag vs. K_mag
    KH = []
    for i in range(len(b_absK)):
        if b_absH[i] != 0:
            KH.append(b_absH[i] - b_absK[i])
        if b_absH[i] == 0:
            KH.append(float('nan'))
    
    sigma_J = b_DelJ[1::2]
    sigma_H = b_DelH[1::2]
    sigma_K = b_DelK[1::2]
    sigma_KJ = (sigma_J**2 + sigma_K**2)**0.5
    sigma_KH = (sigma_H**2 + sigma_K**2)**0.5


    # For Cluster IC 2391
    start = 0
    stop = 13 + 1
    
    plt.subplot(1, 2, 1)
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color='b', label="IC 2391 P")
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 'D', color='b', label="IC 2391 C")
    
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        print i
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color='b', label="IC 2391 P")
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 'D', color='b', label="IC 2391 C")
    
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    
    # For Cluster NGC 6475
    start = 14
    stop = 23 + 1
    
    plt.subplot(1, 2, 1)
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color='g', label='NGC 6474 P')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 'D', color='g', label='NGC 6474 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color='g', label='NGC 6474 P')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 'D', color='g', label='NGC 6474 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    
    # For Cluster NGC 2451
    start = 24
    stop = 49 + 1
    
    plt.subplot(1, 2, 1)
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color = 'r', label='NGC 2451 P')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 'D', color = 'r', label='NGC 2451 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color = 'r', label='NGC 2451 P')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 'D', color = 'r', label='NGC 2451 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    
    # For Cluster NGC 3532
    start = 52
    stop = 67 + 1
    
    plt.subplot(1, 2, 1)
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color = 'c', label='NGC 3532 P')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 'D', color = 'c', label='NGC 3532 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color = 'c', label='NGC 3532 P')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 'D', color = 'c', label='NGC 3532 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    
    # For Cluster IC 2602
    start = 68
    stop = 107 + 1
    
    plt.subplot(1, 2, 1)
    plt.plot(KJ[start:stop:2], b_absK[start:stop:2], 'o', color='m', label='IC 2602 P')
    plt.plot(KJ[start+1:stop:2], b_absK[start+1:stop:2], 'D', color='m', label='IC 2602 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KJ[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelJ[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_j - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(J-K) Mag.", fontsize='16')
    
    plt.subplot(1, 2, 2)
    plt.plot(KH[start:stop:2], b_absK[start:stop:2], 'o', color='m', label='IC 2602 P')
    plt.plot(KH[start+1:stop:2], b_absK[start+1:stop:2], 'D', color='m', label='IC 2602 C')
    
    for i in range(start, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(0.01**2 + 0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    for i in range(start+1, stop, 2):
        plt.errorbar(KH[i], b_absK[i], xerr=(b_DelK[i]**2 + b_DelH[i]**2 + 2*0.01**2)**.5, yerr=0.01, fmt='.', color='k')
    
    plt.plot(m_h - m_k, m_k, color='k')
    plt.gca().invert_yaxis()
    plt.ylabel("K Mag.", fontsize='16')
    plt.xlabel("(H-K) Mag.", fontsize='16')
    
    plt.suptitle("All Clusters", fontsize='22')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    plot = raw_input("\nPlot color comparison for all clusters? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot color comparison for all clusters? (Y|N): ")
            leave = False
    print '\nAll processes are complete!'
    
    


if __name__ == '__main__':
	main()