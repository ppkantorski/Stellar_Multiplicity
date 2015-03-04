#!/usr/bin/env python

# ========================================================================== #
# File: star_check.py                                                        #
# Programmer: Patrick Kantorski                                              #
# Date: 03/24/14                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to verify the accuracy of  #
#              statistical data taken from pictures of stellar multiples.    #
# ========================================================================== #

import numpy as np
import pyfits
import subprocess


def main():
    
    print("\nThis program was written by Patrick Kantorski to verify data collected by Gaspard Duchene.")

    date = raw_input("Date of Dataset: ")
    data_selection(date)
    
    print("Data Verification Complete!")


def data_selection(date):
    loop = 1
    number = 1

    name = []
    binary = []
    num = []
    sep = []
    ang = []
    flux = []

    while loop <= 1:
        print("===========================================================================================\n")
        
        path = raw_input("File with Directory: ")
        
        # Opens the file with DS9.
        p = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", path])
        
        name.append(raw_input("Picture Name: ") )
        binary.append(input("Number of Pairs: ") )
        
        num.append(number)
        
        
        if binary[number - 1] == 1:
            
            print("\nPrimary Star Information: ")
            max_flux(path)
            
            
            print("\nInsert values to verify star.")
            print("--- Primary Star ---")
            x1 = input("X Position #1: ")
            y1 = input("Y Position #1: ")
            flux_1 = input("Flux Magnitude #1: ")
            
            print("--- Secondary Star ---")
            x2 = input("X Position #2: ")
            y2 = input("Y Position #2: ")
            flux_2 = input("Flux Magnitude #2: ")
            print('\n')
            
            # Position 1 is seperation, position 2 is angle.
            position = position_check(x1,y1,x2,y2)
            sep.append(position[0])
            ang.append(position[1])

            flux.append(flux_ratio(flux_1,flux_2) )
        
        else:
            sep.append(0.0)
            ang.append(0.0)
            flux.append(0.0)
            
        print('\n')
        print(num)
        print(name)
        print(binary)
        print(sep)
        print(ang)
        print(flux)
        
        
        np.savez(date, Number= num, Name= name, Pairs= binary, Seperation= sep, Angle= ang, Flux= flux)
        number += 1
        
        # Checks to see if data verification is complete.
        finish = 1
        while finish == 1:
            x = raw_input("\nNext picture? (Y/N) ")

            if x == 'Y' or x == 'y':
                loop = 1
                finish = 2
                # Closes DS9.
                p.terminate()
            
            elif x == 'N' or x == 'n':
                loop = 2
                finish = 2
                p.terminate()


# Finds primary star values.
def max_flux(path):
    
    file = pyfits.open(path)
    image = file[0].data
    
    position = np.where(image == np.max(image))
    flux = np.max(image)
    
    print("Position: "+ "x = " + str(position[1])+ ", y = " +str(position[0]) )
    print("Maximum Flux: "+ str(flux))
    
    return [position, flux];


# Calculates the seperation of binaries and position of primary star.
def position_check(x1,y1,x2,y2):
    
    x_distance = x2 - x1
    y_distance = y2 - y1
    
    z_distance = np.sqrt(x_distance**2 + y_distance**2)
    seperation = (0.0495) * z_distance
    
    print("Seperation in arcsec: ")
    print(seperation)
    
    if x_distance == 0 and y_distance > 0:
        angle = 180
    
    elif x_distance == 0 and y_distance < 0:
        angle = 0

    elif x_distance > 0:
        angle = np.rad2deg(np.arctan((-y_distance)/(x_distance) )) - 90
        if angle < 0:
            angle = angle + 360

    else:
        angle = np.rad2deg(np.arctan((-y_distance)/(x_distance) )) + 90
        if angle < 0:
            angle = angle + 360

    print("Primary Star Position in degrees: ")
    print(angle)
    
    return [seperation, angle];


# Calculates the flux ratio between two stars.
def flux_ratio(flux_1,flux_2):
    
    ratio = 2.5 * np.log10(flux_1/flux_2)
    print("Flux Ratio of Stars: ")
    print(ratio)
    
    return ratio;


if __name__ == '__main__':
	main()