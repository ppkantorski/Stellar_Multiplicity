#!/usr/bin/env python

# ========================================================================== #
# File: d_lim_calc.py                                                        #
# Programmer: Patrick Kantorski                                              #
# Date: 01/27/15                                                             #
# Research: Stellar Multiplicity                                             #
# Advisor: Gapsard Duchene                                                   #
# Description: This program was written in Python to calculate and save      #
#              the detection limits for specified images.                    #
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
    var = 0; all_names=[]; all_ang_sep=[]; all_mag_K=[]; all_max_flux=[]
    
    select = raw_input("Compute Detection Limit for (1|2|3|4|5|6)? : ")
    stay = True
    while stay == True:
        if select != '1' and select != '2' and select != '3' and select != '4' and select != '5' and select != '6':
            select = raw_input("Please Enter Options (1|2|3|4|5|6): ")
        else:
            stay = False
    
    # New file selection.
    if select == "1":
        with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/IC_2391_masked.txt', "r") as myfile:
            cluster = "IC_2391"
            data = myfile.readlines()
            len_data = len(data)
    elif select == "2":
        with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/NGC_6475_masked.txt', "r") as myfile:
            cluster = "NGC_6475"
            data = myfile.readlines()
            len_data = len(data)
    elif select == "3":
        with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/NGC_2451_masked.txt', "r") as myfile:
            cluster = "NGC_2451"
            data = myfile.readlines()
            len_data = len(data)
    elif select == "4":
        with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/NGC_2516_masked.txt', "r") as myfile:
            cluster = "NGC_2516"
            data = myfile.readlines()
            len_data = len(data)
    elif select == "5":
        with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/NGC_3532_masked.txt', "r") as myfile:
            cluster = "NGC_3532"
            data = myfile.readlines()
            len_data = len(data)
    elif select == "6":
        with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Mask_Log/IC_2602_masked.txt', "r") as myfile:
            cluster = "IC_2602"
            data = myfile.readlines()
            len_data = len(data)
    print "Cluster:", cluster
    
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
            name = (path.partition(cluster+'/')[2]).partition('_img1.fits')[0]
            if ('_img2.fits' in name) == True:
                current_img = 'img2'
                name = (path.partition(cluster+'/')[2]).partition('_img2.fits')[0]                       
            if ('_img3.fits' in name )== True:                                                           
                current_img = 'img3'                                                                     
                name = (path.partition(cluster+'/')[2]).partition('_img3.fits')[0]                       
                                                                                                         
            print("Star #"+str(var+1)+":")                                                               
            print(name+'\n')                                                                             
                                                                                                         
                                                                                                         
        try:                                                                                             
            file = pyfits.open(path)                                                                     
                                                                                                         
        except IOError:                                                                                                    
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
            name = (path.partition(cluster+'/')[2]).partition('_img1.fits')[0]                           
            print("Star #"+str(var+1)+":")                                                               
            print(name+'\n')                                                                             
                                                                                                         
            file = pyfits.open(path)
            
        image = np.copy(file[0].data)
        #STD_image = np.nanstd(image)
        #print "Image STD:", STD_image
        #print image[np.where(3*STD_image > image)]
        
        
        # Open DS9...
        #p = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', path])
        #p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])
        
        #a = raw_input('Press Enter to continue... ')
        
        ### Enter primary star's information... ###
        print("\nPrimary Star Information: ")
        #m_f = max_flux(image)
        #x_pos_1 = float(m_f[0][0])
        #y_pos_1 = float(m_f[0][1])
        
        print("\n--- Primary Star ---")
        #print("X Position #1: "+str(x_pos_1))
        #print("Y Position #1: "+str(y_pos_1))
        #width_1 = 3
    
        # Find centroid for primary...
        x_cent_1 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Centroid_Data/'+cluster+'_centroid_data.npz')['x_cent'][var]
        y_cent_1 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Centroid_Data/'+cluster+'_centroid_data.npz')['y_cent'][var]
        #x_cent_1 = centroid(image, width_1, x_pos_1, y_pos_1)[0]
        #y_cent_1 = centroid(image, width_1, x_pos_1, y_pos_1)[1]
        print "\nCentroid of primary (x, y):", x_cent_1, y_cent_1
        
        # Find max flux for primary...
        max_flux_1 = np.load('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Centroid_Data/'+cluster+'_centroid_data.npz')['max_flux'][var]
        print "Max flux for primary: ", max_flux_1
    
    
        ### Detection Limit Calculations ###                                                                  # I might have to apply the 3xSTD
        ang_sep_array = []; flux_array = []                                                                   # condition here instead of below.
        for j in range(100, len(image[0])-100, 1):                                                            #
            for i in range(100, len(image[1])-100, 1):                                                        #
                x_position = i                                                                                #
                y_position = j                                                                                #
                max_flux_2 = image[j,i]                                                                       #
                flux_array.append(max_flux_2)                                                                 #
                ang_sep_array.append(position_check(x_cent_1, y_cent_1, x_position, y_position)[0])           #
                                                                                                              #
        #plt.plot(ang_sep_array, flux_array, '.')                                                             #
        #plt.xlabel('Angular Seperation', fontsize='18')                                                      #
        #plt.ylabel('Mag_K', fontsize='18')                                                                   #
        #plt.xscale('log')                                                                                    #
        #plt.gca().invert_yaxis()                                                                             #
        #plt.show()                                                                                           #
                                                                                                              #
                                                                                                              #
                                                                                                              #
        
        N = 100 # total number of pixels in 5 arcsec radius.
        
        ang_sep_array = np.asarray(ang_sep_array)
        fix_ang_sep_array = np.round(ang_sep_array/.0495) * .0495 # Rounding to nearest pixel.
        fix_flux_array = flux_array
        
        
        #plt.plot(fix_ang_sep_array, fix_flux_array, '.')
        #plt.xlabel('Angular Seperation', fontsize='18')
        #plt.ylabel('Mag_K', fontsize='18')
        #plt.xscale('log')
        #plt.gca().invert_yaxis()
        #plt.show()
        
        
        sorted_data = np.array(sorted(np.column_stack((fix_ang_sep_array, fix_flux_array)), key=lambda row: row[0]))
        sorted_x = []; sorted_y = []
        for i in range(len(sorted_data)):
            sorted_x.append(sorted_data[i][0])
            sorted_y.append(sorted_data[i][1])
        fix_ang_sep_array = sorted_x
        fix_flux_array = sorted_y
        
        
        final_sep_array = list(set(fix_ang_sep_array)) # Removes degenerate values.
        final_flux_array = []; sort_flux_array = []

        for i in range(len(final_sep_array)):
            for j in range(len(fix_ang_sep_array)):
                if final_sep_array[i] == fix_ang_sep_array[j]:
                    final_flux_array.append(fix_flux_array[j])
            
            if final_sep_array[i] > 1.25:
                for m in range(len(final_flux_array)):
                    if final_flux_array[m] > (3 * np.nanstd(final_flux_array)):
                        #print 'Bad Pixel Value:', final_flux_array[m]
                        #print 'Seperation:', final_sep_array[i]
                        final_flux_array[m] = np.nan
                        #print final_flux_array[m]
                    #if 3* np.nanstd(final_flux_array) < final_flux_array[m]:
                        #print 'Bad Pixel Value:', final_flux_array[m]
                        #print 'Seperation:', final_sep_array[i]
                    #    final_flux_array[m] = np.nan
                        #print final_flux_array[m]
            
            sort_flux_array.append(np.nanstd(final_flux_array) * 5.)
            final_flux_array = []
        
        
        delta_K = flux_ratio(max_flux_1, sort_flux_array)
        sorted_data = np.array(sorted(np.column_stack((final_sep_array, delta_K)), key=lambda row: row[0]))
        sorted_x = []; sorted_y = []
        for i in range(len(sorted_data)):
            sorted_x.append(sorted_data[i][0])
            sorted_y.append(sorted_data[i][1])
        
        #plt.clf()
        #plt.plot(sorted_x, sorted_y, color='k')
        #plt.xlabel('Angular Seperation', fontsize='18')
        #plt.ylabel('Delta K', fontsize='18')
        #plt.xscale('log')
        #plt.gca().invert_yaxis()
        #plt.show()                
        
        all_names.append(name)
        all_ang_sep.append(sorted_x)
        all_mag_K.append(sorted_y)
        
        print all_names
        print "\nSaving data for Star #"+str(var+1)+"..."
        np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Detection_Limit/Binaries/Recalculations/'+cluster+'_bin_data',
        star_name = all_names, ang_sep=all_ang_sep, mag_K=all_mag_K)
        print "Save data complete!"
        
        #a = raw_input('Press any key to continue... ')
        #p.terminate()
        var = var + 1
    
    
def max_flux(img):
    position = np.where(img[120:190, 120:190] == np.max(img[120:190, 120:190]))
    flux = float(np.max(img[120:190, 120:190]))
    print img

    x_pos = int(position[1])+1+120
    y_pos = int(position[0])+1+120
    position = [x_pos, y_pos]
    #print position
    
    print "Position:", "x =", position[0], ", y =", position[1]
    print("Maximum Flux: "+ str(flux))
    
    return [position, flux]
    

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


def find_and_replace(array, find, replace):
    sort_idx = np.argsort(array)
    where_ = np.take(sort_idx, 
                     np.searchsorted(array, find, sorter=sort_idx))
    if not np.all(array[where_] == find):
        raise ValueError('All items in find must be in array')
    array[where_] = replace


if __name__ == '__main__':
	main()