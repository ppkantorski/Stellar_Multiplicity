#!/usr/bin/env python

# ========================================================================== #
# File: plot_d_lim.py                                                        #
# Programmer: Patrick Kantorski                                              #
# Date: 01/27/15                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to plot previously saved   #
#              detection limits data.                                        #
# ========================================================================== #

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

choice = raw_input("\nEnter specified cluster: ")
if choice == '1':
    cluster = "IC_2391"
    lower_x = .9
    upper_x = 1.1
    lower_y = 5.2
    upper_y = 5.7
if choice == '2':
    cluster = "NGC_6475"
    lower_x = 1
    upper_x = 2
    lower_y = 3
    upper_y = 4
if choice == '3':
    cluster = "NGC_2451"
    lower_x = 1.4
    upper_x = 1.5
    lower_y = 6
    upper_y = 7
if choice == '4':
    cluster = "NGC_2516"
    lower_x = 1.2
    upper_x = 1.5
    lower_y = 5
    upper_y = 6
if choice == '5':
    cluster = "NGC_3532"
    lower_x = 1.3
    upper_x = 1.5
    lower_y = 5
    upper_y = 6
if choice == '6':
    cluster = "IC_2602"
    lower_x = 1.2
    upper_x = 1.4
    lower_y = 5
    upper_y = 5.4
    
try:
    data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/'+cluster+'_sin_data.npz')

except IOError:
    print "Files for cluster", cluster, "does not exist!\n"
    sys.exit()

star_name = data['star_name']
ang_sep = data['ang_sep']
mag_K = data['mag_K']

i = 0; fixed_star_name = []; fixed_ang_sep = []; fixed_mag_K = []
while i < len(star_name) - 1:
    temp_name = star_name[i]
    temp_index = i
    #plt.plot(ang_sep[i], mag_K[i], color='r')
    median_1 = np.median(mag_K[i][20:137])
    if star_name[temp_index+1] == '':
        #plt.plot(ang_sep[i+1], mag_K[i+1], color='b')
        median_2 = np.median(mag_K[i+1][20:137])
        try:
            if star_name[temp_index+2] == '':
                #plt.plot(ang_sep[i+2], mag_K[i+2], color='g')
                i = i + 2
                median_3 = np.median(mag_K[i+2][20:137])
            elif star_name[temp_index+2] != '':
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
    if median_2 > median_1 and median_2 > median_3:
        print str(star_name[temp_index])+": Image 2 is best."
        fixed_star_name.append(star_name[temp_index])
        fixed_ang_sep.append(ang_sep[temp_index+1])
        fixed_mag_K.append(mag_K[temp_index+1])
    if median_3 > median_1 and median_3 > median_2:
        print str(star_name[temp_index])+": Image 3 is best."
        fixed_star_name.append(star_name[temp_index])
        fixed_ang_sep.append(ang_sep[temp_index+2])
        fixed_mag_K.append(mag_K[temp_index+2])
    #a = raw_input("Break function or next star? :")
    
    print i
    print "\nSaving sorted/fixed data..."
    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/fixed_'+cluster+'_sin_data',
    star_name = fixed_star_name, ang_sep=fixed_ang_sep, mag_K=fixed_mag_K)
    print "Save data complete!"


# Loading saved sorted/fixed data...
data = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/fixed_'+cluster+'_sin_data.npz')
star_name = data['star_name']
ang_sep = data['ang_sep']
mag_K = data['mag_K']



for i in range(len(ang_sep)):
    for j in range(len(ang_sep[i])):
        if ang_sep[i][j] > lower_x and ang_sep[i][j] < upper_x:
            if mag_K[i][j] > lower_y and mag_K[i][j] < upper_y:
                print "\nPossible Bad Star #"+str(i)+":", star_name[i]

print "Plotting data for Cluster "+cluster+"..."
plt.title("Detection Limit for Singles in "+cluster, fontsize='20')
plt.xlabel("Angular Seperation", fontsize='16')
plt.ylabel("Mag K", fontsize='16')
plt.xscale('log')
plt.gca().invert_yaxis()
for i in range(len(ang_sep)):
    plt.plot(ang_sep[i], mag_K[i], 'o', color='0.3')

print "Saving figure..."
plt.savefig('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/'+cluster+'.png')    
plt.show()


# Re-execute program.
print("\n=====================================================================")
again = raw_input("Run program again? (y/n): ")
while again != 'y' and again != 'Y' and again != 'N' and again != 'n': 
    again = raw_input("Please enter (y/n): ")
if again == 'Y' or again == 'y':
    os.system('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/plot_d_lim_sin.py')
elif again == 'N' or again == 'n':
    print('\nAll process are complete!')