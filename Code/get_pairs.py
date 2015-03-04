#!/usr/bin/env python

# ========================================================================== #
# File: give_pairs.py                                                        #
# Programmer: Patrick Kantorski                                              #
# Date: 04/02/14                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to extract data from       #
#              verified .npz files.                                          #
# ========================================================================== #

import numpy as np

def main():

    loop = True
    while loop == True:
        path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Verified_Data/'+raw_input("Please Enter Filename: ")+'.npz'
        file = np.load(path)
    
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0

    
        print("\nNumber:")
        while a < len(file['Number']):
            if file['Pairs'][a] == 1:
                print(file['Number'][a])
            a = a + 1
    
        print("\nName:")
        while b < len(file['Number']):
            if file['Pairs'][b] == 1:
                print(file['Name'][b])
            b = b + 1
    
        print("\nSeperation:")
        while c < len(file['Number']):
            if file['Pairs'][c] == 1:
                print(file['Seperation'][c])
            c = c + 1
    
        print("\nAngle:")
        while d < len(file['Number']):
            if file['Pairs'][d] == 1:
                print(file['Angle'][d])
            d = d + 1
    
        print("\nFlux:")
        while e < len(file['Number']):
            if file['Pairs'][e] == 1:
                print(file['Flux'][e])
            e = e + 1

        again = raw_input("\nRun again? (y/n): ")
    
        while again != 'Y' and again != 'y' and again != 'N' and again != 'n':
            again = raw_input("Please enter (y/n): ")
    
        if again == 'Y' or again == 'y':
            loop = True
            print('\n')
        
        elif again == 'N' or again == 'n':
            loop = False
            print('\nAll process are complete!')
    


if __name__ == '__main__':
	main()