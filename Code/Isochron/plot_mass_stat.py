#!/usr/bin/env python

# This program is the main program for returning cluster specific mass values.
# This is to be ran before running 'sort_isochrone.py'

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from pylab import rcParams
import os


def main():
    # Loading Isochron Data & Binary/Single Magnitude Data.
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/mass.txt')
    Teff = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/temperature.txt')
    age = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/age.txt')
    luminosity = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/luminosity.txt')
    
    """
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_k.txt')
    """
    
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
    
    M_cutoff = 0.5
    
    stay = True
    while stay == True:
        prompt = str(raw_input("Enter Cluster Name: "))
        if prompt == 'IC_2391' or prompt == '1':
            # For Cluster IC 2391
            cluster = 'IC_2391'
            print "\nCluster Name:", cluster
            #J_cross = 6.00
            #H_cross = 5.17
            #K_cross = 5.50
            start = 0
            stop = 13 + 1
            s_start = 0
            s_stop = 19 + 1
            stay = False
            break
        if prompt == 'NGC_6475' or prompt == '2':
            # For Cluster NGC 6475
            cluster = 'NGC_6475'
            print "\nCluster Name:", cluster
            #J_cross = 6.50
            #H_cross = 5.50
            #K_cross = 5.60
            start = 14
            stop = 23 + 1
            s_start = 20
            s_stop = 22 + 1
            stay = False
            break
        if prompt == 'NGC_2451' or prompt == '3':
            # For Cluster NGC 2451
            cluster = 'NGC_2451'
            print "\nCluster Name:", cluster
            #J_cross = 6.00
            #H_cross = 5.15
            #K_cross = 5.25
            start = 24
            stop = 49 + 1
            s_start = 23
            s_stop = 50 + 1
            stay = False
            break
        if prompt == 'NGC_2516' or prompt == '4':
            # For Cluster NGC 2516
            cluster = 'NGC_2516'
            print "\nCluster Name:", cluster
            #J_cross = 6.50
            #H_cross = 5.50
            #K_cross = 5.60
            start = 0
            stop = 0
            s_start = 51
            s_stop = 74 + 1
            stay = False
            break        
        if prompt == 'NGC_3532' or prompt == '5':
            # For Cluster NGC 3532
            cluster = 'NGC_3532'
            print "\nCluster Name:", cluster
            #J_cross = 6.40
            #H_cross = 5.50
            #K_cross = 5.50
            start = 50
            stop = 67 + 1
            s_start = 75
            s_stop = 89 + 1
            stay = False
            break
        if prompt == 'IC_2602' or prompt == '6':
            # For Cluster IC 2602
            cluster = 'IC_2602'
            print "\nCluster Name:", cluster
            #J_cross = 6.00
            #H_cross = 5.00
            #K_cross = 5.10
            start = 68
            stop = 107 + 1
            s_start = 90
            s_stop = 112 #+ 1
            stay = False
            break
        else:
            stay = True

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
    
    '''
    # Loading fixed mass data values for specified cluster...
    mass_data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Masses/'+cluster+'_fixed_mass.npz')
    J_M_final = mass_data['J_M']
    H_M_final = mass_data['H_M']
    K_M_final = mass_data['K_M']
    s_J_M_final = mass_data['s_J_M']
    s_H_M_final = mass_data['s_H_M']
    s_K_M_final = mass_data['s_K_M']
    b_J_final = mass_data['b_J']
    b_H_final = mass_data['b_H']
    b_K_final = mass_data['b_K']
    s_J_final = mass_data['s_J']
    s_H_final = mass_data['s_H']
    s_K_final = mass_data['s_K']
    '''
    
    print '\n'
    stay_1 = True
    while stay_1 == True:
        prompt = raw_input('Apply upper/lower error prop.? (y|n): ')
        if prompt == 'Y' or prompt == 'y':
            stay = True
            stay_1 = False
        elif prompt == 'N' or prompt == 'n':
            stay = False
            stay_1 = False
        else:
            stay_1 = True

    while stay == True:
        # Code for applying the upper and lower error propogation.
        blanket = 0.01 * 3  # Should be 0.01 (happens to be the same for both).
        stay_1 = True
        while stay_1 == True:
            choice = str(raw_input('Upper or Lower Error Prop.? (1|2): '))
            if choice == "1":
                sign = -1
                stay_1 = False
            elif choice == "2":
                sign = 1
                stay_1 = False
            else:
                stay_1 = True
            
        b_J = []
        for n in range(len(b_absJ)):
            odd = 2*n
            even = 2*n + 1
            if odd > len(b_absJ)-1:
                break
            if even > len(b_absJ)-1:
                break
            b_J.append(b_absJ[odd]+ sign*blanket) #Primary Stars
            b_J.append(b_absJ[even] + sign*(blanket**2 + b_DelJ[even]**2)**(0.5) ) #Companion Stars
            #b_J.append(b_absJ[even] + sign* 3*(blanket**2 + b_DelJ[even]**2)**(0.5) )
        b_absJ = b_J
        
        b_H = []
        for n in range(len(b_absH)):
            odd = 2*n
            even = 2*n + 1
            if odd > len(b_absH)-1:
                break
            if even > len(b_absH)-1:
                break
            b_H.append(b_absH[odd]+ sign*blanket) #Primary Stars
            b_H.append(b_absH[even] + sign*(blanket**2 + b_DelH[even]**2)**(0.5) ) #Companion Stars
            #b_H.append(b_absJ[even] + sign* 3*(blanket**2 + b_DelH[even]**2)**(0.5) )
        b_absH = b_H
        
        b_K = []
        for n in range(len(b_absK)):
            odd = 2*n
            even = 2*n + 1
            if odd > len(b_absK)-1:
                break
            if even > len(b_absK)-1:
                break
            b_K.append(b_absK[odd]+ sign*blanket) #Primary Stars
            b_K.append(b_absK[even] + sign*(blanket**2 + b_DelK[even]**2)**(0.5) ) #Companion Stars
            #b_K.append(b_absJ[even] + sign* 3*(blanket**2 + b_DelK[even]**2)**(0.5) )
        b_absK = b_K
        
        s_absJ = s_absJ + sign*blanket
        s_absH = s_absH + sign*blanket
        s_absK = s_absK + sign*blanket
        
        stay = False
    
    
    ### Code for  Mass vs Mag J, H, & K. ###
    # Mass vs MagJ
    x = mass
    y = m_j
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_j_array = [xnew, ynew]
    
    x = NG_mass
    y = NG_m_j
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(NG_mass[0], NG_mass[len(NG_mass)-1], 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    NG_m_j_array = [xnew, ynew]
    
    x = D_mass
    y = D_m_j
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(D_mass[0], D_mass[len(D_mass)-1], 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    D_m_j_array = [xnew, ynew]
            
    # Mass vs MagH
    x = mass
    y = m_h
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_h_array = [xnew, ynew]
    
    x = NG_mass
    y = NG_m_h
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(NG_mass[0], NG_mass[len(NG_mass)-1], 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    NG_m_h_array = [xnew, ynew]
    
    x = D_mass
    y = D_m_h
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(D_mass[0], D_mass[len(D_mass)-1], 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    D_m_h_array = [xnew, ynew]
    
    # Mass vs MagK
    x = mass
    y = m_k
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_k_array = [xnew, ynew]
    
    x = NG_mass
    y = NG_m_k
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(NG_mass[0], NG_mass[len(NG_mass)-1], 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    NG_m_k_array = [xnew, ynew]
    
    x = D_mass
    y = D_m_k
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(D_mass[0], D_mass[len(D_mass)-1], 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    D_m_k_array = [xnew, ynew]
    #######################################
    

    # The following is code to find the corresponding mass values from Mag J, H, & K.
    J_mass = []
    NG_J_mass = []
    D_J_mass = []
    for i in range(0, len(b_absJ)):
        index = find_nearest(m_j_array[1:][0], b_absJ[i])[0]
        J_mass.append(m_j_array[0:][0][index])
        NG_index = find_nearest(NG_m_j_array[1:][0], b_absJ[i])[0]
        NG_J_mass.append(NG_m_j_array[0:][0][NG_index])
        D_index = find_nearest(D_m_j_array[1:][0], b_absJ[i])[0]
        D_J_mass.append(D_m_j_array[0:][0][D_index])
    H_mass = []
    NG_H_mass = []
    D_H_mass = []
    for i in range(0, len(b_absH)):
        index = find_nearest(m_h_array[1:][0], b_absH[i])[0]
        H_mass.append(m_h_array[0:][0][index])
        NG_index = find_nearest(NG_m_h_array[1:][0], b_absH[i])[0]
        NG_H_mass.append(NG_m_h_array[0:][0][NG_index])
        D_index = find_nearest(D_m_h_array[1:][0], b_absH[i])[0]
        D_H_mass.append(D_m_h_array[0:][0][D_index])
    K_mass = []
    NG_K_mass = []
    D_K_mass = []
    for i in range(0, len(b_absK)):
        index = find_nearest(m_k_array[1:][0], b_absK[i])[0]
        K_mass.append(m_k_array[0:][0][index])
        NG_index = find_nearest(NG_m_k_array[1:][0], b_absK[i])[0]
        NG_K_mass.append(NG_m_k_array[0:][0][NG_index])
        D_index = find_nearest(D_m_k_array[1:][0], b_absK[i])[0]
        D_K_mass.append(D_m_k_array[0:][0][D_index])
    s_J_mass = []
    NG_s_J_mass = []
    D_s_J_mass = []
    for i in range(0, len(s_absJ)):
        index = find_nearest(m_j_array[1:][0], s_absJ[i])[0]
        s_J_mass.append(m_j_array[0:][0][index])
        NG_index = find_nearest(NG_m_j_array[1:][0], s_absJ[i])[0]
        NG_s_J_mass.append(NG_m_j_array[0:][0][NG_index])
        D_index = find_nearest(D_m_j_array[1:][0], s_absJ[i])[0]
        D_s_J_mass.append(D_m_j_array[0:][0][D_index])
    s_H_mass = []
    NG_s_H_mass = []
    D_s_H_mass = []
    for i in range(0, len(s_absH)):
        index = find_nearest(m_h_array[1:][0], s_absH[i])[0]
        s_H_mass.append(m_h_array[0:][0][index])
        NG_index = find_nearest(NG_m_h_array[1:][0], s_absH[i])[0]
        NG_s_H_mass.append(NG_m_h_array[0:][0][NG_index])
        D_index = find_nearest(D_m_h_array[1:][0], s_absH[i])[0]
        D_s_H_mass.append(D_m_h_array[0:][0][D_index])
    s_K_mass = []
    NG_s_K_mass = []
    D_s_K_mass = []
    for i in range(0, len(s_absK)):
        index = find_nearest(m_k_array[1:][0], s_absK[i])[0]
        s_K_mass.append(m_k_array[0:][0][index])
        NG_index = find_nearest(NG_m_k_array[1:][0], s_absK[i])[0]
        NG_s_K_mass.append(NG_m_k_array[0:][0][NG_index])
        D_index = find_nearest(D_m_k_array[1:][0], s_absK[i])[0]
        D_s_K_mass.append(D_m_k_array[0:][0][D_index])
        #print index, m_k_array[0:][0][index]
    
    
    '''
    ###
    # J-band for all three Isochrones.
    rcParams['figure.figsize'] = 21, 7
    plt.suptitle(cluster+" Mass vs App Mag.", fontsize='22')
    plt.subplot(1, 3, 1)
    plt.plot(m_j_array[0:][0], m_j_array[0:][1], color='b')
    plt.plot(NG_m_j_array[0:][0], NG_m_j_array[0:][1], color='r')
    plt.plot(D_m_j_array[0:][0], D_m_j_array[0:][1], color='g')
    plt.plot(J_M_final, b_J_final, '.', color='k')
    plt.plot(s_J_M_final, s_J_final, '.', color='k')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
    plt.axvline(M_cutoff, color='k', linestyle=':')
    
    # H-band for binaries Dusty Isochrone.
    plt.subplot(1, 3, 2)
    plt.plot(m_h_array[0:][0], m_h_array[0:][1], color='b')
    plt.plot(NG_m_h_array[0:][0], NG_m_h_array[0:][1], color='r')
    plt.plot(D_m_h_array[0:][0], D_m_h_array[0:][1], color='g')
    plt.plot(H_M_final, b_H_final, '.', color='k')
    plt.plot(s_H_M_final, s_H_final, '.', color='k')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')
    plt.axvline(M_cutoff, color='k', linestyle=':')
    
    # K-band for binaries Dusty Isochrone.
    plt.subplot(1, 3, 3)
    plt.plot(m_k_array[0:][0], m_k_array[0:][1], color='b')
    plt.plot(NG_m_k_array[0:][0], NG_m_k_array[0:][1], color='r')
    plt.plot(D_m_k_array[0:][0], D_m_k_array[0:][1], color='g')
    plt.plot(K_M_final, b_K_final, '.', color='k')
    plt.plot(s_K_M_final, s_K_final, '.', color='k')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    plt.axvline(M_cutoff, color='k', linestyle=':')
    
    plot = raw_input("\nPlot Interpolations for all three isochrones? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            #plt.tight_layout()
            plt.show()
            leave = True
            #print '\n'
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
            #print '\n'
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot Interpolations for all three isochrones? (Y|N): ")
            leave = False
    '''      
    
    # J-band for binaries and singles.
    rcParams['figure.figsize'] = 21, 7
    plt.suptitle(cluster+" Mass vs App Mag.", fontsize='22')
    plt.subplot(1, 3, 1)
    plt.plot(J_mass[start:stop], b_absJ[start:stop], 'o', color='g')
    plt.plot(s_J_mass[s_start:s_stop], s_absJ[s_start:s_stop], '.', color='k')
    plt.plot(m_j_array[0:][0], m_j_array[0:][1], color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
    
    # H-band for binaries
    plt.subplot(1, 3, 2)
    plt.plot(H_mass[start:stop], b_absH[start:stop], 'o', color='g')
    plt.plot(s_H_mass[s_start:s_stop], s_absH[s_start:s_stop], '.', color='k')
    plt.plot(m_h_array[0:][0], m_h_array[0:][1], color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')
    
    # K-band for binaries
    plt.subplot(1, 3, 3)
    plt.plot(K_mass[start:stop], b_absK[start:stop], 'o', color='g')
    plt.plot(s_K_mass[s_start:s_stop], s_absK[s_start:s_stop], '.', color='k')
    plt.plot(m_k_array[0:][0], m_k_array[0:][1], color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    
    
    plot = raw_input("\nPlot Interpolations with magnitude values for main isochrone? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            #plt.tight_layout()
            plt.show()
            leave = True
            #print '\n'
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
            #print '\n'
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot Interpolations with magnitude values? (Y|N): ")
            leave = False
    
    
    # J-band for binaries NextGen Isochrone.
    rcParams['figure.figsize'] = 21, 7
    #plt.suptitle(cluster+" Mass vs App Mag. (NextGen)", fontsize='22')
    plt.subplot(1, 3, 1)
    plt.plot(NG_J_mass[start:stop], b_absJ[start:stop], 'o', color='g')
    plt.plot(NG_s_J_mass[s_start:s_stop], s_absH[s_start:s_stop], '.', color='k')
    plt.plot(NG_m_j_array[0:][0], NG_m_j_array[0:][1], color='r')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
    
    # H-band for binaries NextGen Isochrone.
    plt.subplot(1, 3, 2)
    plt.plot(NG_H_mass[start:stop], b_absH[start:stop], 'o', color='g')
    plt.plot(NG_s_H_mass[s_start:s_stop], s_absH[s_start:s_stop], '.', color='k')
    plt.plot(NG_m_h_array[0:][0], NG_m_h_array[0:][1], color='r')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')
    
    # K-band for binaries NextGen Isochrone.
    plt.subplot(1, 3, 3)
    plt.plot(NG_K_mass[start:stop], b_absK[start:stop], 'o', color='g')
    plt.plot(NG_s_K_mass[s_start:s_stop], s_absH[s_start:s_stop], '.', color='k')
    plt.plot(NG_m_k_array[0:][0], NG_m_k_array[0:][1], color='r')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    
    plot = raw_input("\nPlot Interpolations with magnitude values for NextGen? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            #plt.tight_layout()
            plt.show()
            leave = True
            #print '\n'
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
            #print '\n'
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot Interpolations with magnitude values? (Y|N): ")
            leave = False
    
    
    # J-band for binaries Dusty Isochrone.
    rcParams['figure.figsize'] = 21, 7
    #plt.suptitle(cluster+" Mass vs App Mag. (NextGen)", fontsize='22')
    plt.subplot(1, 3, 1)
    plt.plot(D_J_mass[start:stop], b_absJ[start:stop], 'o', color='g')
    plt.plot(D_s_J_mass[s_start:s_stop], s_absH[s_start:s_stop], '.', color='k')
    plt.plot(D_m_j_array[0:][0], D_m_j_array[0:][1], color='r')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
    
    # H-band for binaries Dusty Isochrone.
    plt.subplot(1, 3, 2)
    plt.plot(D_H_mass[start:stop], b_absH[start:stop], 'o', color='g')
    plt.plot(D_s_H_mass[s_start:s_stop], s_absH[s_start:s_stop], '.', color='k')
    plt.plot(D_m_h_array[0:][0], D_m_h_array[0:][1], color='r')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')
    
    # K-band for binaries Dusty Isochrone.
    plt.subplot(1, 3, 3)
    plt.plot(D_K_mass[start:stop], b_absK[start:stop], 'o', color='g')
    plt.plot(D_s_K_mass[s_start:s_stop], s_absH[s_start:s_stop], '.', color='k')
    plt.plot(D_m_k_array[0:][0], D_m_k_array[0:][1], color='r')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    
    plot = raw_input("\nPlot Interpolations with magnitude values for Dusty? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            #plt.tight_layout()
            plt.show()
            leave = True
            #print '\n'
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
            #print '\n'
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot Interpolations with magnitude values? (Y|N): ")
            leave = False    
    ###
    
    
    """
    # J-band mass histogram for primaries.
    plt.suptitle("Mass Histogram for Primaries", fontsize='22')
    plt.subplot(1, 3, 1)
    J_mass_P = []
    for n in range(len(J_mass)):
        odd = 2*n
        if odd > len(J_mass)-1:
            break
        J_mass_P.append(J_mass[odd])
        
    plt.hist(J_mass_P, bins=12, color = 'b')
    plt.title('J-band', fontsize='20')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    
    # H-band mass histogram for primaries.
    plt.subplot(1, 3, 2)
    H_mass_P = []
    for n in range(len(H_mass)):
        odd = 2*n
        if odd > len(H_mass)-1:
            break
        H_mass_P.append(H_mass[odd])
    
    plt.hist(H_mass_P, bins=12, color = 'b')
    plt.title('H-band', fontsize='20')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    
    # K-band mass histogram for primaries.
    plt.subplot(1, 3, 3)
    K_mass_P = []
    for n in range(len(K_mass)):
        odd = 2*n
        if odd > len(K_mass)-1:
            break
        K_mass_P.append(K_mass[odd])
    
    plt.hist(K_mass_P, bins=12, color = 'b')
    plt.title('K-band', fontsize='20')
    plt.xlabel('Mass / M_Sun', fontsize='18')

    
    plot = raw_input("\nPlot primary mass histogram for J, H, & K? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot primary mass histogram for J, H, & K? (Y|N): ")
            leave = False
    
    
    # J-band mass histogram for companions.
    plt.suptitle("Mass Histogram for Companions", fontsize='22')
    plt.subplot(1, 3, 1)
    J_mass_P = []
    for n in range(len(J_mass)):
        odd = 2*n +1
        if odd > len(J_mass)-1:
            break
        J_mass_P.append(J_mass[odd])
        
    plt.hist(J_mass_P, bins=12, color = 'r')
    plt.title('J-band', fontsize='20')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    
    # H-band mass histogram for companions.
    plt.subplot(1, 3, 2)
    H_mass_P = []
    for n in range(len(H_mass)):
        odd = 2*n +1
        if odd > len(H_mass)-1:
            break
        H_mass_P.append(H_mass[odd])
    
    plt.hist(H_mass_P, bins=12, color = 'r')
    plt.title('H-band', fontsize='20')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    
    # K-band mass histogram for companions.
    plt.subplot(1, 3, 3)
    K_mass_P = []
    for n in range(len(K_mass)):
        odd = 2*n +1
        if odd > len(K_mass)-1:
            break
        K_mass_P.append(K_mass[odd])
    
    plt.hist(K_mass_P, bins=12, color = 'r')
    plt.title('K-band', fontsize='20')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    
    plot = raw_input("\nPlot companion mass histogram for J, H, & K? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot companion mass histogram for J, H, & K? (Y|N): ")
            leave = False
    
    
    
    
    plt.plot(s_K_mass, s_absK, 'o', color='g')
    plt.plot(m_k_array[0:][0], m_k_array[0:][1], color='b')
    
    plt.xscale('log')
    plt.title("Single Stars", fontsize='22')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    
    plot = raw_input("\nPlot Interpolation with K-band for single stars? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot Interpolation with K-band for single stars? (Y|N): ")
            leave = False
    """
    
    
    
    
    
    ### Section for calculating the statistical argument... ###
    area = load_stat(cluster)[0]
    magnitude = load_stat(cluster)[1]
    J_count = load_stat(cluster)[2]
    H_count = load_stat(cluster)[3]
    K_count = load_stat(cluster)[4]
    
    comp_names = []
    J_c_index = []; H_c_index = []; K_c_index = []
    for i in range(start+1, stop, 2):
        #print "binary array index:", i
        print b_absJ[i]
        if b_absJ[i] == -100:
            J_c_index.append(-100)
            print "Not a number in J!"
        if b_absH[i] == -100:
            H_c_index.append(-100)
            print "Not a number in H!"
        if b_absK[i] == -100:
            K_c_index.append(-100)
            print "Not a number in K!"
        for j in range(len(magnitude)):
            #print "magnitude array index:", j
            try:
                if b_absJ[i] != -100 and b_absJ[i] <= magnitude[0]:
                    #print "b_absJ:", b_absJ[i]
                    #print "magnitude:", magnitude[j]
                    J_c_index.append(j)
                if b_absJ[i] > magnitude[j] and b_absJ[i] <= magnitude[j+1]:
                    print "magnitude:", magnitude[j], magnitude[j+1]
                    J_c_index.append(j+1)
            except (IndexError, ValueError):
                print "Index or Value error!"
                pass
                #J_c_index.append('nan')
            try:
                if b_absH[i] != -100 and b_absH[i] <= magnitude[0]:
                    H_c_index.append(j)
                if b_absH[i] > magnitude[j] and b_absH[i] <= magnitude[j+1]:
                    H_c_index.append(j+1)
            except (IndexError, ValueError):
                print "Index or Value error!"
                pass
                #H_c_index.append('nan')
            try:
                if b_absK[i] != -100 and b_absK[i] <= magnitude[0]:
                    K_c_index.append(j)
                if b_absK[i] > magnitude[j] and b_absK[i] <= magnitude[j+1]:
                    K_c_index.append(j+1)
            except (IndexError, ValueError):
                pass
        comp_names.append(b_names[i].rstrip())
    #print comp_names
    
    print J_c_index
    J_c_array = []; H_c_array = []; K_c_array = []
    for i in range(len(J_c_index)):
        if J_c_index[i] == -100:
            J_c_array.append(0)
        else:
            J_c_array.append(np.sum(J_count[0:J_c_index[i]]))
    for i in range(len(H_c_index)):
        if H_c_index[i] == -100:
            H_c_array.append(0)
        else:
            H_c_array.append(np.sum(H_count[0:H_c_index[i]]))
    for i in range(len(K_c_index)):
        if K_c_index[i] == -100:
            K_c_array.append(0)
        else:
            K_c_array.append(np.sum(K_count[0:K_c_index[i]]))
    #print J_c_array
    
    radius = 5.
    poisson_J = np.exp( -(J_c_array/(area * 3600.**2) * np.pi * radius**2))
    poisson_H = np.exp( -(H_c_array/(area * 3600.**2) * np.pi * radius**2))
    poisson_K = np.exp( -(K_c_array/(area * 3600.**2) * np.pi * radius**2))
    for i in range(len(poisson_J)):
        if poisson_J[i] == 1:
            poisson_J[i] = 0
    for i in range(len(poisson_H)):
        if poisson_H[i] == 1:
            poisson_H[i] = 0
    for i in range(len(poisson_K)):
        if poisson_K[i] == 1:
            poisson_K[i] = 0
    
    print "\nPoisson J, H, & K band Calc.:"
    print "J:", poisson_J
    print "H:", poisson_H
    print "K:", poisson_K
    ###########################################################
    
    
    # fixing data to be for just the cluster selected for saving.......
    J_m = []; H_m = []; K_m = []
    NG_J_m = []; NG_H_m = []; NG_K_m = []
    D_J_m = []; D_H_m = []; D_K_m = []
    for i in range(start, stop):
        J_m.append(J_mass[i])
        K_m.append(K_mass[i])
        H_m.append(H_mass[i])
        NG_J_m.append(NG_J_mass[i])
        NG_H_m.append(NG_H_mass[i])
        NG_K_m.append(NG_K_mass[i])
        D_J_m.append(D_J_mass[i])
        D_H_m.append(D_H_mass[i])
        D_K_m.append(D_K_mass[i])
    J_mass = J_m; H_mass = H_m; K_mass = K_m
    NG_J_mass = NG_J_m; NG_H_mass = NG_H_m; NG_K_mass = NG_K_m
    D_J_mass = D_J_m; D_H_mass = D_H_m; D_K_mass = D_K_m
    
    s_J_m = []; s_H_m = []; s_K_m = []
    NG_s_J_m = []; NG_s_H_m = []; NG_s_K_m = []
    D_s_J_m = []; D_s_H_m = []; D_s_K_m = []
    for i in range(s_start, s_stop):
        s_J_m.append(s_J_mass[i])
        s_K_m.append(s_K_mass[i])
        s_H_m.append(s_H_mass[i])
        NG_s_J_m.append(NG_s_J_mass[i])
        NG_s_H_m.append(NG_s_H_mass[i])
        NG_s_K_m.append(NG_s_K_mass[i])
        D_s_J_m.append(D_s_J_mass[i])
        D_s_H_m.append(D_s_H_mass[i])
        D_s_K_m.append(D_s_K_mass[i])
    s_J_mass = s_J_m; s_H_mass = s_H_m; s_K_mass = s_K_m
    NG_s_J_mass = NG_s_J_m; NG_s_H_mass = NG_s_H_m; NG_s_K_mass = NG_s_K_m
    D_s_J_mass = D_s_J_m; D_s_H_mass = D_s_H_m; D_s_K_mass = D_s_K_m
    
    print "\nSaving data..."
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/'+cluster+'_mass_data',
    J_M= J_mass, H_M= H_mass, K_M= K_mass, s_J_M= s_J_mass, s_H_M= s_H_mass, s_K_M= s_K_mass,
    NG_J_M= NG_J_mass, NG_H_M= NG_H_mass, NG_K_M= NG_K_mass, NG_s_J_M= NG_s_J_mass, NG_s_H_M= NG_s_H_mass, NG_s_K_M= NG_s_K_mass,
    D_J_M= D_J_mass, D_H_M= D_H_mass, D_K_M= D_K_mass, D_s_J_M= D_s_J_mass, D_s_H_M= D_s_H_mass, D_s_K_M= D_s_K_mass)
    
    
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Stat_Argument/Stat_Data/'+cluster+'_stat_data',
    P_J = poisson_J, P_H = poisson_H, P_K = poisson_K, Comp_Names = comp_names)
    print "Save data complete!"
    
    
    # Run 'sort_isochron.py' after.
    print("\n=====================================================================")
    again = raw_input("Run sort_isochron.py to sort/print data? (y/n): ")
    while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
        again = raw_input("Please enter (y/n): ")
    if again == 'Y' or again == 'y':
        print("\n=====================================================================")
        os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/sort_isochrone.py")
    elif again == 'N' or again == 'n':
        print '\n'
        
    
    # Re-execute program.
    print("\n=====================================================================")
    again = raw_input("Run plot_mass_stat.py again? (y/n): ")
    while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
        again = raw_input("Please enter (y/n): ")
    if again == 'Y' or again == 'y':
        print("\n=====================================================================")
        os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/plot_mass_stat.py")
    elif again == 'N' or again == 'n':
        print('\nAll process are complete!')
    
    

def load_main(cluster):
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/mass.txt')
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/M_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/M_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/main/M_k.txt')
    
    return mass, m_j, m_h, m_k


def load_NextGen(cluster):
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/mass.txt')
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/M_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/M_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/NextGen/M_k.txt')
    
    return mass, m_j, m_h, m_k


def load_Dusty(cluster):
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/mass.txt')
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/M_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/M_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Clusters/'+str(cluster)+'/Dusty/M_k.txt')
    
    return mass, m_j, m_h, m_k


def load_stat(cluster):
    actual_area = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/actual_area.txt')
    magnitude = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/actual_mag.txt')
    J_count = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/J_count.txt')
    H_count = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/H_count.txt')
    K_count = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Stat_Argument/Stat_Data/Clusters/'+str(cluster)+'/K_count.txt')

    return actual_area, magnitude, J_count, H_count, K_count


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx, array[idx]


def round2SignifFigs(vals,n):
    """
    (list, int) -> numpy array
    (numpy array, int) -> numpy array

    In: a list/array of values
    Out: array of values rounded to n significant figures

    Does not accept: inf, nan, complex

    >>> m = [0.0, -1.2366e22, 1.2544444e-15, 0.001222]
    >>> round2SignifFigs(m,2)
    array([  0.00e+00,  -1.24e+22,   1.25e-15,   1.22e-03])
    """
    if np.all(np.isfinite(vals)) and np.all(np.isreal((vals))):
        eset = np.seterr(all='ignore')
        mags = 10.0**np.floor(np.log10(np.abs(vals)))  # omag's
        vals = np.around(vals/mags,n)*mags             # round(val/omag)*omag
        np.seterr(**eset)
        vals[np.where(np.isnan(vals))] = 0.0           # 0.0 -> nan -> 0.0
    else:
        raise IOError('Input must be real and finite')
    return vals




if __name__ == '__main__':
	main()