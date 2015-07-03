#!/usr/bin/env python

import numpy as np
import pylab as plt
from pylab import rcParams

def main():

    bin_sep = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Distributions/bin_Sep.txt')[0::2]
    avg_mass = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Distributions/avg_mass.txt')
    m_ratio = avg_mass[1::2] / avg_mass[0::2]


    rcParams['figure.figsize'] = 14, 7
    plt.suptitle('Distribution Histograms', fontsize=22)
    
    plt.subplot(121)
    plt.hist(bin_sep, bins = 10 ** np.linspace(np.log10(30), np.log10(1500), 6), color='0.5')
    plt.gca().set_xscale("log")
    plt.xlabel('Seperation (AU)', fontsize=16)
    
    plt.subplot(122)
    plt.hist(m_ratio, bins=5, color='0.5')
    plt.xlabel('Mass Ratio', fontsize=16)

    plt.show()
    
    
    plt.title('Binary Mass Comparison', fontsize=22)
    plt.plot(avg_mass[1::2], avg_mass[0::2], 'x', color='b')
    plt.plot(np.arange(0,6), np.arange(0,6), '--', color='k')
    plt.plot(np.arange(0,2), 5*np.arange(0,2), '--', color='k')
    plt.xlabel('Companion Mass', fontsize=16)
    plt.ylabel('Primary Mass', fontsize=16)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
	main()