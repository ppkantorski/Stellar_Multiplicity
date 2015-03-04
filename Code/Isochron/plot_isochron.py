#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def main():

    # Loading Isochron Data
    mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/mass.txt')
    Teff = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/temperature.txt')
    age = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/age.txt')
    luminosity = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/luminosity.txt')
    m_j = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/m_j.txt')
    m_h = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/m_h.txt')
    m_k = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Isochron/m_k.txt')


    ### Code for plotting Mass vs L, Teff, & Age. ###    
    n = 1
    while n < 4:
        plt.subplot(1, 3, n)
        
        # Mass vs Luminosity
        if n == 1:
            coefficients = np.polyfit(mass, luminosity, 3)
            polynomial = np.poly1d(coefficients)
            xs = np.arange(0.1, 7.0, 0.01)
            ys = polynomial(xs)
            
            plt.plot(xs, ys, color='r')
            plt.plot(mass, luminosity, 'o', color='b')
            
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Luminosity / L_Sun', fontsize='18')
        # Mass vs Teff
        if n == 2:
            coefficients = np.polyfit(mass, Teff, 3)
            polynomial = np.poly1d(coefficients)
            xs = np.arange(0.1, 7.0, 0.01)
            ys = polynomial(xs)
            
            plt.plot(xs, ys, color='r')
            plt.plot(mass, Teff, 'o', color='b')
            
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Teff / T_Sun', fontsize='18')
        # Mass vs Age
        if n == 3:
            coefficients = np.polyfit(mass, age, 3)
            polynomial = np.poly1d(coefficients)
            xs = np.arange(0.1, 7.0, 0.01)
            ys = polynomial(xs)
            
            #plt.plot(xs, ys, color='k)
            plt.plot(mass, age, 'o', color='b')
            plt.yscale('log')
            
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Age', fontsize='18')
        n += 1
        
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    
    plt.tight_layout()
    plt.show()
    #################################################
    
    
    ### Code for plotting Mass vs Mag J, H, & K. ###
    n = 1
    while n < 4:
        plt.subplot(1, 3, n)
        
        # Mass vs MagJ w/ 5th order polyfit
        if n == 1:
            coefficients = np.polyfit(mass, m_j, 7)
            polynomial = np.poly1d(coefficients)
            xs = np.arange(0.1, 7.0, 0.01)
            ys = polynomial(xs)
            
            plt.plot(xs, ys, color='r')
            plt.plot(mass, m_j, 'o', color='b')
    
            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Mag_J', fontsize='18')
            
        # Mass vs MagH w/ 5th order polyfit
        if n == 2:
            coefficients = np.polyfit(mass, m_h, 6)
            polynomial = np.poly1d(coefficients)
            xs = np.arange(0.1, 7.0, 0.01)
            ys = polynomial(xs)
            
            plt.plot(xs, ys, color='r')
            plt.plot(mass, m_h, 'o', color='b')

            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Mag_H', fontsize='18')

        # Mass vs MagK
        if n == 3:
            # Mass vs Mag_K w/ 5th order polyfit
            coefficients = np.polyfit(mass, m_k, 5)
            polynomial = np.poly1d(coefficients)
            xs = np.arange(0.1, 7.0, 0.01)
            ys = polynomial(xs)
            
            plt.plot(xs, ys, color='r')
            plt.plot(mass, m_k, 'o', color='b')

            plt.xlabel('Mass / M_Sun', fontsize='18')
            plt.ylabel('Mag_K', fontsize='18')
        n += 1
        
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    
    plt.tight_layout()
    plt.show()
    ################################################
    

    

    




if __name__ == '__main__':
	main()