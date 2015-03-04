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
    
    sigfigs = 4
    b_absJ = round2SignifFigs( np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsJ.txt'), sigfigs)
    b_absH = round2SignifFigs( np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsH.txt'), sigfigs)
    b_absK = round2SignifFigs( np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/bin_AbsK.txt'), sigfigs)
    s_absK = round2SignifFigs( np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/single_AbsK.txt'), sigfigs)

    ### Code for plotting Mass vs L, Teff, & Age. ###   
    """"
    n = 1
    
    while n < 4:
        plt.subplot(1, 3, n)
        
        # Mass vs Luminosity
        if n == 1:
            x = mass
            y = luminosity
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.0001)
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
            xnew = np.arange(0.1, 7.0, 0.0001)
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
            y = age
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.0001)
            ynew = interpolate.splev(xnew, tck, der=0)
            MA_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, age, 'o', color='b')
            plt.xscale('log')
            #plt.yscale('log')
            
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Age', fontsize='18')
        n += 1
        
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    
    plt.tight_layout()
    plt.show()
    #################################################
    """
    
    
    ### Code for plotting Mass vs Mag J, H, & K. ###
    n = 1
    while n < 4:
        plt.subplot(1, 3, n)
        
        # Mass vs MagJ
        if n == 1:
            x = mass
            y = m_j
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.000001)
            ynew = interpolate.splev(xnew, tck, der=0)
            m_j_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, m_j, 'o', color='b')
            plt.xscale('log')
            #plt.yscale('log')
    
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Mag_J', fontsize='18')
            
        # Mass vs MagH
        if n == 2:
            x = mass
            y = m_h
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.000001)
            ynew = interpolate.splev(xnew, tck, der=0)
            m_h_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, m_h, 'o', color='b')
            plt.xscale('log')
            #plt.yscale('log')

            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Mag_H', fontsize='18')

        # Mass vs MagK
        if n == 3:
            x = mass
            y = m_h
            tck = interpolate.splrep(x, y, s=0)
            xnew = np.arange(0.1, 7.0, 0.000001)
            ynew = interpolate.splev(xnew, tck, der=0)
            m_k_array = [xnew, ynew]
            
            plt.plot(xnew, ynew, color='r')
            plt.plot(mass, m_k, 'o', color='b')
            plt.xscale('log')
            #plt.yscale('log')

            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Mag_K', fontsize='18')
        n += 1
        
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    
    plot = raw_input("\nPlot Isochron w/ Interpolation? (Y|N): ")
    leave = False
    while leave == False:
        if plot == 'Y' or plot == 'y':
            plt.tight_layout()
            plt.show()
            leave = True
            print '\n'
        elif plot == 'N' or plot == 'n':
            plt.close()
            leave = True
            print '\n'
        elif plot != 'y' and plot != 'y' and plot != 'N' and plot != 'n':
            plot = raw_input("Plot Isochron w/ Interpolation? (Y|N): ")
            leave = False
        
    ################################################
    

    # The following is code to find the corresponding mass values from Mag J, H, & K.
    
    print len(b_absJ)
    J_mass = []
    m_j_rounded = round2SignifFigs(m_j_array[1:][0], sigfigs)
    for i in range(0, len(b_absJ)):
        #print i
        if b_absJ[i] == 0:
            print "AbsJ Entry:", i, "               Data point is empty!"
            #print "Corresponding Mass:", 0.000
            J_mass.append(0)
        if b_absJ[i] > 10.49 or b_absJ[i] < -1.14:
            print "AbsJ Entry:", i, "               Data point is out of range!"
            J_mass.append(0)
        end = -10    
        for j in range(0, len(xnew)):
            #print m_j_array[1:][0][j]
            if b_absJ[i] == m_j_rounded[j]:
                if end == i:
                    break
                end = i
                print "AbsJ Entry:", i, "               Isochron Entry:", j
                #print "Binary AbsJ:", b_absJ[i], "          Rounded AbsJ:", m_j_rounded[j]
                #print "Isochron AbsJ:", m_j_array[1:][0][j]
                #print "Corresponding Mass:", m_j_array[0:][0][j], "\n"
                J_mass.append(m_j_array[0:][0][j])
        #print "Length of J_mass:", len(J_mass)
    #print J_mass
    #print len(J_mass)
    """
    plt.plot(J_mass, b_absJ, 'o', color='g')
    plt.plot(m_j_array[0:][0], m_j_array[0:][1], color='b')
    
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_J', fontsize='18')
    plt.tight_layout()
    plt.show()
    """
    
    #print len(b_absH)
    H_mass = []
    m_h_rounded = round2SignifFigs(m_h_array[1:][0], sigfigs)
    for i in range(0, len(b_absH)):
        if b_absH[i] == 0:
            print "AbsH Entry:", i, "               Data point is empty!"
            #print "Corresponding Mass:", 0.000
            H_mass.append(0)
        if b_absH[i] > 9.77 or b_absH[i] < -1.05:
            print "AbsH Entry:", i, "               Data point is out of range!"
            H_mass.append(0)
        end = -10    
        for j in range(0, len(xnew)):
            #print m_j_array[1:][0][j]
            if b_absH[i] == m_h_rounded[j]:
                if end == i:
                    break
                end = i
                print "AbsH Entry:", i, "               Isochron Entry:", j
                #print "Binary AbsH:", b_absH[i], "          Rounded AbsH:", m_h_rounded[j]
                #print "Isochron AbsH:", m_h_array[1:][0][j]
                #print "Corresponding Mass:", m_h_array[0:][0][j], "\n"
                H_mass.append(m_h_array[0:][0][j])
        #print "Length of H_mass:", len(H_mass)
    """
    plt.plot(H_mass, b_absH, 'o', color='g')
    plt.plot(m_h_array[0:][0], m_h_array[0:][1], color='b')
    
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_H', fontsize='18')
    plt.tight_layout()
    plt.show()
    """  
    
    #print len(b_absK)
    K_mass = []
    m_k_rounded = round2SignifFigs(m_k_array[1:][0], sigfigs)
    for i in range(0, len(b_absK)):
        if b_absK[i] == 0:
            print "AbsK Entry:", i, "               Data point is empty!"
            #print "Data point is empty!\n"
            #print "Corresponding Mass:", 0.000
            K_mass.append(0)
        if b_absK[i] > 9.32 or b_absK[i] < -0.97:
            print "AbsK Entry:", i, "               Data point is out of range!"
            K_mass.append(0)
        end = -10    
        if b_absK[i] <= 9.32 and b_absK[i] >= -0.97:
            for j in range(0, len(xnew)):
                #print m_j_array[1:][0][j]
                if b_absK[i] == m_k_rounded[j]:
                    if end == i:
                        break
                    end = i
                    print "AbsK Entry:", i, "               Isochron Entry:", j
                    print "Binary AbsK:", b_absK[i], "          Rounded AbsK:", m_k_rounded[j]
                    print "Isochron AbsK:", m_k_array[1:][0][j]
                    #print "Corresponding Mass:", m_k_array[0:][0][j], "\n"
                    K_mass.append(m_k_array[0:][0][j])
        #print "Length of K_mass:", len(K_mass)
    """
    plt.plot(K_mass, b_absK, 'o', color='g')
    plt.plot(m_k_array[0:][0], m_k_array[0:][1], color='b')
    
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    plt.tight_layout()
    plt.show()
    """
    
    S_K_mass = []
    m_k_rounded = round2SignifFigs(m_k_array[1:][0], sigfigs)
    for i in range(0, len(s_absK)):
        if s_absK[i] == 0:
            print "AbsK Entry:", i, "               Data point is empty!"
            #print "Data point is empty!\n"
            #print "Corresponding Mass:", 0.000
            S_K_mass.append(0)
        if s_absK[i] > 9.32 or s_absK[i] < -0.97:
            print "AbsK Entry:", i, "               Data point is out of range!"
            S_K_mass.append(0)
        end = -10
        if s_absK[i] <= 9.32 and s_absK[i] >= -0.97:
            for j in range(0, len(xnew)):
                #print m_j_array[1:][0][j]
                if s_absK[i] == m_k_rounded[j]:
                    if end == i:
                        break
                    end = i
                    print "AbsK Entry:", i, "               Isochron Entry:", j
                    #print "Binary AbsK:", b_absK[i], "          Rounded AbsK:", m_k_rounded[j]
                    #print "Isochron AbsK:", m_k_array[1:][0][j]
                    #print "Corresponding Mass:", m_k_array[0:][0][j], "\n"
                    S_K_mass.append(m_k_array[0:][0][j])
    """
    plt.plot(S_K_mass, s_absK, 'o', color='g')
    plt.plot(m_k_array[0:][0], m_k_array[0:][1], color='b')
    
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Mass / M_Sun', fontsize='18')
    plt.ylabel('Mag_K', fontsize='18')
    plt.tight_layout()
    plt.show()
    """

    print "Saving data..."
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/Abs_Data/mass_data',
    J_M= J_mass, H_M= H_mass, K_M= K_mass, S_K_M= S_K_mass)
    print "Save data complete!"


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