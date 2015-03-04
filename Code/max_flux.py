#!/usr/bin/env python

# ========================================================================== #
# File: max_flux.py                                                          #
# Programmer: Patrick Kantorski                                              #
# Date: 03/17/14                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to verify the accuracy of  #
#              statistical data taken from pictures of stellar multiples.    #
# ========================================================================== #

import os
import numpy as np
import pyfits



#def file_search(fil, path):
#    path = '/Users/ppkantorski/Documents/Research/Duchene/Datasets/*/*/K/*/*.fits'
#    cmd_str = 'echo ' + path + ' > temp.txt'
#    os.system(cmd_str)
    
#    lis = open('temp.txt')
#    file_string = str(lis.readlines())
#    file_list = file_string.split(" ")

#    found = 0
#    count = 0
#    while not found:
#        string = file_list[count]
#        loc = string.count(fil)
        
#        if found != 1 and count == len(file_list)-1:
#            print("File is not within that path.")
#            break
            
#    os.remove("temp.txt")
#    return file_list[count]


def max_flux(name, path = '/Users/ppkantorski/Documents/Research/Duchene/Datasets/*/*/K/img1/'):
#def max_flux(path):
    
    #full_file = file_search(fil, path)
    
    file = pyfits.open(path+name)
    image = file[0].data
    
    position = np.where(image == np.max(image))
    flux = np.max(image)
    
    print(position)
    print(flux)
    