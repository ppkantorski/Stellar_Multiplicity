#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def main():
    # Loading Isochron Data & Binary/Single Magnitude Data.
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Main/mass.txt')
    Teff = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Main/temperature.txt')
    age = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Main/age.txt')
    luminosity = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Main/luminosity.txt')
    
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Main/m_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Main/m_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/Main/m_k.txt')
    
    b_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsJ.txt')
    b_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsH.txt')
    b_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsK.txt')
    
    s_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsJ.txt')
    s_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsH.txt')
    s_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsK.txt')
    
    b_DelJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelJ.txt')
    b_DelH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelH.txt')
    b_DelK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_DelK.txt')
    
    """
    # Code for applying the upper and lower error propogation.
    blanket = 0.01  # Should be 0.01 (happens to be the same for both).
    sign = 1  # Should be either +1 or -1.
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
    b_absK = b_K
    """

    ### Code for plotting Mass vs L, Teff, & Age. ###   
    n = 1
    while n < 4:
        plt.suptitle("Mass vs L, Teff, & Age", fontsize='22')
        plt.subplot(1, 3, n)
        
        # Mass vs Luminosity
        if n == 1:
            x = mass
            y = luminosity
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.001)
            ynew = interpolate.splev(xnew, tck, der=0)
            ML_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, luminosity, 'o', color='b')
            plt.xscale('log')
            plt.yscale('log')
            
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Luminosity / L_Sun', fontsize='18')
        # Mass vs Teff
        if n == 2:
            x = mass
            y = Teff
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.001)
            ynew = interpolate.splev(xnew, tck, der=0)
            MT_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, Teff, 'o', color='b')
            plt.xscale('log')
            plt.yscale('log')
            
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Teff / T_Sun', fontsize='18')
        # Mass vs log(Age)
        if n == 3:
            x = mass
            y = np.log(age)/np.log(10)
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.001)
            ynew = interpolate.splev(xnew, tck, der=0)
            MA_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, np.log(age)/np.log(10), 'o', color='b')
            plt.xscale('log')
            #plt.yscale('log')
            
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('log(Age)', fontsize='18')
        n += 1
        
    plot = raw_input("\nPlot Isochron w/ Interpolation? (Y|N): ")
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
            #rint '\n'
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot Isochron w/ Interpolation? (Y|N): ")
            leave = False
    
    #################################################
    
    
    
    ### Code for plotting Mass vs Mag J, H, & K. ###
    # Mass vs MagJ
    x = mass
    y = m_j
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_j_array = [xnew, ynew]
    
    plt.suptitle("Isochron Mass vs App Mag.", fontsize='22')
    plt.subplot(1, 3, 1)
    plt.plot(xnew, ynew, color='r')
    plt.plot(mass, m_j, 'o', color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
            
    # Mass vs MagH
    x = mass
    y = m_h
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_h_array = [xnew, ynew]
    
    plt.subplot(1, 3, 2)
    plt.plot(xnew, ynew, color='r')
    plt.plot(mass, m_h, 'o', color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')

    # Mass vs MagK
    x = mass
    y = m_k
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_k_array = [xnew, ynew]
    
    plt.subplot(1, 3, 3)
    plt.plot(xnew, ynew, color='r')
    plt.plot(mass, m_k, 'o', color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
        
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    
    plot = raw_input("\nPlot mass Isochron w/ Interpolation? (Y|N): ")
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
            #rint '\n'
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot mass Isochron w/ Interpolation? (Y|N): ")
            leave = False
    ################################################
    

    # The following is code to find the corresponding mass values from Mag J, H, & K.
    J_mass = []
    for i in range(0, len(b_absJ)):
        index = find_nearest(m_j_array[1:][0], b_absJ[i])[0]
        J_mass.append(m_j_array[0:][0][index])
        #print index, m_j_array[0:][0][index]
    H_mass = []
    for i in range(0, len(b_absH)):
        index = find_nearest(m_h_array[1:][0], b_absH[i])[0]
        H_mass.append(m_h_array[0:][0][index])
        #print index, m_h_array[0:][0][index]
    K_mass = []
    for i in range(0, len(b_absK)):
        index = find_nearest(m_k_array[1:][0], b_absK[i])[0]
        K_mass.append(m_k_array[0:][0][index])
        #print index, m_k_array[0:][0][index]
    s_J_mass = []
    for i in range(0, len(s_absJ)):
        index = find_nearest(m_j_array[1:][0], s_absJ[i])[0]
        s_J_mass.append(m_j_array[0:][0][index])
        #print index, m_k_array[0:][0][index]
    s_H_mass = []
    for i in range(0, len(s_absH)):
        index = find_nearest(m_h_array[1:][0], s_absH[i])[0]
        s_H_mass.append(m_h_array[0:][0][index])
        #print index, m_k_array[0:][0][index]
    s_K_mass = []
    for i in range(0, len(s_absK)):
        index = find_nearest(m_k_array[1:][0], s_absK[i])[0]
        s_K_mass.append(m_k_array[0:][0][index])
        #print index, m_k_array[0:][0][index]
    
    
    ###

    # J-band for binaries.
    plt.suptitle("Binary Mass vs App Mag.", fontsize='22')
    plt.subplot(1, 3, 1)
    plt.plot(J_mass, b_absJ, 'o', color='g')
    plt.plot(m_j_array[0:][0], m_j_array[0:][1], color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
    
    # H-band for binaries
    plt.subplot(1, 3, 2)
    plt.plot(H_mass, b_absH, 'o', color='g')
    plt.plot(m_h_array[0:][0], m_h_array[0:][1], color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')
    
    # K-band for binaries
    plt.subplot(1, 3, 3)
    plt.plot(K_mass, b_absK, 'o', color='g')
    plt.plot(m_k_array[0:][0], m_k_array[0:][1], color='b')
    plt.xscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    
    plot = raw_input("\nPlot Interpolations with magnitude values? (Y|N): ")
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
    
    print len(J_mass)
    
    print "\nSaving data..."
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/mass_data',
    J_M= J_mass, H_M= H_mass, K_M= K_mass, s_J_M= s_J_mass, s_H_M= s_H_mass, s_K_M= s_K_mass)
    print "Save data complete!"
        


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