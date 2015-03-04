#!/usr/bin/env python

# ========================================================================== #
# File: d_limit.py                                                           #
# Programmer: Patrick Kantorski                                              #
# Date: 01/27/15                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to calculate and save      #
#              the detection limits for specified clusters.                  #
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
    print("===========================================================================================\n")
    sin_bin_choice = raw_input("Singles or Binaries? (s|b): ")
    loop = 1
    while loop <= 1:
        if sin_bin_choice != 's' and sin_bin_choice != '1' and sin_bin_choice != 'b' and sin_bin_choice != '2':
            sin_bin_choice = raw_input("Please enter (s|b): ")
            loop = 1
        else:
            loop = 2
    select = raw_input("\nEnter which dataset to use: ")

    # Defining arrays to store arrays for saving...
    all_names = []; all_ang_sep = []; all_mag_K = []; x_centroids = []; y_centroids = []
    DNE = []; triple_counter = 0; quad_counter = 0 # This counter will be used to offset the PA array after running through the 3-4 Star System.
    
    # Iteration variables for loops.
    loop = 1
    var = 0
    while loop <= 1:
        # New file selection.
        if sin_bin_choice == "s" or sin_bin_choice == "1":
            if select == "1":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/IC_2391_sin.txt', "r") as myfile:
                    cluster = "IC_2391"
                    data = myfile.readlines()
                    len_data = len(data)
            elif select == "2":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_6475_sin.txt', "r") as myfile:
                    cluster = "NGC_6475"
                    data = myfile.readlines()
                    len_data = len(data)
            elif select == "3":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_2451_sin.txt', "r") as myfile:
                    cluster = "NGC_2451"
                    data = myfile.readlines()
                    len_data = len(data)
            elif select == "4":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_2516_sin.txt', "r") as myfile:
                    cluster = "NGC_2516"
                    data = myfile.readlines()
                    len_data = len(data)
            elif select == "5":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_3532_sin.txt', "r") as myfile:
                    cluster = "NGC_3532"
                    data = myfile.readlines()
                    len_data = len(data)
            elif select == "6":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/IC_2602_sin.txt', "r") as myfile:
                    cluster = "IC_2602"
                    data = myfile.readlines()
                    len_data = len(data)
            print "Cluster:", cluster
        if sin_bin_choice == "b" or sin_bin_choice == "2":
            if select == "1":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/IC_2391_bin.txt', "r") as myfile:
                    cluster = "IC_2391"
                    data = myfile.readlines()
                    len_data = len(data)
                    triple_index = np.array([np.nan])
                    quad_index = np.array([np.nan])
            elif select == "2":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_6475_bin.txt', "r") as myfile:
                    cluster = "NGC_6475"
                    data = myfile.readlines()
                    len_data = len(data)
                    triple_index = np.array([0, 1, 2, 6, 7, 8])
                    quad_index = np.array([np.nan])
            elif select == "3":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_2451_bin.txt', "r") as myfile:
                    cluster = "NGC_2451"
                    data = myfile.readlines()
                    len_data = len(data)
                    triple_index = np.array([3, 4, 5, 30, 31, 32])
                    quad_index = np.array([np.nan])
            elif select == "4":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_2516_bin.txt', "r") as myfile:
                    print "\nNote: NGC 2516 does not contain any binaries...\n"
                    sys.exit()
                    cluster = "NGC_2516"
                    data = myfile.readlines()
                    len_data = len(data)
                    triple_index = np.array([np.nan])
                    quad_index = np.array([np.nan])
            elif select == "5":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/NGC_3532_bin.txt', "r") as myfile:
                    cluster = "NGC_3532"
                    data = myfile.readlines()
                    len_data = len(data)
                    triple_index = np.array([9, 10, 11, 15, 16, 17])
                    quad_index = np.array([np.nan])
            elif select == "6":
                with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/IC_2602_bin.txt', "r") as myfile:
                    cluster = "IC_2602"
                    data = myfile.readlines()
                    len_data = len(data)
                    triple_index = np.array([6, 7, 8])
                    quad_index = np.array([36, 37, 38, 39, 40, 41])
                    
            print "\nCluster:", cluster
            
            bin_sep_array = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/'+cluster+'_bin_sep.txt')[0::2]
            bin_PA_array = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/'+cluster+'_bin_PA.txt')[0::2]
            
        else:
            len_data = var + 1
        while var < len_data:
            print("\n===========================================================================================\n")
            if select == '1' or select == '2' or select == '3' or select =='4' or select =='5' or select =='6':
                try:
                    path =  data[var].rstrip()
                except IndexError:
                    print "End of file list has been reached!\n"
                    sys.exit()
                except IOError:
                    DNE.append(var+1)
                    var = var + 1
                    print "Specified file is missing..."
                    print "Opening next file..\n"
                    try:
                        path =  data[var].rstrip()
                    except IndexError:
                        print "End of file list has been reached!\n"
                        sys.exit()

                print("File with Directory:")
                print(path+'\n')
                
                current_img = 'img1'
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                if not name:
                    current_img = 'img2'
                    name = (path.partition('img2/')[2]).partition('.fits')[0]
                if not name:
                    current_img = 'img3'
                    name = (path.partition('img3/')[2]).partition('.fits')[0]
                    
                print("Star #"+str(var+1)+":")
                print(name+'\n')
            else:
                path = raw_input("Enter file path & name: ")
                current_img = 'img1'
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                if not name:
                    current_img = 'img2'
                    name = (path.partition('img2/')[2]).partition('.fits')[0]
                if not name:
                    current_img = 'img3'
                    name = (path.partition('img3/')[2]).partition('.fits')[0]
                    
                print("Star #"+str(var+1)+":")
                print(name+'\n')
    
    
    
            if (var in triple_index) == True:
                print '\nCurrent Selection is a 3 star system!\n'
            if (var in quad_index) == True:
                print '\nCurrent Selection is a 4 star system!\n'
            
            try:
                file = pyfits.open(path)

                print "Variable Number:", var
                # This line keeps track of the triple star offset/counter.  Without, data will be displaced.     # Side Note:
                if (var-3 in triple_index) == True:                                                              #    Future errors with the code not returing
                    if (var-2 in triple_index) == True:                                                          #  the correct 'PA' or 'Seperation' would be from
                        if (var-1 in triple_index) == True: # If previous 3 indexes                              #  this section. It works.. But only on everything
                            triple_counter = triple_counter + 3                                                  #  that I've tested it on so far.  If there is
                            if (var-4 in triple_index) == True:                                                  #  something wrong with the code, it would be from
                                quad_counter = quad_counter - 3 # If previous 4 indexes exist, undo the +6       #  not applying the 'if previous 4 indexes exist,
                            if (var-4 in triple_index) == True & (var-6 in triple_index) == True:                #  undo the +3 or +6, or in the lower case below
                                quad_counter = quad_counter + 3                                                  #  shown in the IOError section, +4 or +7.
                                                                                                                 # 
                if (var-3 in quad_index) == True:                                                                #    Anyways, the current code written should work
                    if (var-2 in quad_index) == True:                                                            #  properly. This was just a flag, no pun intended.
                        if (var-1 in quad_index) == True: # If previous 3 indexes                                # 
                            quad_counter = quad_counter + 6                                                      # 
                            if (var-4 in quad_index) == True:                                                    # 
                                quad_counter = quad_counter - 6 # If previous 4 indexes exist, undo the +6       # 
                            if (var-4 in quad_index) == True & (var-6 in quad_index) == True:                    # 
                                quad_counter = quad_counter + 6                                                  # 
                                                                                                                 # 
                                                                                                                 # 
            except IOError:                                                                                      # 
                # This line keeps track of the triple star offset/counter.  Without, data will be displaced.     # 
                if (var-2 in triple_index) == True:                                                              # 
                    if (var-1 in triple_index) == True:                                                          # 
                        if (var in triple_index) == True: # If previous 3 indexes                                # 
                            triple_counter = triple_counter + 3                                                  # 
                if (var-2 in quad_index) == True:                                                                # 
                    if (var-1 in quad_index) == True:                                                            # 
                        if (var in quad_index) == True: # If previous 3 indexes                                  # 
                            quad_counter = quad_counter + 6                                                      # 


                DNE.append(var+1)
                var = var + 1
                if (var in triple_index) == True:
                    print '\nCurrent Selection is a 3 star system!\n'
                if (var in quad_index) == True:
                    print '\nCurrent Selection is a 4 star system!\n'
                
                
                print "Specified file is missing..."
                print "Opening next file..\n"
                try:
                    path =  data[var].rstrip()
                except IndexError:
                    print "End of file list has been reached!\n"
                    sys.exit()
                
                print("File with Directory:")
                print(path+'\n')
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                print("Star #"+str(var+1)+":")
                print(name+'\n')
                
                file = pyfits.open(path)
                
                if (var in triple_index) == True:
                    print '\nCurrent Selection is a 3 star system!\n'
                print "Variable Number:", var 

                            
                    
            image = np.copy(file[0].data)
            
            # This index is used for the PA and Sep Arrays.
            PA_sep_index = np.around((var+triple_counter+quad_counter)/3) # returns 0, 0, 0, 1, 1, 1, 2, 2, 2, ...
            print "Triple Counter:", triple_counter
            print "Quad Counter:", quad_counter
            print "PA_sep_index:", PA_sep_index
            
            '''
            # Write test image for viewing...
            print "Writing test image..."
            write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/test_star.fits'
            fits.writeto(write_path, file[0].data, clobber=True)
            p_test = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
            '''
            print("===========================================================================================\n")
            
            
            skip = raw_input("Next star? (y|n): ")
            #skip = 'n'
            
            if skip == 'N' or skip == 'n':

                ### Enter primary star's information... ###
                print("\nPrimary Star Information: ")
                m_f = max_flux(image)
                x_pos_1 = float(m_f[0][0])
                y_pos_1 = float(m_f[0][1])
                
                print("\n--- Primary Star ---")
                print("X Position #1: "+str(x_pos_1))
                print("Y Position #1: "+str(y_pos_1))
                width_1 = 3
            
                # Find centroid for primary...
                x_cent_1 = centroid(image, width_1, x_pos_1, y_pos_1)[0]
                y_cent_1 = centroid(image, width_1, x_pos_1, y_pos_1)[1]
                print "\nCentroid of primary (x, y):", x_cent_1, y_cent_1
                
                # Find max flux for primary...
                max_flux_1 = image[y_cent_1, x_cent_1]
                print "Max flux for primary: ", max_flux_1

                if sin_bin_choice == 's' or sin_bin_choice == '1': # This code was added for labeling consistency.
                    image_full_fix = np.copy(image)
                
                # Applying mask to companion star for binaries...
                if sin_bin_choice == 'b' or sin_bin_choice == '2':
                    # This line will return true if binary is a 3 or 4 Star System, false if not.
                    triple_sys = var in triple_index
                    quad_sys = var in quad_index
                    
                    # 2-Star 'Binary' Case
                    if triple_sys == False and quad_sys == False:
                        print("\nCompanion Star Information: ")
                        print("\n--- Commpanion Star ---")
                                        
                        # Open DS9...
                        p = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', path])
                        
                        x_pos_2 = x_cent_1 + np.cos((270.-bin_PA_array[PA_sep_index])*np.pi/180.) * bin_sep_array[PA_sep_index] / 0.0495
                        y_pos_2 = y_cent_1 + np.sin((270.-bin_PA_array[PA_sep_index])*np.pi/180.) * bin_sep_array[PA_sep_index] / 0.0495
                    
                        print("X Position #1: "+str(x_pos_2))
                        print("Y Position #1: "+str(y_pos_2))
                    
                        print "\nPrimary Angle:", bin_PA_array[PA_sep_index]
                        print "Angular Seperation", bin_sep_array[PA_sep_index]

                        x_cent_2 = centroid(image, width_1, x_pos_2, y_pos_2)[0]
                        y_cent_2 = centroid(image, width_1, x_pos_2, y_pos_2)[1]
                        print "\nCentroid of companion (x, y):", x_cent_2, y_cent_2, '\n'
                        
                        
                        arc_or_box = raw_input("\nMask Companion Star with Box or Arc? (1|2): ")
                        
                        loop = 1
                        while loop <= 1:
                            if arc_or_box != '1' and arc_or_box != '2':
                                arc_or_box = raw_input("Please enter (1|2): ")
                                loop = 1
                            else:
                                loop = 2
                                
                        if arc_or_box == '1':
                            loop = 1
                            while loop <= 1:
                                width_2 = float(raw_input("\nEnter width of box around companion star: "))
                                img_fix = centroid(image, width_2, x_cent_2, y_cent_2)[3]
                                # Fixed image without primary star...
                                
                                image_full_fix = np.copy(image)
                                image_full_fix[y_cent_2-(width_2/2.):y_cent_2+(width_2/2.), x_cent_2-(width_2/2.):x_cent_2+(width_2/2.)] = img_fix
                                
                                # Write image for viewing...
                                print "\nWriting image with primary star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                                
                        
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        print '\nSaving masked fits file...'
                                        write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/'+cluster+'/'+name+'_'+current_img+'.fits'
                                        fits.writeto(write_path, image_full_fix, clobber=True)
                                        print 'Masked fits file was properly saved!\n'
                                        loop = 2
                                        loop_1 = 2
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                        
                        
                        if arc_or_box == '2':
                            loop = 1
                            while loop <= 1:
                                #os.remove('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits')
                                #print "Writing orignal image to the masked_star FITS file..."
                                #write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                #fits.writeto(write_path, image_original, clobber=True)
                                
                                width_2 = 5 # Value not important for arc circle area..
                                inner_rad = float(raw_input("\nInner Radius (in pix): "))
                                outter_rad = float(raw_input("Outter Radius (in pix): "))
                                ang_width = float(input("Ang. Width (in deg): "))
                                ang_range = (270. - bin_PA_array[PA_sep_index] - ang_width/2., 270. - bin_PA_array[PA_sep_index] + ang_width/2.)
                                
                                
                                img_fix = centroid(image, width_2, x_cent_2, y_cent_2, x_cent_1, y_cent_1, inner_rad, outter_rad, ang_range)[4]
                                image_full_fix = np.copy(img_fix)
                                
                                # Write image for viewing...
                                print "\nWriting image with primary star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                        
                                
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        print '\nSaving masked fits file...'
                                        write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/'+cluster+'/'+name+'_'+current_img+'.fits'
                                        fits.writeto(write_path, image_full_fix, clobber=True)
                                        print 'Masked fits file was properly saved!\n'
                                        loop = 2
                                        loop_1 = 2
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                                        
                    
                
                    
                    # 3-Star 'Binary' Case
                    if triple_sys == True:
                        print('\n**** This star is part of a 3-body system! ****\n')
                        
                        print("\nCompanion Star Information: ")
                        print("\n--- Commpanion Stars ---")
                                        
                        # Open DS9...
                        p = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', path])
                    
                        x_pos_2 = x_cent_1 + np.cos((270.-bin_PA_array[PA_sep_index])*np.pi/180.) * bin_sep_array[PA_sep_index] / 0.0495
                        y_pos_2 = y_cent_1 + np.sin((270.-bin_PA_array[PA_sep_index])*np.pi/180.) * bin_sep_array[PA_sep_index] / 0.0495
                        
                        x_pos_3 = x_cent_1 + np.cos((270.-bin_PA_array[PA_sep_index+1])*np.pi/180.) * bin_sep_array[PA_sep_index+1] / 0.0495
                        y_pos_3 = y_cent_1 + np.sin((270.-bin_PA_array[PA_sep_index+1])*np.pi/180.) * bin_sep_array[PA_sep_index+1] / 0.0495
                    
                        print "\nPrimary Angle #1:", bin_PA_array[PA_sep_index]
                        print "Angular Seperation #1", bin_sep_array[PA_sep_index]                        

                        x_cent_2 = centroid(image, width_1, x_pos_2, y_pos_2)[0]
                        y_cent_2 = centroid(image, width_1, x_pos_2, y_pos_2)[1]
                        print "\nCentroid of companion #1 (x, y):", x_cent_2, y_cent_2,
                        
                        print "\nPrimary Angle #2:", bin_PA_array[PA_sep_index + 1]
                        print "Angular Seperation #2", bin_sep_array[PA_sep_index + 1]
                        
                        x_cent_3 = centroid(image, width_1, x_pos_3, y_pos_3)[0]
                        y_cent_3 = centroid(image, width_1, x_pos_3, y_pos_3)[1]
                        print "\nCentroid of companion #2 (x, y):", x_cent_3, y_cent_3, '\n'
                        
                        loop = 1
                        while loop <= 1:
                            choice = float(raw_input("\nMask Companion Stars with Box/Box, Box/Arc, or Arc/Arc? (1|2|3): "))
                            if choice == 1 or choice == 2 or choice == 3:
                                loop = 2
                                print '\n'
                            else:
                                print('Please enter options (1|2|3).')

                        # Box/Box Mask
                        if choice == 1:
                            print "\n[1] Performing the 1st Box Mask..."
                            loop = 1 # This loop is for the first box..
                            while loop <= 1:
                                width_2 = float(raw_input("\nEnter width of box around companion star #1: "))
                                img_fix = centroid(image, width_2, x_cent_2, y_cent_2)[3]
                                # Fixed image without primary star...
                                
                                image_full_fix = np.copy(image)
                                image_full_fix[y_cent_2-(width_2/2.):y_cent_2+(width_2/2.), x_cent_2-(width_2/2.):x_cent_2+(width_2/2.)] = img_fix
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                        
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        image_copy = np.copy(image_full_fix)  # Replaces the previous image with the masked image.
                                        loop = 2
                                        loop_1 = 2
                                        p_2.kill()
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                            
                            print "\n[2] Performing the 2nd Box Mask..."            
                            loop = 1 # This loop is for the second box..
                            while loop <= 1:
                                width_2 = float(raw_input("\nEnter width of box around companion star #2: "))
                                img_fix = centroid(image_copy, width_2, x_cent_3, y_cent_3)[3]
                                # Fixed image without primary star...
                                
                                image_full_fix = np.copy(image_copy)
                                image_full_fix[y_cent_3-(width_2/2.):y_cent_3+(width_2/2.), x_cent_3-(width_2/2.):x_cent_3+(width_2/2.)] = img_fix
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                                            
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        print '\nSaving masked fits file...'
                                        write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/'+cluster+'/'+name+'_'+current_img+'.fits'
                                        fits.writeto(write_path, image_full_fix, clobber=True)
                                        print 'Masked fits file was properly saved!\n'
                                        loop = 2
                                        loop_1 = 2
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                        
                        # Box/Arc Mask
                        if choice == 2:
                            loop = 1
                            while loop <= 1:
                                choice_1 = float(raw_input('Apply Box Mask to Companion Star #1 or #2? (1|2): '))
                                if choice_1 == 1:
                                    PA_1 = bin_PA_array[PA_sep_index]
                                    PA_2 = bin_PA_array[PA_sep_index+1]
                                    x_C_1 = x_cent_2
                                    y_C_1 = y_cent_2
                                    x_C_2 = x_cent_3
                                    y_C_2 = y_cent_3
                                    loop = 2
                                if choice_1 == 2:
                                    PA_1 = bin_PA_array[PA_sep_index+1]
                                    PA_2 = bin_PA_array[PA_sep_index]
                                    x_C_1 = x_cent_3
                                    y_C_1 = y_cent_3
                                    x_C_2 = x_cent_2
                                    y_C_2 = y_cent_2
                                    loop = 2
                                else:
                                    print "Please Enter options (1|2). "
                            
                            # This section does the Box Mask before performing the Arc Mask.
                            print "\n[1] Performing the Box Mask..."
                            loop = 1
                            while loop <= 1:

                                width_2 = float(raw_input("\nEnter width of box around companion star #1: "))
                                img_fix = centroid(np.copy(image), width_2, x_C_1, y_C_1)[3]
                                # Fixed image without primary star...
                                
                                image_full_fix = np.copy(image)
                                image_full_fix[y_C_1-(width_2/2.):y_C_1+(width_2/2.), x_C_1-(width_2/2.):x_C_1+(width_2/2.)] = img_fix
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                        
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        loop = 2
                                        loop_1 = 2
                                        p_2.kill()
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                            
                            # This section does the Arc Mask after performing a Box Mask.
                            print "\n[2] Performing the Arc Mask..."
                            loop = 1
                            while loop <= 1:
                          
                                width_2 = 5 # Value not important for arc circle area..
                                inner_rad = float(raw_input("\nInner Radius (in pix): "))
                                outter_rad = float(raw_input("Outter Radius (in pix): "))
                                ang_width = float(input("Ang. Width (in deg): "))
                                ang_range = (270. - PA_2 - ang_width/2., 270. - PA_2 + ang_width/2.)
                                
                                img_fix = centroid(np.copy(image_full_fix), width_2, x_C_2, y_C_2, x_cent_1, y_cent_1, inner_rad, outter_rad, ang_range)[4]
                                image_full_fix = np.copy(img_fix)
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                        
                                
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        print '\nSaving masked fits file...'
                                        write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/'+cluster+'/'+name+'_'+current_img+'.fits'
                                        fits.writeto(write_path, image_full_fix, clobber=True)
                                        print 'Masked fits file was properly saved!\n'
                                        loop = 2
                                        loop_1 = 2
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')

                
                        # Arc/Arc Mask
                        if choice == 3:
                            print "\n[1] Performing the 1st Arc Mask..."
                            loop = 1 # This loop is for the 1st Arc Mask...
                            while loop <= 1:
                                #os.remove('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits')
                                #print "Writing orignal image to the masked_star FITS file..."
                                #write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                #fits.writeto(write_path, image_original, clobber=True)
                                
                                width_2 = 5 # Value not important for arc circle area..
                                inner_rad = float(raw_input("\nInner Radius (in pix): "))
                                outter_rad = float(raw_input("Outter Radius (in pix): "))
                                ang_width = float(input("Ang. Width (in deg): "))
                                ang_range = (270. - bin_PA_array[PA_sep_index] - ang_width/2., 270. - bin_PA_array[PA_sep_index] + ang_width/2.)
                                
                                img_fix = centroid(np.copy(image), width_2, x_cent_2, y_cent_2, x_cent_1, y_cent_1, inner_rad, outter_rad, ang_range)[4]
                                image_full_fix = np.copy(img_fix)
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                                
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        loop = 2
                                        loop_1 = 2
                                        p_2.kill()
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                            
                            
                            print "\n[2] Performing the 2nd Arc Mask..."
                            loop = 1 # This loop is for the 2nd Arc Mask...
                            while loop <= 1:
                                #os.remove('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits')
                                #print "Writing orignal image to the masked_star FITS file..."
                                #write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                #fits.writeto(write_path, image_original, clobber=True)
                                
                                width_2 = 5 # Value not important for arc circle area..
                                inner_rad = float(raw_input("\nInner Radius (in pix): "))
                                outter_rad = float(raw_input("Outter Radius (in pix): "))
                                ang_width = float(input("Ang. Width (in deg): "))
                                ang_range = (270. - bin_PA_array[PA_sep_index+1] - ang_width/2., 270. - bin_PA_array[PA_sep_index+1] + ang_width/2.)
                                
                                img_fix = centroid(np.copy(image_full_fix), width_2, x_cent_3, y_cent_3, x_cent_1, y_cent_1, inner_rad, outter_rad, ang_range)[4]
                                image_full_fix = np.copy(img_fix)
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                        
                                
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        print '\nSaving masked fits file...'
                                        write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/'+cluster+'/'+name+'_'+current_img+'.fits'
                                        fits.writeto(write_path, image_full_fix, clobber=True)
                                        print 'Masked fits file was properly saved!\n'
                                        loop = 2
                                        loop_1 = 2
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                        

                

                    # 4-Star 'Binary' Case
                    if quad_sys == True:
                        print('\n**** This star is part of a 4-body system! ****\n')
                        
                        print("\nCompanion Star Information: ")
                        print("\n--- Commpanion Stars ---")
                                        
                        # Open DS9...
                        p = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', path])
                    
                        x_pos_2 = x_cent_1 + np.cos((270.-bin_PA_array[PA_sep_index])*np.pi/180.) * bin_sep_array[PA_sep_index] / 0.0495
                        y_pos_2 = y_cent_1 + np.sin((270.-bin_PA_array[PA_sep_index])*np.pi/180.) * bin_sep_array[PA_sep_index] / 0.0495
                        
                        x_pos_3 = x_cent_1 + np.cos((270.-bin_PA_array[PA_sep_index+1])*np.pi/180.) * bin_sep_array[PA_sep_index+1] / 0.0495
                        y_pos_3 = y_cent_1 + np.sin((270.-bin_PA_array[PA_sep_index+1])*np.pi/180.) * bin_sep_array[PA_sep_index+1] / 0.0495

                        x_pos_4 = x_cent_1 + np.cos((270.-bin_PA_array[PA_sep_index+2])*np.pi/180.) * bin_sep_array[PA_sep_index+2] / 0.0495
                        y_pos_4 = y_cent_1 + np.sin((270.-bin_PA_array[PA_sep_index+2])*np.pi/180.) * bin_sep_array[PA_sep_index+2] / 0.0495
                    
                    
                        print "\nPrimary Angle #1:", bin_PA_array[PA_sep_index]
                        print "Angular Seperation #1", bin_sep_array[PA_sep_index]                        

                        x_cent_2 = centroid(image, width_1, x_pos_2, y_pos_2)[0]
                        y_cent_2 = centroid(image, width_1, x_pos_2, y_pos_2)[1]
                        print "\nCentroid of companion #1 (x, y):", x_cent_2, y_cent_2,
                        
                        print "\nPrimary Angle #2:", bin_PA_array[PA_sep_index + 1]
                        print "Angular Seperation #2", bin_sep_array[PA_sep_index + 1]
                        
                        x_cent_3 = centroid(image, width_1, x_pos_3, y_pos_3)[0]
                        y_cent_3 = centroid(image, width_1, x_pos_3, y_pos_3)[1]
                        print "\nCentroid of companion #2 (x, y):", x_cent_3, y_cent_3,
                        
                        print "\nPrimary Angle #3:", bin_PA_array[PA_sep_index + 2]
                        print "Angular Seperation #3", bin_sep_array[PA_sep_index + 2]
                        
                        x_cent_4 = centroid(image, width_1, x_pos_4, y_pos_4)[0]
                        y_cent_4 = centroid(image, width_1, x_pos_4, y_pos_4)[1]
                        print "\nCentroid of companion #3 (x, y):", x_cent_4, y_cent_4, '\n'
                        
                        loop = 1
                        while loop <= 1:
                            print "\nDefault Option: Masking Companion Stars with Box/Box/Box"
                            choice = 1
                            if choice == 1 or choice == 2 or choice == 3:
                                loop = 2
                            else:
                                print('Please enter options (1|2|3).')

                        # Box/Box/Box Mask
                        if choice == 1:
                            print "\n[1] Performing the 1st Box Mask..."
                            loop = 1 # This loop is for the first box..
                            while loop <= 1:
                                width_2 = float(raw_input("\nEnter width of box around companion star #1: "))
                                img_fix = centroid(image, width_2, x_cent_2, y_cent_2)[3]
                                # Fixed image without primary star...
                                
                                image_full_fix = np.copy(image)
                                image_full_fix[y_cent_2-(width_2/2.):y_cent_2+(width_2/2.), x_cent_2-(width_2/2.):x_cent_2+(width_2/2.)] = img_fix
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                        
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        image_copy = np.copy(image_full_fix)  # Replaces the previous image with the masked image.
                                        loop = 2
                                        loop_1 = 2
                                        p_2.kill()
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                            
                            print "\n[2] Performing the 2nd Box Mask..."            
                            loop = 1 # This loop is for the second box..
                            while loop <= 1:
                                width_2 = float(raw_input("\nEnter width of box around companion star #2: "))
                                img_fix = centroid(image_copy, width_2, x_cent_3, y_cent_3)[3]
                                # Fixed image without primary star...
                                
                                image_full_fix = np.copy(image_copy)
                                image_full_fix[y_cent_3-(width_2/2.):y_cent_3+(width_2/2.), x_cent_3-(width_2/2.):x_cent_3+(width_2/2.)] = img_fix
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                                            
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        image_copy = np.copy(image_full_fix)
                                        loop = 2
                                        loop_1 = 2
                                        p_2.kill()
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')

                            print "\n[3] Performing the 3rd Box Mask..."            
                            loop = 1 # This loop is for the second box..
                            while loop <= 1:
                                width_3 = float(raw_input("\nEnter width of box around companion star #3: "))
                                img_fix = centroid(image_copy, width_3, x_cent_4, y_cent_4)[3]
                                # Fixed image without primary star...
                                
                                image_full_fix = np.copy(image_copy)
                                image_full_fix[y_cent_4-(width_3/2.):y_cent_4+(width_3/2.), x_cent_4-(width_3/2.):x_cent_4+(width_3/2.)] = img_fix
                                
                                # Write image for viewing...
                                print "\nWriting image with companion star removed..."
                                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/masked_star.fits'
                                fits.writeto(write_path, image_full_fix, clobber=True)
                                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
                                            
                                loop_1 = 1
                                while loop_1 <= 1:
                                    good = raw_input("Use specified parameters? (y|n): ")
                                    if good == 'y' or good == 'Y':
                                        print '\nSaving masked fits file...'
                                        write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/'+cluster+'/'+name+'_'+current_img+'.fits'
                                        fits.writeto(write_path, image_full_fix, clobber=True)
                                        print 'Masked fits file was properly saved!\n'
                                        loop = 2
                                        loop_1 = 2
                                    elif good == 'n' or good == 'N':
                                        loop_1 = 2
                                        p_2.kill()
                                    else:
                                        print('\nPlease enter options (y|n). \n')
                        
                        

                
                
                ### Detection Limit Calculations ###
                ang_sep_array = []; flux_array = []
                for j in range(100, len(image_full_fix[0])-100, 1):
                    for i in range(100, len(image_full_fix[1])-100, 1):
                        x_position = i
                        y_position = j
                        max_flux_2 = image_full_fix[j,i]
                        flux_array.append(max_flux_2)
                        ang_sep_array.append(position_check(x_cent_1, y_cent_1, x_position, y_position)[0])
                
                #plt.plot(ang_sep_array, flux_array, '.')
                plt.xlabel('Angular Seperation', fontsize='18')
                plt.ylabel('Mag_K', fontsize='18')
                plt.xscale('log')
                plt.gca().invert_yaxis()
                #plt.show()
                
                N = 100 # total number of pixels in 5 arcsec radius.
                
                ang_sep_array = np.asarray(ang_sep_array)
                fix_ang_sep_array = np.round(ang_sep_array/.0495) * .0495 # Rounding to nearest pixel.
                fix_flux_array = flux_array 

                
                #plt.plot(fix_ang_sep_array, fix_flux_array, '.')
                plt.xlabel('Angular Seperation', fontsize='18')
                plt.ylabel('Mag_K', fontsize='18')
                plt.xscale('log')
                plt.gca().invert_yaxis()
                #plt.show()
                
                
                final_sep_array = list(set(fix_ang_sep_array))  # Removes degenerate values.
                final_flux_array = []; sort_flux_array = []
                for i in range(len(final_sep_array)):
                    for j in range(len(fix_ang_sep_array)):
                        if final_sep_array[i] == fix_ang_sep_array[j]:
                            final_flux_array.append(fix_flux_array[j])
                    
                    sort_flux_array.append(np.nanstd(final_flux_array) * 5.)
                    final_flux_array = []
                

                delta_K = flux_ratio(max_flux_1, sort_flux_array)
                sorted_data = np.array(sorted(np.column_stack((final_sep_array, delta_K)), key=lambda row: row[0]))
                sorted_x = []; sorted_y = []
                for i in range(len(sorted_data)):
                    sorted_x.append(sorted_data[i][0])
                    sorted_y.append(sorted_data[i][1])
                
                plt.clf()
                plt.plot(sorted_x, sorted_y, color='k')
                plt.xlabel('Angular Seperation', fontsize='18')
                plt.ylabel('Delta K', fontsize='18')
                plt.xscale('log')
                plt.gca().invert_yaxis()
                #plt.show()                

                all_names.append(name)
                all_ang_sep.append(sorted_x)
                all_mag_K.append(sorted_y)

                
                if sin_bin_choice == 's' or sin_bin_choice == '1':
                    print "\nSaving data for Star #"+str(var+1)+"..."
                    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/'+cluster+'_sin_data',
                    star_name = all_names, ang_sep=all_ang_sep, mag_K=all_mag_K)
                    print "Save data complete!"
                    
                if sin_bin_choice == 'b' or sin_bin_choice == '2':
                    print "\nSaving data for Star #"+str(var+1)+"..."
                    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/'+cluster+'_bin_data',
                    star_name = all_names, ang_sep=all_ang_sep, mag_K=all_mag_K)
                    print "Save data complete!"
                    
                
                #########################################################################

                flux = flux_ratio(max_flux_1, max_flux_2)


                loop = 1
                finish = 2
                
                print "\nFiles that DNE:", DNE
                
                
                ### Checks to see if data verification is complete. ###
                if sin_bin_choice == 's' or sin_bin_choice == '1':
                    finish = 0
                if sin_bin_choice == 'b' or sin_bin_choice == '2':
                    finish = 1
                while finish == 1:
                    x = raw_input("\nNext Star? (y/n): ")
                    if x != 'y' and x != 'Y' and x != 'n' and x != 'N':
                        a = True
                        while a == True:
                            x = raw_input("Please enter (y/n): ")
                            if x == 'y' or x == 'Y' or x == 'n' or x == 'N':
                                a = False
                    if x == 'Y' or x == 'y':
                        loop = 1
                        finish = 2
                        var = var + 1
                        # Closes DS9.
                        p.terminate()
                        p_2.terminate()
                        #p_test.terminate()
                        print('\n')
                    elif x == 'N' or x == 'n':
                        loop = 2
                        finish = 2
                        p.terminate()
                        p_2.terminate()
                        #p_test.terminate()
                        print('\nAll process are complete!')
                        sys.exit()
                #######################################################
                
            elif skip == 'y' or skip == 'Y':
                loop = 1
                finish = 2
                var = var + 1


def max_flux(img):
    position = np.where(img[120:190, 120:190] == np.max(img[120:190, 120:190]))
    flux = float(np.max(img[120:190, 120:190]))

    x_pos = int(position[1])+1+120
    y_pos = int(position[0])+1+120
    position = [x_pos, y_pos]
    #print position
    
    print "Position:", "x =", position[0], ", y =", position[1]
    print("Maximum Flux: "+ str(flux))
    
    return [position, flux]


def centroid(img, width, x_pos, y_pos, x_cent = None, y_cent = None, rad_inner = None, rad_outter = None, ang_range = None):
    img_copy = np.copy(img) # Creating a copy of the image is essential so that original values aren't overwritten.
    star_box = img_copy[y_pos-(width/2):y_pos+(width/2), x_pos-(width/2):x_pos+(width/2)]
    std = np.std(star_box)
    
    x_weights = np.sum(star_box, axis = 0)
    x_vector = np.arange(len(star_box[1]))
    y_weights = np.sum(star_box, axis = 1)
    y_vector = np.arange(len(star_box[0]))
    
    x_centroid = np.sum(x_vector*x_weights)/np.sum(x_weights) + x_pos-(width/2)
    y_centroid = np.sum(y_vector*y_weights)/np.sum(y_weights) + y_pos-(width/2)
    
    # Sets the box about the star equal to 'nan' values...
    if x_cent == None:
        mask_box = star_box - np.nan
        mask_arc = np.nan

    # Sets the arc circle area about the star equal to 'nan' values...
    if x_cent != None:
        mask_box = np.nan
        mask_select = sector_mask(img.shape, (x_cent, y_cent), rad_inner, rad_outter, ang_range)
        mask_arc = img_copy
        mask_arc[mask_select] = np.nan
        #mask_arc = star_a - np.nan
        

    
    
    return [x_centroid, y_centroid, std, mask_box, mask_arc]


def aperature(img, x_pos, y_pos, std, rad_out=0):
    flux_array = []
    count_array = []
    ratio_array = []
    rad_array = []
    std_array = []

    # Changed Radius from 5.0 to 3.0
    rad = 0.5 # to find 1 pixel! 
    
    x_range = np.arange(x_pos - rad, x_pos + rad)
    y_range = np.arange(y_pos - rad, y_pos + rad)
    #rad_range = np.arange(start, radius, 0.5)

    flux = 0
    count = 0
    flux_outside = 0
    count_out = 0
    for i in x_range:
        for j in y_range:
            r = np.sqrt((i-x_pos)**2 + (j-y_pos)**2)
            if r < rad:
                count = count + 1
                flux = flux + img[j,i]
            if r >= rad and r< rad_out:
                count_out = count_out + 1
                flux_outside = flux_outside + img[j,i]


    return [flux, flux_outside]
    #return [max_rad, max_ratio]


# Calculates the seperation of binaries and position of primary star.
def position_check(x1,y1,x2,y2):

    x_distance = float(x2 - x1)
    y_distance = float(y2 - y1)
    
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


# Calculates the flux ratio between two stars.
def flux_ratio(flux_1,flux_2):
    
    ratio = 2.5 * np.log10(flux_1/flux_2)
    #print("Flux Ratio of Stars: ")
    #print(ratio)
    #print('\n')
    
    return ratio

def sector_mask(shape, centre, rad_inner, rad_outter, angle_range):
    """
    Return a boolean mask for a circular sector. The start/stop angles in  
    `angle_range` should be given in clockwise order.
    """

    x,y = np.ogrid[:shape[0],:shape[1]]
    cy,cx = centre # fitts files are stupid
    tmin,tmax = np.deg2rad(angle_range)
    

    # ensure stop angle > start angle
    if tmax < tmin:
            tmax += 2*np.pi

    # convert cartesian --> polar coordinates
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = np.arctan2(x-cx,y-cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2*np.pi)

    # circular mask
    circmask = (r2 >= rad_inner**2) & (r2 <= rad_outter**2)

    # angular mask
    anglemask = theta <= (tmax-tmin)

    return circmask*anglemask


def reboot():
    # Reboot script.
    os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/cent_aper.py")
    sys.exit()
    

if __name__ == '__main__':
	main()