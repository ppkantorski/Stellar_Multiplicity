#!/usr/bin/env python

# ========================================================================== #
# File: plot_d_lim.py                                                        #
# Programmer: Patrick Kantorski                                              #
# Date: 01/27/15                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to plot previously saved   #
#              detection limits data.  Be sure to run 'd_limit_mass.py' and  #
#              'd_lim_calc.py' first!                                        #
# ========================================================================== #

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

choice = raw_input("\nEnter specified cluster: ")
if choice == '1':
    cluster = "IC_2391"
    start = 0
    stop = 13 + 1
    s_start = 0
    s_stop = 19 + 1
    
    lower_x = .9
    upper_x = 1.1
    lower_y = 5.2
    upper_y = 5.7

if choice == '2':
    cluster = "NGC_6475"
    start = 14
    stop = 23 + 1
    s_start = 20
    s_stop = 22 + 1
    
    lower_x = 1
    upper_x = 2
    lower_y = 3
    upper_y = 4
    
if choice == '3':
    cluster = "NGC_2451"
    start = 24
    stop = 49 + 1
    s_start = 23
    s_stop = 50 + 1
    
    lower_x = 1.4
    upper_x = 1.5
    lower_y = 6
    upper_y = 7
    
if choice == '4':
    cluster = "NGC_2516"
    start = 0
    stop = 0
    s_start = 51
    s_stop = 74 + 1
    
    lower_x = 1.2
    upper_x = 1.5
    lower_y = 5
    upper_y = 6
    
    ## This was placed here as a dummy index so that choice 5 is used as dummy data for this empty binary dataset.
    #start = 50
    #stop = 67 + 1
    
if choice == '5':
    cluster = "NGC_3532"
    start = 50
    stop = 67 + 1
    s_start = 75
    s_stop = 89 + 1
    
    lower_x = 1.3
    upper_x = 1.5
    lower_y = 5
    upper_y = 6
if choice == '6':
    cluster = "IC_2602"
    start = 68
    stop = 107 + 1
    s_start = 90
    s_stop = 112 + 1
    
    lower_x = 1.2
    upper_x = 1.4
    lower_y = 5
    upper_y = 5.4

try:
    # Loading another dataset as dummy data for the NGC 2516 detection limit so that I dont have to rewrite code...
    #data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/NGC_3532_bin_data.npz')
    
    # Data is rewritten as the correct cluster if selection is not NGC 2516
    if cluster != "NGC_2516":
        data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_bin_mass_data.npz')
    s_data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/Recalculations/'+cluster+'_sin_mass_data.npz')


except IOError:
    print "Files for cluster", cluster, "does not exist!\n"
    sys.exit()


########################################### BINARY STAR SECTION #################################################

# Loading Binary Star Data...
if cluster != "NGC_2516":
    star_name = data['star_name']
    print star_name
    ang_sep = data['ang_sep']
    mag_K = data['mag_K']
    K_mass = data['K_mass']
    max_mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/primary_mass.txt')
    
    
    #print 'mag_K length/shape:', len(mag_K), mag_K.shape
    print 'K_mass length/shape:', len(K_mass), K_mass.shape
    
    
    i = 0; fixed_star_name = []; fixed_ang_sep = []; fixed_mag_K = []; fixed_K_mass = [];
    while i < len(star_name) - 1:
        temp_name = star_name[i]
        temp_index = i
        #plt.plot(ang_sep[i], mag_K[i], color='r')
        median_1 = np.median(mag_K[i][50:80])
        if star_name[temp_index+1] == star_name[temp_index]:
            #plt.plot(ang_sep[i+1], mag_K[i+1], color='b')
            median_2 = np.median(mag_K[i+1][50:80])
            median_3 = 0
            try:
                if star_name[temp_index+2] == star_name[temp_index]:
                    #plt.plot(ang_sep[i+2], mag_K[i+2], color='g')
                    i = i + 2
                    median_3 = np.median(mag_K[i+2][50:80])
                elif star_name[temp_index+2] != star_name[temp_index]:
                    median_3 = 0
                    i = i + 1
            except IndexError:
                i = len(star_name)
        i = i + 1
        #plt.title("Detection Limit for "+str(temp_name), fontsize='20')
        #plt.xscale('log')
        #plt.gca().invert_yaxis()
        #plt.show()
        
        if median_1 > median_2 and median_1 > median_3:
            print str(star_name[temp_index])+": Image 1 is best."
            fixed_star_name.append(star_name[temp_index])
            fixed_ang_sep.append(ang_sep[temp_index])
            fixed_mag_K.append(mag_K[temp_index])
            fixed_K_mass.append(K_mass[temp_index])
        if median_2 > median_1 and median_2 > median_3:
            print str(star_name[temp_index])+": Image 2 is best."
            fixed_star_name.append(star_name[temp_index])
            fixed_ang_sep.append(ang_sep[temp_index+1])
            fixed_mag_K.append(mag_K[temp_index+1])
            fixed_K_mass.append(K_mass[temp_index+1])
        if median_3 > median_1 and median_3 > median_2:
            print str(star_name[temp_index])+": Image 3 is best."
            fixed_star_name.append(star_name[temp_index])
            fixed_ang_sep.append(ang_sep[temp_index+2])
            fixed_mag_K.append(mag_K[temp_index+2])
            fixed_K_mass.append(K_mass[temp_index+2])
        #a = raw_input("Break function or next star? :")
        
        print i
        print "\nSaving sorted/fixed data..."
        np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/fixed_'+cluster+'_data',
        star_name = fixed_star_name, ang_sep=fixed_ang_sep, mag_K=fixed_mag_K, K_mass=fixed_K_mass)
        print "Save data complete!\n"
    
    
    # Loading saved sorted/fixed data...
    data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/fixed_'+cluster+'_data.npz')
    star_name = data['star_name']
    ang_sep = data['ang_sep']
    mag_K = data['mag_K']
    K_mass = data['K_mass']
    
    
    #print 'mag_K length/shape:', len(mag_K[0]), mag_K.shape
    #print 'K_mass length/shape:', len(K_mass[0]), K_mass.shape
    
    for i in range(len(ang_sep)):
        for j in range(len(ang_sep[i])):
            if ang_sep[i][j] > lower_x and ang_sep[i][j] < upper_x:
                if mag_K[i][j] > lower_y and mag_K[i][j] < upper_y:
                    print "\nPossible Bad Star #"+str(i)+":", star_name[i]
    
    
    plt.figure(1)
    print "Plotting data for Cluster "+cluster+"..."
    plt.title("Detection Limit for Binaries in "+cluster, fontsize='20')
    plt.xlabel("Angular Seperation", fontsize='16')
    plt.ylabel("Mag K", fontsize='16')
    plt.xscale('log')
    plt.gca().invert_yaxis()
    for i in range(len(ang_sep)):
        plt.plot(ang_sep[i], mag_K[i], '-')
    
    
    #print "Saving figure..."
    #plt.savefig('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_mag_K.png')    
    #plt.show()



########################################### SINGLE STAR SECTION ###############################################

# Loading Single Star Data..
s_star_name = s_data['star_name']
print "SINGLE STAR NAME:", s_star_name
s_ang_sep = s_data['ang_sep']
s_mag_K = s_data['mag_K']
s_K_mass = s_data['K_mass']

s_max_mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/primary_mass.txt')

#print 's_mag_K length/shape:', len(s_mag_K), s_mag_K.shape
print 's_K_mass length/shape:', len(s_K_mass), s_K_mass.shape


i = 0; fixed_s_star_name = []; fixed_s_ang_sep = []; fixed_s_mag_K = []; fixed_s_K_mass = [];
while i < len(s_star_name) - 1:
    temp_name = s_star_name[i]
    temp_index = i
    #plt.plot(s_ang_sep[i], s_mag_K[i], color='r')
    median_1 = np.median(s_mag_K[i][20:137])
    median_2 = 0
    median_3 = 0

    if s_star_name[temp_index+1] == s_star_name[temp_index]:
        #plt.plot(s_ang_sep[i+1], s_mag_K[i+1], color='b')
        median_2 = np.median(s_mag_K[i+1][20:137])
        try:
            if s_star_name[temp_index+2] == s_star_name[temp_index]:
                #plt.plot(s_ang_sep[i+2], s_mag_K[i+2], color='g')
                i = i + 2
                median_3 = np.median(s_mag_K[i+2][20:137])
            elif s_star_name[temp_index+2] != s_star_name[temp_index]:
                median_3 = 0
                i = i + 1
        except IndexError:
            i = len(s_star_name)
    i = i + 1
    #plt.title("Detection Limit for "+str(temp_name), fontsize='20')
    #plt.xscale('log')
    #plt.gca().invert_yaxis()
    #plt.show()
    
    
    if median_1 > median_2 and median_1 > median_3:
        print str(s_star_name[temp_index])+": Image 1 is best."
        fixed_s_star_name.append(s_star_name[temp_index])
        fixed_s_ang_sep.append(s_ang_sep[temp_index])
        fixed_s_mag_K.append(s_mag_K[temp_index])
        fixed_s_K_mass.append(s_K_mass[temp_index])
    if median_2 > median_1 and median_2 > median_3:
        print str(s_star_name[temp_index])+": Image 2 is best."
        fixed_s_star_name.append(s_star_name[temp_index])
        fixed_s_ang_sep.append(s_ang_sep[temp_index+1])
        fixed_s_mag_K.append(s_mag_K[temp_index+1])
        fixed_s_K_mass.append(s_K_mass[temp_index+1])
    if median_3 > median_1 and median_3 > median_2:
        print str(s_star_name[temp_index])+": Image 3 is best."
        fixed_s_star_name.append(s_star_name[temp_index])
        fixed_s_ang_sep.append(s_ang_sep[temp_index+2])
        fixed_s_mag_K.append(s_mag_K[temp_index+2])
        fixed_s_K_mass.append(s_K_mass[temp_index+2])
    #a = raw_input("Break function or next star? :")
    
    print i
    print "\nSaving sorted/fixed data..."
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/Recalculations/fixed_'+cluster+'_data',
    star_name = fixed_s_star_name, ang_sep=fixed_s_ang_sep, mag_K=fixed_s_mag_K, K_mass=fixed_s_K_mass)
    print "Save data complete!\n"


# Loading saved sorted/fixed data...
s_data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/Recalculations/fixed_'+cluster+'_data.npz')
s_star_name = s_data['star_name']
s_ang_sep = s_data['ang_sep']
s_mag_K = s_data['mag_K']
s_K_mass = s_data['K_mass']


#print 's_mag_K length/shape:', len(s_mag_K[0]), s_mag_K.shape
#print 's_K_mass length/shape:', len(s_K_mass[0]), s_K_mass.shape

#for i in range(len(s_ang_sep)):
#    for j in range(len(s_ang_sep[i])):
#        if s_ang_sep[i][j] > lower_x and s_ang_sep[i][j] < upper_x:
#            if s_mag_K[i][j] > lower_y and s_mag_K[i][j] < upper_y:
#                print "\nPossible Bad Star #"+str(i)+":", s_star_name[i]



plt.figure(2)
print "Plotting data for Cluster "+cluster+"..."
plt.title("Detection Limit for Singles in "+cluster, fontsize='20')
plt.xlabel("Angular Seperation", fontsize='16')
plt.ylabel("Mag K", fontsize='16')
plt.xscale('log')
plt.gca().invert_yaxis()
for i in range(len(s_ang_sep)):
    plt.plot(s_ang_sep[i], s_mag_K[i])

#print "Saving figure..."
#plt.savefig('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_mag_K.png')    
plt.show()



##################################### PLOTTING BOTH SINGLES AND BINARIES SECTION ##########################################




plt.figure(3)
print "Plotting mass data for Cluster "+cluster+"..."
plt.title("Detection Limit for "+cluster, fontsize='20')
plt.xlabel("Angular Seperation", fontsize='16')
plt.ylabel("Mass Ratio", fontsize='16')
plt.xscale('log')
#plt.gca().invert_yaxis()

#print 'K_mass', K_mass

if cluster != "NGC_2516":
    # BINARY CALCULATION #
    final_mass = []
    print 'max_mass', max_mass[start:stop][0::2]; i = 0
    while i < len(max_mass[start:stop][0::2]):
        final_mass.append(max_mass[start:stop][0::2][i])
        #print final_mass
        try:
            if max_mass[start:stop][0::2][i] == max_mass[start:stop][0::2][i+1]:
                i = i+1
            if max_mass[start:stop][0::2][i] == max_mass[start:stop][0::2][i+1]:
                i = i+1
        except IndexError:
            a = 'blah'
        i = i + 1
    
    #print 'Final Mass', final_mass

# SINGLE CALCULATION #
s_final_mass = []
#print 's_max_mass', s_max_mass[s_start:s_stop];
i = 0
while i < len(s_max_mass[s_start:s_stop]):
    s_final_mass.append(s_max_mass[s_start:s_stop][i])
    #print final_mass
    try:
        if s_max_mass[s_start:s_stop][i] == s_max_mass[s_start:s_stop][i+1]:
            i = i+1
        if s_max_mass[s_start:s_stop][i] == s_max_mass[s_start:s_stop][i+1]:
            i = i+1
    except IndexError:
        a = 'blah'
    i = i + 1

#print 'Single Final Mass:', s_final_mass
#print 'Single K Mass:', len(s_K_mass)

#print 'star name length:', len(star_name)
#print 'max mass length:', len(max_mass[start:stop][0::2])
#print 'star name:', star_name
#print 'max mass:', max_mass[start:stop][0::2]

# Plot binary data only if the cluster selected is NOT NGC 2516

mass_ratio=[]; final_ang_sep=[]; final_mag_K=[];
if cluster != "NGC_2516":
    for i in range(len(ang_sep)):
        #if ang_sep[i][0]==0:
        #    del ang_sep[i][0]
        #    del K_mass[i][0]
        #    del final_mass[i][0]
        #if ang_sep[i][0]!=0:
        if star_name[i] == 'M291-K_Kfinal':
            print "caught the outlier.."
        if star_name[i] != 'M291-K_Kfinal':
            final_mag_K.append(mag_K[i])
            final_ang_sep.append(ang_sep[i])
            mass_ratio.append(K_mass[i]/final_mass[i])
            plt.plot(ang_sep[i], K_mass[i]/final_mass[i], '-', label=star_name[i])
        for j in range(len(ang_sep[i])):
            if j == 1:
                if (K_mass[i]/final_mass[i])[j] > 1.4:
                    print 'Binary: Bad Star above 1.4!! :', star_name[i]
                    #print 'Binary: Mass value:', max_mass[start:stop][0::2][i]
                if (K_mass[i]/final_mass[i])[j] < 0.75:
                    print 'Binary: Bad Star below 0.75!! :', star_name[i]
                    #print 'Binary: Mass value:', max_mass[start:stop][0::2][i]


#print 'single star name length:', len(s_star_name)
#print 'single max mass length:', len(s_max_mass[s_start:s_stop])
#print 'single star name:', s_star_name
#print 'single max mass:', s_max_mass[s_start:s_stop]

s_mass_ratio=[]; final_s_ang_sep=[]; final_s_mag_K=[]
for i in range(len(s_ang_sep)):
    #if s_ang_sep[i][0]==0:
    #    del s_ang_sep[i][0]
    #    del s_K_mass[i][0]
    #    del s_final_mass[i][0]
    #if s_ang_sep[i][0]!=0:
    final_s_mag_K.append(s_mag_K[i])
    final_s_ang_sep.append(s_ang_sep[i])
    s_mass_ratio.append(s_K_mass[i]/s_final_mass[i])
    plt.plot(s_ang_sep[i], s_K_mass[i]/s_final_mass[i], '-', label=s_star_name[i])
    for j in range(len(s_ang_sep[i])):
        if j == 1:
            if (s_K_mass[i]/s_final_mass[i])[j] > 1.4:
                print 'Single: Bad Star above 1.4!! :', s_star_name[i]
                #print 'Binary: Mass value:', max_mass[start:stop][0::2][i]
            if (s_K_mass[i]/s_final_mass[i])[j] < 0.75:
                print 'Single: Bad Star below 0.75!! :', s_star_name[i]
                #print 'Binary: Mass value:', max_mass[start:stop][0::2][i]
            

print "Saving figure..."
#plt.legend()
#n
plt.xlim(0.1, 10)
plt.savefig('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/'+cluster+'_mass_K.png')
plt.show()

#mass_ratio = K_mass/final_mass
#s_mass_ratio = s_K_mass/s_final_mass

print "\nSaving data for Cluster "+cluster+"..."
if cluster != "NGC_2516":
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/'+cluster+'_data',
    star_name = star_name, ang_sep=final_ang_sep, mass_ratio=mass_ratio, mag_K=final_mag_K,
    s_star_name=s_star_name, s_ang_sep=final_s_ang_sep, s_mass_ratio=s_mass_ratio, s_mag_K=final_s_mag_K)
if cluster == "NGC_2516":
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/'+cluster+'_data',
    s_star_name=s_star_name, s_ang_sep=final_s_ang_sep, s_mass_ratio=s_mass_ratio, s_mag_K=final_s_mag_K)
    
print "Save data complete!"


# Re-execute program.
print("\n=====================================================================")
again = raw_input("Run program again? (y/n): ")
while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
    again = raw_input("Please enter (y/n): ")
if again == 'Y' or again == 'y':
    os.system('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/plot_d_lim.py')
elif again == 'N' or again == 'n':
    print('\nAll process are complete!')