#!/usr/bin/env python

import numpy as np

IC_2391_b = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/IR_photometry/ic2391_barrado04.txt')
IC_2391_p = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/IR_photometry/ic2391_platais07.txt')
IC_2602_d = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/IR_photometry/ic2602_dobbie10.txt')
IC_2602_r = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/IR_photometry/ic2602_randich01.txt')
NGC_2451a_b = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Isochron/IR_photometry/ngc2451a_balog09.txt')

data_1 = IC_2391_b
data_2 = IC_2391_p
data_3 = IC_2602_d
data_4 = IC_2602_r
data_5 = NGC_2451a_b

J_1 = data_1[:,0] - (5 * np.log10(145) - 5)
J_2 = data_2[:,0] - (5 * np.log10(145) - 5)
J_3 = data_3[:,0] - (5 * np.log10(149) - 5)
J_4 = data_4[:,0] - (5 * np.log10(149) - 5)
J_5 = data_5[:,0] - (5 * np.log10(184) - 5)
JK_2 = data_2[:,1]

J_IR_photo = []
J_IR_photo.extend(J_1)
#J_IR_photo.extend(J_2)
J_IR_photo.extend(J_3)
J_IR_photo.extend(J_4)
J_IR_photo.extend(J_5)
J_IR_photo = np.array(J_IR_photo)

H_1 = data_1[:,1] - (5 * np.log10(145) - 5)
#H_2 = data_2[1:,6] - (5 * np.log10(145) - 5)
H_3 = data_3[:,1] - (5 * np.log10(149) - 5)
H_4 = data_4[:,1] - (5 * np.log10(149) - 5)
H_5 = data_5[:,1] - (5 * np.log10(184) - 5)

H_IR_photo = []
H_IR_photo.extend(H_1)
H_IR_photo.extend(H_3)
H_IR_photo.extend(H_4)
H_IR_photo.extend(H_5)
H_IR_photo = np.array(H_IR_photo)

K_1 = data_1[:,2] - (5 * np.log10(145) - 5)
K_2 = data_2[:,0] - data_2[:,1] - (5 * np.log10(145) - 5)
K_3 = data_3[:,2] - (5 * np.log10(149) - 5)
K_4 = data_4[:,2] - (5 * np.log10(149) - 5)
K_5 = data_5[:,2] - (5 * np.log10(184) - 5)

K_IR_photo = []
K_IR_photo.extend(K_1)
#K_IR_photo.extend(K_2)
K_IR_photo.extend(K_3)
K_IR_photo.extend(K_4)
K_IR_photo.extend(K_5)
K_IR_photo = np.array(K_IR_photo)
