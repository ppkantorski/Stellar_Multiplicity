#!/usr/bin/env python

import numpy as np
import pylab as plt
import os
import sys
from d_lim_stat_data import *

def main():

    plt.rcParams['figure.figsize'] = 14, 7
    plt.suptitle("Detection Limit for All Clusters", fontsize='20')
    for i in range(len(final_ang_sep)):
        # I believe his line was to treat some weird offset.
        if final_names[i]=='M88' or final_names[i]=='M131' or final_names[i]=='M239':
            final_ang_sep[i] = np.delete(final_ang_sep[i], 0)
            final_m_ratio[i] = np.delete(final_m_ratio[i], 0)
            final_mag_K[i] = np.delete(final_mag_K[i], 0)
        
        final_ang_sep[i] = np.delete(final_ang_sep[i], 0)
        final_m_ratio[i] = np.delete(final_m_ratio[i], 0)
        final_mag_K[i] = np.delete(final_mag_K[i], 0)
        
        plt.subplot(121)
        plt.gca().invert_yaxis()
        plt.xscale('log')
        plt.xlim(0.09, 10)
        plt.xlabel("Angular Seperation", fontsize='16')
        plt.ylabel("Delta K", fontsize='16')
        plt.plot(final_ang_sep[i], final_mag_K[i], '-', label=final_names[i])

        
        plt.subplot(122)
        plt.xscale('log')
        plt.xlim(0.09, 10)
        plt.xlabel("Angular Seperation", fontsize='16')
        plt.ylabel("Mass Ratio", fontsize='16')
        plt.plot(final_ang_sep[i], final_m_ratio[i], '-', label=final_names[i])

    #plt.show()
    plt.clf()
    
    # This line is for catching the stars that stangely have an ang sep of 0..
    for i in range(len(final_ang_sep)):
        if final_ang_sep[i][0] == 0:
            print star_name[i]
    
    
    #print zip(*final_ang_sep)[0]
    
    
    mag_K_std = []; mag_K_median = [];
    mag_K_16 = []; mag_K_84 = []; mag_K_2_5 = []; mag_K_97_5 = []
    
    mass_std = []; mass_median = [];
    mass_16 = []; mass_84 = []; mass_2_5 = []; mass_97_5 = []
    
    for i in range(len(zip(*final_ang_sep))):
        
        sorted_ang_sep = np.sort(zip(*final_ang_sep)[i])
        
        
        sorted_mag_K = np.sort(zip(*final_mag_K)[i])
        
        plt.subplot(121)
        #plt.plot(sorted_ang_sep,sorted_mag_K,'.', color='0.5')
        
        #sep_array.append(sorted_x)
        #print sorted_mag_K[0:int(len(sorted_mag_K)*.1)]
        
        mag_K_std.append(np.std(sorted_mag_K))
        mag_K_median.append(np.median(sorted_mag_K))
        mag_K_16.append(sorted_mag_K[int(len(sorted_mag_K)*.16)-1])
        mag_K_84.append(sorted_mag_K[int(len(sorted_mag_K)*.84)-1])
        mag_K_2_5.append(sorted_mag_K[int(len(sorted_mag_K)*.025)-1])
        mag_K_97_5.append(sorted_mag_K[int(len(sorted_mag_K)*.975)-1])
        
        
        sorted_m_ratio =  np.sort(zip(*final_m_ratio)[i])
        
        plt.subplot(122)
        #plt.plot(sorted_ang_sep,sorted_m_ratio,'.', color='0.5')
        
        #sep_array.append(sorted_x)
        mass_std.append(np.std(sorted_m_ratio))
        mass_median.append(np.median(sorted_m_ratio))
        mass_16.append(sorted_m_ratio[int(len(sorted_m_ratio)*.16)-1])
        mass_84.append(sorted_m_ratio[int(len(sorted_m_ratio)*.84)-1])
        mass_2_5.append(sorted_m_ratio[int(len(sorted_m_ratio)*.025)-1])
        mass_97_5.append(sorted_m_ratio[int(len(sorted_m_ratio)*.975)-1])
        
        
        
    ## The following code is for plotting the boundaries.. ##
    
    seperation = np.array(zip(*final_ang_sep))[:,0]
    
    plt.rcParams['figure.figsize'] = 14, 7
    plt.suptitle("Detection Limit for All Clusters", fontsize='20')
    
    plt.subplot(121)
    plt.gca().invert_yaxis()
    plt.xscale('log')
    plt.xlim(0.09, 6)
    plt.xlabel("Angular Seperation", fontsize='16')
    plt.ylabel("Delta K", fontsize='16')
    
    
    #print len(comp_sep), len(comp_names)
    for i in range(len(comp_sep)):
        #if comp_names[i] in reduction_list:
        #    plt.plot(comp_sep[i], comp_delta_K[i], 's', color='r')
        if comp_names[i] not in std_avg_list and comp_names[i] not in stat_arg_list and comp_names[i] in JH_list:
            plt.plot(comp_sep[i], comp_delta_K[i], 'o', color='w')
        #elif comp_names[i] in std_avg_list and comp_names[i] not in stat_arg_list and comp_names[i] in JH_list:
        #    plt.plot(comp_sep[i], comp_delta_K[i], '<', color='w')
        #elif comp_names[i] not in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] in JH_list:
        #    plt.plot(comp_sep[i], comp_delta_K[i], '>', color='w')
        #elif comp_names[i] in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] in JH_list:
        #    plt.plot(comp_sep[i], comp_delta_K[i], 'v', color='w')
        elif comp_names[i] in std_avg_list and comp_names[i] not in stat_arg_list and comp_names[i] not in JH_list:
            if comp_delta_K[i] < 4.5 and comp_sep[i] < 2:
                print "Below 4.5 delK & below 2 arcsec:", comp_names[i]
            plt.plot(comp_sep[i], comp_delta_K[i], '<', color='r')
        elif comp_names[i] not in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] not in JH_list:
            plt.plot(comp_sep[i], comp_delta_K[i], '>', color='r')
        elif comp_names[i] in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] not in JH_list:
            plt.plot(comp_sep[i], comp_delta_K[i], 'v', color='m')
        else:
            plt.plot(comp_sep[i], comp_delta_K[i], 'o', color='b')
    
    plt.plot(seperation, np.array(mag_K_median), '-', color='k', linewidth=2, label='median')
    plt.plot(seperation, np.array(mag_K_16), '--', color='0.7', linewidth=2, label='16%')
    plt.plot(seperation, np.array(mag_K_84), '--', color='0.7', linewidth=2, label='84%')
    plt.plot(seperation, np.array(mag_K_2_5), '--', color='0.4', linewidth=2, label='2.5%')
    plt.plot(seperation, np.array(mag_K_97_5), '--', color='0.4', linewidth=2, label='97.5%')
    #plt.plot(seperation, np.array(mag_K_median)+np.array(mag_K_std), '--', color='g', linewidth=2, label='1'+r'$\sigma$')
    #plt.plot(seperation, np.array(mag_K_median)-np.array(mag_K_std), '--', color='g', linewidth=2)
    #plt.legend()
    
    
    plt.subplot(122)
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(0.09, 6)
    plt.xlabel("Angular Seperation", fontsize='16')
    plt.ylabel("Mass Ratio", fontsize='16')
    
    for i in range(len(comp_sep)):
        #if comp_names[i] in reduction_list:
        #    plt.plot(comp_sep[i], comp_delta_K[i], 's', color='r')
        #if comp_names[i] in upper_lim_list:
        #    plt.plot(comp_sep[i], comp_m_ratio[i], '2', color='k')
        if comp_names[i] not in std_avg_list and comp_names[i] not in stat_arg_list and comp_names[i] in JH_list:
            plt.plot(comp_sep[i], comp_m_ratio[i], 'o', color='w')
        #elif comp_names[i] in std_avg_list and comp_names[i] not in stat_arg_list and comp_names[i] in JH_list:
        #    plt.plot(comp_sep[i], comp_m_ratio[i], '<', color='w')
        #elif comp_names[i] not in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] in JH_list:
        #    plt.plot(comp_sep[i], comp_m_ratio[i], '>', color='w')
        #elif comp_names[i] in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] in JH_list:
        #    plt.plot(comp_sep[i], comp_m_ratio[i], 'v', color='w')
            
        elif comp_names[i] in std_avg_list and comp_names[i] not in stat_arg_list and comp_names[i] not in JH_list:
            #if comp_delta_K[i] < 4.5:
            #    print "Below 4.5 delK:", comp_names[i]
            plt.plot(comp_sep[i], comp_m_ratio[i], '<', color='r')
        elif comp_names[i] not in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] not in JH_list:
            plt.plot(comp_sep[i], comp_m_ratio[i], '>', color='r')
        elif comp_names[i] in std_avg_list and comp_names[i] in stat_arg_list and comp_names[i] not in JH_list :
            plt.plot(comp_sep[i], comp_m_ratio[i], 'v', color='m')
        else:
            plt.plot(comp_sep[i], comp_m_ratio[i], 'o', color='b')

    
    plt.plot(seperation, np.array(mass_median), '-', color='k', linewidth=2, label='median')
    plt.plot(seperation, np.array(mass_16), '--', color='.7', linewidth=2, label='16%')
    plt.plot(seperation, np.array(mass_84), '--', color='.7', linewidth=2, label='84%')
    plt.plot(seperation, np.array(mass_2_5), '--', color='.4', linewidth=2, label='2.5%')
    plt.plot(seperation, np.array(mass_97_5), '--', color='.4', linewidth=2, label='97.5%')
    #plt.plot(seperation, np.array(mass_median)+np.array(mass_std), '--', color='g', linewidth=2, label='1'+r'$\sigma$')
    #plt.plot(seperation, np.array(mass_median)-np.array(mass_std), '--', color='g', linewidth=2)
    #plt.legend()
    plt.show()
    

    
    #print comp_names

    

if __name__ == '__main__':
	main()