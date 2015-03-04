#!/usr/bin/env python

# ========================================================================== #
# File: star_check.py                                                        #
# Programmer: Patrick Kantorski                                              #
# Date: 03/25/14                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to verify the accuracy of  #
#              statistical data taken from pictures of stellar multiples.    #
# ========================================================================== #

import numpy as np
import pyfits
import subprocess
import aper


def main():
    
    print("\nThis program was written by Patrick Kantorski to verify data collected by Gaspard Duchene.")

    date = raw_input("Date of Dataset: ")
    data_selection(date)
    
    print("Data Verification Complete!")


def data_selection(date):
    # Iteration variables for loops.
    loop = 1
    var = 0

    # Initializing identification number and lists for .npz file.
    number = 1
    name = []
    pairs = []
    num = []
    sep = []
    ang = []
    flux = []

    while loop <= 1:
        print("===========================================================================================\n")
        
        if date == "Feb17":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb17_bin.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        elif date == "Feb18":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb18_bin.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        elif date == "Feb19":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb19_bin.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        elif date == "Feb20":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb20_bin.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        elif date == "Extra":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/extra_bin.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        else:
            len_data = var + 1
        
        
        while var < len_data:
            if date == "Feb17" or  date == "Feb18" or  date == "Feb19" or  date == "Feb20" or date == "Extra":
                path =  data[var].rstrip()
                print("File with Directory:")
                print(path+'\n')
                
            else:
                path = raw_input("File with Directory: ")
        
            # Opens the file with DS9.
            p = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', path])
        
            
            name.append(raw_input("Picture Name: ") )
            pairs.append(input("Number of Pairs: ") )
            num.append(number)
        
        
            if pairs[number - 1] == 1:
            
                print("\nPrimary Star Information: ")
                m_f = max_flux(path)
                
                use = raw_input("Use Information? (y/n): ")
                
                if use != 'y' and use != 'Y' and use != 'n' and use != 'N':
                    a = True
                    while a == True:
                        use = raw_input("Please enter (y/n): ")
                        if use == 'y' or use == 'Y' or use == 'n' or use == 'N':
                            a = False
                        
                
                if use == 'y' or use == 'Y':
                    x1 = int(m_f[0][1]) + 1
                    y1 = int(m_f[0][0]) + 1
                    flux_1 = m_f[1]
                    
                    print("\n--- Primary Star ---")
                    print("X Position #1: "+str(x1))
                    print("Y Position #1: "+str(y1))
                    print("Flux Magnitude #1: "+str(flux_1))
                    
                elif use == 'n' or use == 'N':
                    
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
                flux.append(flux_ratio(flux_1,flux_2))
        
            else:
                sep.append(0.0)
                ang.append(0.0)
                flux.append(0.0)
            
            
            print("Number: "+str(num))
            print("Name: "+str(name))
            print("Pairs: "+str(pairs))
            print("Seperation: "+str(sep))
            print("Orbital Angle: "+str(ang))
            print("Magnitude Diff.: "+str(flux))
        
        
            np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Data/'+date, Number= num, Name= name, Pairs= pairs, Seperation= sep, Angle= ang, Flux= flux)
            number += 1
        
            # Checks to see if data verification is complete.
            finish = 1
            while finish == 1:
                x = raw_input("\nNext picture? (y/n) ")

                if x != 'y' and x != 'Y' and x != 'n' and x != 'N':
                    a = True
                    while a == True:
                        x = raw_input("Please enter (y/n): ")
                        if x == 'y' or x == 'Y' or x == 'n' or x == 'N':
                            a = False

                if x == 'Y' or x == 'y':
                    loop = 1
                    finish = 2
                    # Closes DS9.
                    p.terminate()
                    var = var + 1
                    print('\n')
            
                elif x == 'N' or x == 'n':
                    loop = 2
                    finish = 2
                    var = len_data
                    print('\n')
                    p.terminate()


# Finds primary star values.
def max_flux(path):
    
    file = pyfits.open(path)
    image = file[0].data
    
    position = np.where(image == np.max(image))
    flux = float(np.max(image))
    
    print("Position: "+ "x = " + str(int(position[1]+1))+ ", y = " +str(int(position[0]+1)) )
    print("Maximum Flux: "+ str(flux))
    
    return [position, flux];


# Calculates the seperation of binaries and position of primary star.
def position_check(x1,y1,x2,y2):
    
    x_distance = float(x2 - x1)
    y_distance = float(y2 - y1)
    
    print x1, x2, x_distance
    print y1, y2, y_distance
    
    # Pixel scale was set to 0.0495 arcsec/pix!
    z_distance = np.sqrt(x_distance**2 + y_distance**2)
    seperation = (0.0495) * z_distance
    
    print z_distance
    
    print("Seperation in arcsec: ")
    print(seperation)
    
    if x_distance == 0 and y_distance > 0:
        angle = 180
    
    elif x_distance == 0 and y_distance < 0:
        angle = 0

    elif x_distance > 0:
        #print np.arctan((-1*y_distance)/(x_distance) )
        #print "y/x: ", -y_distance/x_distance
        angle = np.rad2deg(np.arctan((-y_distance)/(x_distance) )) - 90.
        if angle < 0:
            angle = angle + 360

    elif x_distance < 0:
        #y_distance = -y_distance
        #print np.arctan((-1*y_distance)/(x_distance) )
        #print "y/x: ", -y_distance/x_distance
        angle = np.rad2deg(np.arctan((-y_distance)/(x_distance) )) + 90.
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
    print('\n')
    
    return ratio;


if __name__ == '__main__':
	main()