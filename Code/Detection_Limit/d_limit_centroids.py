#!/usr/bin/env python

# ========================================================================== #
# File: d_limit_centroids.py                                                 #
# Programmer: Patrick Kantorski                                              #
# Date: 01/27/15                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was parsed from the original 'd_limit.py'        #
#              program to store the orignal max flux & centroid values       #
#              for use in the 'd_lim_calc.py' program.                       #
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

    bs_choice = raw_input("Singles or Binaries (s|b)? : ")
    stay = True
    while stay == True:
        if bs_choice != 's' and bs_choice != 'S' and bs_choice != 'b' and bs_choice != 'B':
            bs_choice = raw_input("Please Enter (s|b): ")
        else:
            stay = False
            
    select = raw_input("Compute centroids for (1|2|3|4|5|6)? : ")
    stay = True
    while stay == True:
        if select != '1' and select != '2' and select != '3' and select != '4' and select != '5' and select != '6':
            select = raw_input("Please Enter Options (1|2|3|4|5|6): ")
        else:
            stay = False

    # Defining arrays to store arrays for saving...
    all_names = []; all_ang_sep = []; all_mag_K = []; x_centroids = []; y_centroids = []; max_flux_array = []
    DNE = []; triple_counter = 0; quad_counter = 0 # This counter will be used to offset the PA array after running through the 3-4 Star System.
    
    # Iteration variables for loops.
    loop = 1
    var = 0
    while loop <= 1:
        # New file selection.
        if bs_choice == 's' or bs_choice == 'S':
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
            # Initialized to provide dummy data.
            triple_index = np.array([np.nan])
            quad_index = np.array([np.nan])
            
            
        if bs_choice == 'b' or bs_choice == 'B':
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
            else:
                len_data = var + 1
        
        print "\nCluster:", cluster
        try:
            path =  data[var].rstrip()
        except IndexError:
            print "End of file list has been reached!\n"
            sys.exit()
        
        
        if bs_choice == 'b' or bs_choice == 'B':
            bin_sep_array = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/'+cluster+'_bin_sep.txt')[0::2]
            bin_PA_array = np.loadtxt('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/'+cluster+'_bin_PA.txt')[0::2]
            

            
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
                
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                if not name:
                    name = (path.partition('img2/')[2]).partition('.fits')[0]
                if not name:
                    name = (path.partition('img3/')[2]).partition('.fits')[0]
                    
                print("Star #"+str(var+1)+":")
                print(name+'\n')
            else:
                path = raw_input("Enter file path & name: ")
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                if not name:
                    name = (path.partition('img2/')[2]).partition('.fits')[0]
                if not name:
                    name = (path.partition('img3/')[2]).partition('.fits')[0]
                    
                print("Star #"+str(var+1)+":")
                print(name+'\n')
    
    
            
            try:
                file = pyfits.open(path)
                                                                                                                 
                                                                                                                 
            except IOError:                                                                                      
                # This line keeps track of the triple star offset/counter.  Without, data will be displaced.                               


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
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                print("Star #"+str(var+1)+":")
                print(name+'\n')
                
                file = pyfits.open(path)
                
                if (var in triple_index) == True:
                    print '\nCurrent Selection is a 3 star system!\n'
                print "Variable Number:", var 

                            
                    
            image = np.copy(file[0].data)
            
            # This index is used for the PA and Sep Arrays.
            if bs_choice == 'b' or bs_choice == 'B':
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
            
            
            #skip = raw_input("Next star? (y|n): ")
            skip = 'n'
            
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


                
                x_centroids.append(x_cent_1); y_centroids.append(y_cent_1); max_flux_array.append(max_flux_1); all_names.append(name)
                
                if bs_choice == 'b' or bs_choice == 'B':
                    print "\nSaving data for Binary Star #"+str(var+1)+"..."
                    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Centroid_Data/'+cluster+'_centroid_data',
                    star_name = all_names, x_cent=x_centroids, y_cent=y_centroids, max_flux=max_flux_array)
                    print "Save data complete!"
                
                if bs_choice == 's' or bs_choice == 'S':
                    print "\nSaving data for Single Star #"+str(var+1)+"..."
                    np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Singles/Centroid_Data/'+cluster+'_centroid_data',
                    star_name = all_names, x_cent=x_centroids, y_cent=y_centroids, max_flux=max_flux_array)
                    print "Save data complete!"
                
                #########################################################################


                loop = 1
                finish = 1
                
                
                ### Checks to see if data verification is complete. ###

                while finish == 1:
                    #x = raw_input("\nNext Star? (y/n): ")
                    x = 'y'
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
                        #p_test.terminate()
                        print('\n')
                    elif x == 'N' or x == 'n':
                        loop = 2
                        finish = 2
                        p.terminate()
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