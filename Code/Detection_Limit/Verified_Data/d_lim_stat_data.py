#!/usr/bin/env python

import numpy as np

# This list is for stars with a bad reduction status.
reduction_list = ['M182', 'M284']

# This list is for stars w/ no J or H photometry.
JH_list = ['M317 a', 'M317 b', 'M409', 'M49 a', 'M49 b', 'W13', 'W17', 'B1']

# This list is for stars with J band as a lower limit.
upper_lim_list = ['M56 a', 'M141-2 a', 'R110']

# This list is for companion stars with std/avg values > 0.1
std_avg_list = ['R84 b', 'B62']

# This list is for companion stars with stat. arg. values < 0.95
stat_arg_list = ['M56 a', 'M42', 'M86 c', 'M162', 'M47 a', 'M278', 'M50', 'M317 a', 'M317 b', 'M409',
    'M49 a', 'M49 b', 'M665', 'R90', 'R97', 'W17', 'W24 / R81 a', 'W24 / R81 b', 'W25 a', 'W25 b', 'W25 c']


bin_names = open('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/bin_names.txt', 'r').readlines()
bin_delta_K = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/bin_delta_K.txt')
bin_absK = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/bin_absK.txt')
bin_mass_K = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/bin_mass_K.txt')
bin_sep = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/bin_sep.txt')

comp_names = []
for i in range(len(bin_names)):
    comp_names.append(bin_names[i].rstrip('\n'))
    
comp_delta_K = bin_delta_K[0::2]
comp_absK = bin_absK[1::2]
comp_m_ratio = bin_mass_K[1::2]/bin_mass_K[0::2]
comp_sep = bin_sep[0::2]


data_1 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/IC_2391_data.npz')
data_2 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/NGC_6475_data.npz')
data_3 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/NGC_2451_data.npz')
data_4 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/NGC_2516_data.npz')
data_5 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/NGC_3532_data.npz')
data_6 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Verified_Data/IC_2602_data.npz')

star_name_1 = data_1['star_name']
star_name_2 = data_2['star_name']
star_name_3 = data_3['star_name']
#star_name_4 = data_4['star_name']
star_name_5 = data_5['star_name']
star_name_6 = data_6['star_name']
star_name = np.concatenate((star_name_1, star_name_2, star_name_3, star_name_5, star_name_6))

s_star_name_1 = data_1['s_star_name']
s_star_name_2 = data_2['s_star_name']
s_star_name_3 = data_3['s_star_name']
s_star_name_4 = data_4['s_star_name']
s_star_name_5 = data_5['s_star_name']
s_star_name_6 = data_6['s_star_name']
s_star_name = np.concatenate((s_star_name_1, s_star_name_2, s_star_name_3, s_star_name_4, s_star_name_5, s_star_name_6))

ang_sep_1 = data_1['ang_sep']
ang_sep_2 = data_2['ang_sep']
ang_sep_3 = data_3['ang_sep']
#ang_sep_4 = data_4['ang_sep']
ang_sep_5 = data_5['ang_sep']
ang_sep_6 = data_6['ang_sep']
ang_sep = np.concatenate((ang_sep_1, ang_sep_2, ang_sep_3, ang_sep_5, ang_sep_6))

s_ang_sep_1 = data_1['s_ang_sep']
s_ang_sep_2 = data_2['s_ang_sep']
s_ang_sep_3 = data_3['s_ang_sep']
s_ang_sep_4 = data_4['s_ang_sep']
s_ang_sep_5 = data_5['s_ang_sep']
s_ang_sep_6 = data_6['s_ang_sep']
s_ang_sep = np.concatenate((s_ang_sep_1, s_ang_sep_2, s_ang_sep_3, s_ang_sep_4, s_ang_sep_5, s_ang_sep_6))

mass_ratio_1 = data_1['mass_ratio']
mass_ratio_2 = data_2['mass_ratio']
mass_ratio_3 = data_3['mass_ratio']
#mass_ratio_4 = data_4['mass_ratio']
mass_ratio_5 = data_5['mass_ratio']
mass_ratio_6 = data_6['mass_ratio']
mass_ratio = np.concatenate((mass_ratio_1, mass_ratio_2, mass_ratio_3, mass_ratio_5, mass_ratio_6))

s_mass_ratio_1 = data_1['s_mass_ratio']
s_mass_ratio_2 = data_2['s_mass_ratio']
s_mass_ratio_3 = data_3['s_mass_ratio']
s_mass_ratio_4 = data_4['s_mass_ratio']
s_mass_ratio_5 = data_5['s_mass_ratio']
s_mass_ratio_6 = data_6['s_mass_ratio']
s_mass_ratio = np.concatenate((s_mass_ratio_1, s_mass_ratio_2, s_mass_ratio_3, s_mass_ratio_4, s_mass_ratio_5, s_mass_ratio_6))

mag_K_1 = data_1['mag_K']
mag_K_2 = data_2['mag_K']
mag_K_3 = data_3['mag_K']
#mag_K_4 = data_4['mag_K']
mag_K_5 = data_5['mag_K']
mag_K_6 = data_6['mag_K']
mag_K = np.concatenate((mag_K_1, mag_K_2, mag_K_3, mag_K_5, mag_K_6))

s_mag_K_1 = data_1['s_mag_K']
s_mag_K_2 = data_2['s_mag_K']
s_mag_K_3 = data_3['s_mag_K']
s_mag_K_4 = data_4['s_mag_K']
s_mag_K_5 = data_5['s_mag_K']
s_mag_K_6 = data_6['s_mag_K']
s_mag_K = np.concatenate((s_mag_K_1, s_mag_K_2, s_mag_K_3, s_mag_K_4, s_mag_K_5, s_mag_K_6))


final_names = np.concatenate((star_name, s_star_name))
final_ang_sep = np.concatenate((ang_sep, s_ang_sep))
final_m_ratio = np.concatenate((mass_ratio, s_mass_ratio))
final_mag_K = np.concatenate((mag_K, s_mag_K))