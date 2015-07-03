#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def main():
    # Loading Isochron Data & Binary/Single Magnitude Data.
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/mass.txt')
    Teff = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/temperature.txt')
    age = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/age.txt')
    luminosity = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/luminosity.txt')
    
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Isochron_Data/main/m_k.txt')
    
    b_absJ = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsJ.txt')
    b_absH = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsH.txt')
    b_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsK.txt')
    s_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsK.txt')

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
        # Mass vs Age
        if n == 3:
            x = mass
            y = np.log(age)/np.log(10)
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.001)
            ynew = interpolate.splev(xnew, tck, der=0)
            MA_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, np.log(age)/np.log(10), 'o', color='b')
            #plt.xscale('log')
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
    
    
    ### Code for plotting log(Age) vs Mag J, H, & K. ###
    # Mass vs MagJ
    x = mass
    y = m_j
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_j_array = [xnew, ynew]
    
    plt.suptitle("Isochron log(Age) vs App Mag.", fontsize='22')
    plt.subplot(1, 3, 1)
    print MA_array[0:][1]
    plt.plot(MA_array[0:][1], ynew, color='r')
    plt.plot(np.log(age)/np.log(10), m_j, 'o', color='b')
    plt.xlabel('log(Age)', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
            
    # Mass vs MagH
    x = mass
    y = m_h
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_h_array = [xnew, ynew]
    
    plt.subplot(1, 3, 2)
    plt.plot(MA_array[0:][1], ynew, color='r')
    plt.plot(np.log(age)/np.log(10), m_h, 'o', color='b')
    plt.xlabel('log(Age)', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')

    # Mass vs MagK
    x = mass
    y = m_k
    tck = interpolate.splrep(x, y, s=0)
    xnew = np.arange(0.1, 7.0, 0.001)
    ynew = interpolate.splev(xnew, tck, der=0)
    m_k_array = [xnew, ynew]
    
    plt.subplot(1, 3, 3)
    plt.plot(MA_array[0:][1], ynew, color='r')
    plt.plot(np.log(age)/np.log(10), m_k, 'o', color='b')
    plt.xlabel('log(Age)', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
        
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    
    plot = raw_input("\nPlot age Isochron w/ Interpolation? (Y|N): ")
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
            plot = raw_input("Plot age Isochron w/ Interpolation? (Y|N): ")
            leave = False
    ################################################
    

    # The following is code to find the corresponding age values from Mag J, H, & K.
    J_age = []
    for i in range(0, len(b_absJ)):
        index = find_nearest(m_j_array[1:][0], b_absJ[i])[0]
        J_age.append(MA_array[0:][1][index])
        #print index, m_j_array[0:][0][index]
    H_age = []
    for i in range(0, len(b_absH)):
        index = find_nearest(m_h_array[1:][0], b_absH[i])[0]
        H_age.append(MA_array[0:][1][index])
        #print index, m_h_array[0:][0][index]
    K_age = []
    for i in range(0, len(b_absK)):
        index = find_nearest(m_k_array[1:][0], b_absK[i])[0]
        K_age.append(MA_array[0:][1][index])
        #print index, m_k_array[0:][0][index]
    s_K_age = []
    for i in range(0, len(s_absK)):
        index = find_nearest(m_k_array[1:][0], s_absK[i])[0]
        s_K_age.append(MA_array[0:][1][index])
        #print index, m_k_array[0:][0][index]
    
    
    ###

    # J-band for binaries.
    plt.suptitle("Binary log(Age) vs App Mag.", fontsize='22')
    plt.subplot(1, 3, 1)
    plt.plot(J_age, b_absJ, 'o', color='g')
    plt.plot(MA_array[0:][1], m_j_array[0:][1], color='b')
    #plt.xscale('log')
    plt.xlabel('log(Age)', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
    
    # H-band for binaries
    plt.subplot(1, 3, 2)
    plt.plot(H_age, b_absH, 'o', color='g')
    plt.plot(MA_array[0:][1], m_h_array[0:][1], color='b')
    #plt.xscale('log')
    plt.xlabel('log(Age)', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')
    
    # K-band for binaries
    plt.subplot(1, 3, 3)
    plt.plot(K_age, b_absK, 'o', color='g')
    plt.plot(MA_array[0:][1], m_k_array[0:][1], color='b')
    #plt.xscale('log')
    plt.xlabel('log(Age)', fontsize='18')
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
    
    
    ### Histograms ###

    # J-band age histogram for primary.
    plt.suptitle("Age Histogram for Primaries", fontsize='22')
    plt.subplot(1, 3, 1)
    J_age_P = []
    for n in range(len(J_age)):
        odd = 2*n
        if odd > len(J_age)-1:
            break
        J_age_P.append(J_age[odd])
    plt.hist(J_age_P, bins=12, color='b')
    plt.title('J-band', fontsize='20')
    plt.xlabel('log(Age)', fontsize='18')
    
    # H-band age histogram for primary.
    plt.subplot(1, 3, 2)
    H_age_P = []
    for n in range(len(H_age)):
        odd = 2*n
        if odd > len(H_age)-1:
            break
        H_age_P.append(H_age[odd])
    plt.hist(H_age_P, bins=12, color ='b')
    plt.title('H-band', fontsize='20')
    plt.xlabel('log(Age)', fontsize='18')
    
    # K-band age histogram for primary.
    plt.subplot(1, 3, 3)
    K_age_P = []
    for n in range(len(K_age)):
        odd = 2*n
        if odd > len(K_age)-1:
            break
        K_age_P.append(K_age[odd])
    plt.hist(K_age_P, bins=12, color ='b')
    plt.title('K-band', fontsize='20')
    plt.xlabel('log(Age)', fontsize='18')

    
    plot = raw_input("\nPlot primary age histogram for J, H, & K? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot primary age histogram for J, H, & K? (Y|N): ")
            leave = False
    
    
    # J-band age histogram for companions.
    plt.suptitle("Age Histogram for Companions", fontsize='22')
    plt.subplot(1, 3, 1)
    J_age_P = []
    for n in range(len(J_age)):
        odd = 2*n + 1
        if odd > len(J_age)-1:
            break
        J_age_P.append(J_age[odd])
    plt.hist(J_age_P, bins=12, color='r')
    plt.title('J-band', fontsize='20')
    plt.xlabel('log(Age)', fontsize='18')
    
    # H-band age histogram for companions.
    plt.subplot(1, 3, 2)
    H_age_P = []
    for n in range(len(H_age)):
        odd = 2*n + 1
        if odd > len(H_age)-1:
            break
        H_age_P.append(H_age[odd])
    plt.hist(H_age_P, bins=12, color ='r')
    plt.title('H-band', fontsize='20')
    plt.xlabel('log(Age)', fontsize='18')
    
    # K-band age histogram for companions.
    plt.subplot(1, 3, 3)
    K_age_P = []
    for n in range(len(K_age)):
        odd = 2*n + 1
        if odd > len(K_age)-1:
            break
        K_age_P.append(K_age[odd])
    plt.hist(K_age_P, bins=12, color ='r')
    plt.title('K-band', fontsize='20')
    plt.xlabel('log(Age)', fontsize='18')

    
    plot = raw_input("\nPlot companion age histogram for J, H, & K? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.show()
            leave = True
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot companion age histogram for J, H, & K? (Y|N): ")
            leave = False
    ##################
    
    
    
    plt.plot(s_K_age, s_absK, 'o', color='g')
    plt.plot(MA_array[0:][1], m_k_array[0:][1], color='b')
    
    #plt.xscale('log')
    plt.title("Single Stars", fontsize='22')
    plt.xlabel('log(Age)', fontsize='18')
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
    
    
    print "\nSaving data..."
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/age_data',
    J_M= J_age, H_M= H_age, K_M= K_age, s_K_M= s_K_age)
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