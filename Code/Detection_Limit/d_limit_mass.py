#!/usr/bin/env python

# This code addes mass values to the datasets that will be fed into the 'plot_d_lim_bin.py' function.

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
    
    
    bs_choice = raw_input("Singles or Binaries (s|b)? : ")
    stay = True
    while stay == True:
        if bs_choice != 's' and bs_choice != 'S' and bs_choice != 'b' and bs_choice != 'B':
            bs_choice = raw_input("Please Enter (s|b): ")
        else:
            stay = False
    
    
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
            s_stop = 112 + 1
            stay = False
            break
        else:
            stay = True


    # This section was added to load the recalculated detection limit data.
    if bs_choice == 's' or bs_choice == 'S':
        data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/Recalculations/'+cluster+'_sin_data.npz')
        names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/sin_names.txt', 'r').readlines()[s_start:s_stop]
        absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/sin_AbsK.txt')[s_start:s_stop]
        
    if bs_choice == 'b' or bs_choice == 'B':
        data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_bin_data.npz')
        names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/bin_names.txt', 'r').readlines()[start:stop][0::2]
        absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/bin_AbsK.txt')[start:stop][0::2]
    
    star_name = data['star_name']
    ang_sep = data['ang_sep']
    mag_K = data['mag_K']
    #max_flux = data['max_flux']
    #print max_flux.shape
    

    #print 'name:', names
    #print 'absK:', absK
    print star_name
    
    
    if bs_choice == 's' or bs_choice == 'S':
        i = 0; j = 0;
        while i < len(star_name):
            try:
                plt.plot(ang_sep[i], mag_K[i], '-', label= names[j])
                if star_name[i] == star_name[i+1]:
                    i = i + 1
                    plt.plot(ang_sep[i], mag_K[i], '-')
                    if star_name[i] == star_name[i+1]:
                        i = i + 1
                        plt.plot(ang_sep[i], mag_K[i], '-')
            except IndexError:
                print 'Index:', i
                print 'length:', len(star_name)
                print 'End of list reached!'
            i = i + 1
            j = j + 1
    
    
    if bs_choice == 'b' or bs_choice == 'B':
        i = 0; j = 0;
        while i < len(star_name):        
            try:
                plt.plot(ang_sep[i], mag_K[i], '-', label= names[j])
                if star_name[i] == star_name[i+1]:
                    i = i + 1
                    plt.plot(ang_sep[i], mag_K[i], '-')
                    if star_name[i] == star_name[i+1]:
                        i = i + 1
                        plt.plot(ang_sep[i], mag_K[i], '-')
                if names[j] == names[j+1]:
                    j = j + 1
                    if names[j] == names[j+1]:
                        j = j + 1
            except IndexError:
                print 'length:', len(star_name)
                print 'End of list reached!'
            i = i + 1
            j = j + 1
    
    plt.title('Delta K Plot for '+cluster, fontsize='22')                                                  
    plt.xlabel('Angular Seperation', fontsize='18')                                           
    plt.ylabel('Mag_K', fontsize='18')                                                        
    plt.xscale('log')    
    plt.gca().invert_yaxis()
    #plt.legend()                  
    plt.show()
    
    
    
    
    if bs_choice == 's' or bs_choice == 'S':
        i = 0; j = 0;
        while i < len(star_name):
            try:
                print 'i:', i, 'j:', j
                print star_name[i], names[j], absK[j]
                mag_K[i] = mag_K[i] + absK[j]
                plt.plot(ang_sep[i], mag_K[i], '-', label= names[j])
                if star_name[i] == star_name[i+1]:
                    mag_K[i+1] = mag_K[i+1] + absK[j]
                    i = i + 1
                    plt.plot(ang_sep[i], mag_K[i], '-')
                    print star_name[i], names[j], absK[j]
                    
                    if star_name[i] == star_name[i+1]:
                        mag_K[i+1] = mag_K[i+1] + absK[j]
                        i = i + 1
                        plt.plot(ang_sep[i], mag_K[i], '-')
                        print star_name[i], names[j], absK[j]
                        
            except IndexError:
                print 'Index:', i
                print 'length:', len(star_name)
                print 'End of list reached!'
            
            i = i + 1
            j = j + 1
    
    
    if bs_choice == 'b' or bs_choice == 'B':
        i = 0; j = 0;
        while i < len(star_name):        
            try:
                print star_name[i], names[j], absK[j]
                mag_K[i] = mag_K[i] + absK[j]
                plt.plot(ang_sep[i], mag_K[i], '-', label= names[j])
                if star_name[i] == star_name[i+1]:
                    mag_K[i+1] = mag_K[i+1] + absK[j]
                    i = i + 1
                    plt.plot(ang_sep[i], mag_K[i], '-')
                    print star_name[i], names[j], absK[j]
                    
                    if star_name[i] == star_name[i+1]:
                        mag_K[i+1] = mag_K[i+1] + absK[j]
                        i = i + 1
                        plt.plot(ang_sep[i], mag_K[i], '-')
                        print star_name[i], names[j], absK[j]
        
                if names[j] == names[j+1]:
                    j = j + 1
                    if names[j] == names[j+1]:
                        j = j + 1
                        
            except IndexError:
                print 'length:', len(star_name)
                print 'End of list reached!'
            
            i = i + 1
            j = j + 1
            
            #a = np.empty(len(mag_K[i])); a.fill(ang_sep[i])
    
    print 'ang_sep len:', len(ang_sep)
    print 'mag_K len:', len(mag_K)
    
    #for i in range(len(mag_K)):
    #    plt.plot(ang_sep[i], mag_K[i], '.')
    #plt.title('Delta K Plot for '+cluster, fontsize='22')                                                  
    #plt.xlabel('Angular Seperation', fontsize='18')                                           
    #plt.ylabel('Mag_K', fontsize='18')                                                        
    #plt.xscale('log')    
    #plt.gca().invert_yaxis()
    #plt.legend()                  
    #plt.show()
    
    #######################################################################


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
    

    # The following is code to find the corresponding mass values from mag_K.
    K_mass = []; K_m_array = []
    NG_K_mass = []; NG_K_array = []
    D_K_mass = []; D_K_array = []
    
    fix_K_mass = []; fix_K_m_array = []; M_cutoff = 0.5
    
    for i in range(0, len(mag_K)):
        K_mass = []; NG_K_mass = []; D_K_mass = []; fix_K_mass = [];
        for j in range(0, len(mag_K[i])):
            index = find_nearest(m_k_array[1:][0], mag_K[i][j])[0]
            K_mass.append(m_k_array[0:][0][index])
            NG_index = find_nearest(NG_m_k_array[1:][0], mag_K[i][j])[0]
            NG_K_mass.append(NG_m_k_array[0:][0][NG_index])
            D_index = find_nearest(D_m_k_array[1:][0], mag_K[i][j])[0]
            D_K_mass.append(D_m_k_array[0:][0][D_index])
            
            if K_mass[j] <= M_cutoff:
                fix_K_mass.append(NG_m_k_array[0:][0][NG_index])
            if K_mass[j] > M_cutoff:
                fix_K_mass.append(m_k_array[0:][0][index])
            

        fix_K_m_array.append(fix_K_mass)

    '''
    # The following is code to find the corresponding mass values from the primary flux.
    K_mass = []; K_m_array = []
    NG_K_mass = []; NG_K_array = []
    D_K_mass = []; D_K_array = []
    
    fix_max_mass = []; fix_max_m_array = []; M_cutoff = 0.5
    for i in range(0, len(max_flux)):
        K_mass = []; NG_K_mass = []; D_K_mass = []; fix_K_mass = [];
        
        index = find_nearest(m_k_array[1:][0], max_flux[i])[0]
        K_mass = m_k_array[0:][0][index]
        NG_index = find_nearest(NG_m_k_array[1:][0], max_flux[i])[0]
        NG_K_mass = NG_m_k_array[0:][0][NG_index]
        D_index = find_nearest(D_m_k_array[1:][0], max_flux[i])[0]
        D_K_mass = D_m_k_array[0:][0][D_index]
        
        if K_mass <= M_cutoff:
            fix_max_mass.append(NG_m_k_array[0:][0][NG_index])
        if K_mass > M_cutoff:
            fix_max_mass.append(m_k_array[0:][0][index])
            
        #print len(K_mass)
        
        K_m_array.append(K_mass)
        NG_K_array.append(NG_K_mass)
        D_K_array.append(D_K_mass)
        
        fix_max_m_array.append(fix_max_mass)
    print 'len max_mass:', len(fix_max_m_array)
    '''
    
    '''
    fix_K_mass = []
    for i in range(len(K_mass)):
        if K_mass[i] <= M_cutoff:
            fix_K_mass.append(NG_K_mass[i])
        if K_mass[i] > M_cutoff:
            fix_K_mass.append(K_mass[i])
    '''
    

    #print "K MASS ARRAY:", fix_K_m_array
    if bs_choice == 's' or bs_choice == 'S':
        print "\nSaving single mass data for Cluster "+cluster+"..."
        np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/Recalculations/'+cluster+'_sin_mass_data',
        star_name = star_name, ang_sep=ang_sep, mag_K=data['mag_K'], K_mass=fix_K_m_array)
        print "Save data complete!"
    
    if bs_choice == 'b' or bs_choice == 'B':
        print "\nSaving binary mass data for Cluster "+cluster+"..."
        np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_bin_mass_data',
        star_name = star_name, ang_sep=ang_sep, mag_K=data['mag_K'], K_mass=fix_K_m_array)
        print "Save data complete!"
    
    
    
    # Re-execute program.
    print("\n=====================================================================")
    again = raw_input("Run d_limit_mass.py again? (y/n): ")
    while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
        again = raw_input("Please enter (y/n): ")
    if again == 'Y' or again == 'y':
        print("\n=====================================================================")
        os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/d_limit_mass.py")
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