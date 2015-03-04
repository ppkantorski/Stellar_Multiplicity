#!/usr/bin/env python

# ========================================================================== #
# File: position_check.py                                                    #
# Programmer: Patrick Kantorski                                              #
# Date: 05/01/14                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to verify the accuracy of  #
#              statistical data taken from pictures of stellar multiples.    #
# ========================================================================== #

import numpy as np
import matplotlib.pyplot as plt
import pyfits
from scipy.ndimage import gaussian_filter
import astropy.io.fits as fits
import subprocess
import os
import sys
import pdb

def main():
    del_x = float(raw_input("Enter the change in x-direction: "))
    del_y = float(raw_input("Enter the change in x-direction: "))
    
    ang_sep = position_check(del_x, del_y)[0]
    PA = position_check(del_x, del_y)[1]
    
    print "\nAngular Seperation: " + str(ang_sep)
    print "Primary Angle: " + str(PA)

def position_check(delta_x, delta_y):

    x_distance = delta_x
    y_distance = delta_y
    
    #print x1, x2, x_distance
    #print y1, y2, y_distance
    
    # Pixel scale was set to 0.0495 arcsec/pix!
    z_distance = np.sqrt(x_distance**2 + y_distance**2)
    seperation = (0.0495) * z_distance
    
    #print z_distance
    
    #print("Seperation in arcsec: ")
    #print(seperation)
    
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

    #print("Primary Star Position in degrees: ")
    #print(angle)
    
    return [seperation, angle];

if __name__ == '__main__':
	main()