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
    
if choice == '5':
    cluster = "NGC_3532"
    start = 50
    stop = 67 + 1
    s_start = 75
    s_stop = 91 + 1
    
    lower_x = 1.3
    upper_x = 1.5
    lower_y = 5
    upper_y = 6
if choice == '6':
    cluster = "IC_2602"
    start = 68
    stop = 107 + 1
    s_start = 92
    s_stop = 114 + 1
    
    lower_x = 1.2
    upper_x = 1.4
    lower_y = 5
    upper_y = 5.4

try:
    #data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_bin_data.npz')
    data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_bin_mass_data.npz')

except IOError:
    print "Files for cluster", cluster, "does not exist!\n"
    sys.exit()

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
    median_1 = np.median(mag_K[i][20:137])
    if star_name[temp_index+1] == star_name[temp_index]:
        #plt.plot(ang_sep[i+1], mag_K[i+1], color='b')
        median_2 = np.median(mag_K[i+1][20:137])
        median_3 = 0
        try:
            if star_name[temp_index+2] == star_name[temp_index]:
                #plt.plot(ang_sep[i+2], mag_K[i+2], color='g')
                i = i + 2
                median_3 = np.median(mag_K[i+2][20:137])
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
    plt.plot(ang_sep[i], mag_K[i], 'o', color='0.3')

print "Saving figure..."
plt.savefig('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_mag_K.png')    
plt.show()


plt.figure(2)
print "Plotting mass data for Cluster "+cluster+"..."
plt.title("Detection Limit for Binaries in "+cluster, fontsize='20')
plt.xlabel("Angular Seperation", fontsize='16')
plt.ylabel("Mass Ratio", fontsize='16')
plt.xscale('log')
#plt.gca().invert_yaxis()

#print 'K_mass', K_mass
final_mass = []
print 'max_mass', max_mass[start:stop][0::2]; i = 0
while i < len(max_mass[start:stop][0::2]):
    final_mass.append(max_mass[start:stop][0::2][i])
    print final_mass
    try:
        if max_mass[start:stop][0::2][i] == max_mass[start:stop][0::2][i+1]:
            i = i+1
        if max_mass[start:stop][0::2][i] == max_mass[start:stop][0::2][i+1]:
            i = i+1
    except IndexError:
        a = 'blah'
    i = i + 1

for i in range(len(ang_sep)):
    print final_mass[i]
    plt.plot(ang_sep[i], K_mass[i]/max_mass[start:stop][0::2][i], 'o', color='0.3') # I BELIEVE THAT THE FLAW IN MY CODE IS HERE../max_mass[start:stop][i]

print "Saving figure..."
plt.savefig('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_mass_K.png')    
plt.show()



# Re-execute program.
print("\n=====================================================================")
again = raw_input("Run program again? (y/n): ")
while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
    again = raw_input("Please enter (y/n): ")
if again == 'Y' or again == 'y':
    os.system('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/plot_d_lim_bin.py')
elif again == 'N' or again == 'n':
    print('\nAll process are complete!')