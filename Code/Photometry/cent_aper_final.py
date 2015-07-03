#!/usr/bin/env python

# ========================================================================== #
# File: cent_aper_final.py                                                   #
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
    print("===========================================================================================\n")
    select = raw_input("Enter which data to use: ")
    
    # Iteration variables for loops.
    loop = 1
    var = 0
    while loop <= 1:
        # New file selection.
        if select == "K" or select == "k":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/last_K.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        if select == "H" or select == "h":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/final_stars_H.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        if select == "J" or select == "j":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/final_stars_J.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        if select == "final":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/final_stars.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        if select == "all":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/all_bin.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        if select == "last":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/last_check.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        if select == "new":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/new_binaries.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        if select == "quick":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/Quick Checks/quick.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
                
        # Added selection to quickly scan through every star & identify overblown images...
        if select == "Feb17":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb17_files.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        elif select == "Feb18":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb18_files.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        elif select == "Feb19":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb19_files.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
        elif select == "Feb20":
            with open ('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/feb20_files.txt', "r") as myfile:
                data = myfile.readlines()
                len_data = len(data)
                
        
        else:
            len_data = var + 1
        while var < len_data:
            print("\n===========================================================================================\n")
            if select == "K" or select == "k" or select == "H" or select == "h" or select == "J" or select == "j" \
            or select == "final" or select == "all" or select == "last" or select == "new" or select == "quick" \
            or select == "Feb17" or select == "Feb18" or select == "Feb19" or select == "Feb20":
                path =  data[var].rstrip()
                print("File with Directory:")
                print(path+'\n')
                
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                print("Star #"+str(var+1)+":")
                print(name+'\n')
            else:
                path = raw_input("Enter file path & name: ")
                name = (path.partition('img1/')[2]).partition('.fits')[0]
                print("Star #"+str(var+1)+":")
                print(name+'\n')
    
            # Open DS9...
            p = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', path])
            file = pyfits.open(path)
            image = file[0].data
            print("===========================================================================================\n")
            
            
            skip = raw_input("Next star? (y|n): ")
            #skip = 'n'
            
            if skip == 'N' or skip == 'n':

                ### Noise calculation... ###
                print("\nPosition #1 For Noise Calculation.")
                print("--- Noise Position ---")
                x_pos_1 = float(raw_input("X Position #1: "))
                y_pos_1 = float(raw_input("Y Position #1: "))
                width_1 = float(raw_input("Enter width of box around sky: "))
                std_noise_1 = centroid(image, width_1, x_pos_1, y_pos_1)[2]
                print "Standard Deviation of Noise #1:", std_noise_1
                
                print("\nPosition #2 For Noise Calculation.")
                print("--- Noise Position ---")
                x_pos_2 = float(raw_input("X Position #2: "))
                y_pos_2 = float(raw_input("Y Position #2: "))
                width_2 = float(raw_input("Enter width of box around sky: "))
                std_noise_2 = centroid(image, width_2, x_pos_2, y_pos_2)[2]
                print "Standard Deviation of Noise #2:", std_noise_2

                std_noise = 0.5*(std_noise_1+std_noise_2)
                
                print "\nStandard Deviation of Noise:", std_noise
                ############################
            

                ### Enter primary star's information... ###
                print("\nPrimary Star Information: ")
                m_f = max_flux(image)
                use = raw_input("Use Information? (y/n): ")
    
                if use != 'y' and use != 'Y' and use != 'n' and use != 'N':
                    a = True
                    while a == True:
                        use = raw_input("Please enter (y/n): ")
                        if use == 'y' or use == 'Y' or use == 'n' or use == 'N':
                            a = False
                elif use == 'y' or use == 'Y':
                    x_pos_1 = float(m_f[0][0]) + 1
                    y_pos_1 = float(m_f[0][1]) + 1
                    print("\n--- Primary Star ---")
                    print("X Position #1: "+str(x_pos_1))
                    print("Y Position #1: "+str(y_pos_1))
                elif use == 'n' or use == 'N':
                    print("\nInsert values to verify star.")
                    print("--- Primary Star ---")
                    x_pos_1 = float(raw_input("X Position #1: "))
                    y_pos_1 = float(raw_input("Y Position #1: "))

                width_1 = float(raw_input("Enter width of box around primary star: "))
            
                # Find centroid for primary...
                x_cent_1 = centroid(image, width_1, x_pos_1, y_pos_1)[0]
                y_cent_1 = centroid(image, width_1, x_pos_1, y_pos_1)[1]
                print "Centroid of primary (x, y):", x_cent_1, y_cent_1
                # Fixed image without primary star...
#                img_fix_1 = centroid(image, width_1, x_cent_1, y_cent_1)[3]
                #image_full_fix_1 = image
#                image_full_fix_1[y_cent_1-(width_1/2):y_cent_1+(width_1/2),
#                x_cent_1-(width_1/2):x_cent_1+(width_1/2)] = img_fix_1
                
                # Write image for viewing...
#                print "Writing image with primary star removed..."
#                write_path = '/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/removed_star.fits'
#                fits.writeto(write_path, image_full_fix_1, clobber=True)
#                p_2 = subprocess.Popen(["/Applications/ds9.darwinmountainlion.7.2/ds9", '-log', '-zoom', 'to', '4', '-cmap', 'b', write_path])



                ### Enter companion star's information... ###
                print("\nInsert values to verify star.")
                print("--- Companion Star ---")
                x_pos_2 = float(raw_input("X Position #2: "))
                y_pos_2 = float(raw_input("Y Position #2: "))
                width_2 = float(raw_input("Enter width of box around companion star: "))

                # Find centroid for secondary...
                x_cent_2 = centroid(image, width_2, x_pos_2, y_pos_2)[0]
                y_cent_2 = centroid(image, width_2, x_pos_2, y_pos_2)[1]
                print "Centroid of companion (x, y):", x_cent_2, y_cent_2

                # Find aperature for companion...
                #p_range = float(raw_input("Number of pixels in range: "))
                aper_2 = aperature(image, x_cent_2, y_cent_2, std_noise)
                #max_rad_2 = aper_2[0][aper_2[2].index(max(aper_2[2]))]
                #max_flux_2 = aper_2[1][aper_2[2].index(max(aper_2[2]))]
                max_flux_2 = aper_2[0]                
                f2_std = aper_2[1]
                
                max_flux_out = aper_2[2]
                flux_out_std = aper_2[3]
                
                """
                flux_out_array = []
                radius_array = []
                for i in range(len(image[1])):
                    aper = aperature(image, x_cent_2, y_cent_2, std_noise, i)
                    flux_out_array.append(flux_ratio(max_flux_1, aper[2]))
                    radius_array.append(i)
                
                plt.plot(radius_array, flux_out_array)
                plt.show()
                """
                
                print "Max flux for companion: ", max_flux_2
                
                          
                
            

                # This section was created to handle the leakage affecting M409 & M42. #
                #print("\n--- Leakage Compensation #1 ---")
                #x_pos_3 = float(raw_input("X Position #1: "))
                #y_pos_3 = float(raw_input("Y Position #1: "))
                #flux_leak_1 = aperature(image, x_pos_3, y_pos_3, std_noise)[0]
                #print "Leakage Flux #1:", flux_leak_1
                
                #print("\n--- Leakage Compensation #2 ---")
                #x_pos_4 = float(raw_input("X Position #2: "))
                #y_pos_4 = float(raw_input("Y Position #2: "))
                #flux_leak_2 = aperature(image, x_pos_4, y_pos_4, std_noise)[0]
                #print "Leakage Flux #2:", flux_leak_2
                
                #flux_leak = 0.5 * (flux_leak_1 + flux_leak_2)
                #print "\nLeakage Flux:", flux_leak

                #max_flux_2 = max_flux_2 - flux_leak
                #print "Max flux fixed for companion:", max_flux_2

                #########################################################################



                file = pyfits.open(path)
                image = file[0].data
                
                # Find aperature for primary...
                aper_1 = aperature(image, x_cent_1, y_cent_1, std_noise)
                #max_rad_1 = max_rad_2
                max_flux_1 = aper_1[0]
                f1_std = aper_1[1]

                print "Max flux for primary: ", max_flux_1




                ### Final calculations... ###

                position = position_check(x_cent_1, y_cent_1, x_cent_2, y_cent_2)
                ang_sep = position[0]
                PA = position[1]
                
                print "\nStar #"+str(var+1)+":", name
                print "\nNoise STD:", std_noise
                print "\nAngular Seperation (arcsec)", ang_sep
                print 'Primary Angle (deg):', PA
                print 'Flux #1 / STD:', f1_std
                print 'Flux #2 / STD:', f2_std
                print "Primary Flux:", max_flux_1
                print "Companion Flux:", max_flux_2
                flux = flux_ratio(max_flux_1, max_flux_2)
                
                print "Flux Ratio:", flux
                
                comment = raw_input("\nComment?: ")
                #############################
                
                
                ### Store data... ###
                num_array = []
                num_array.append(var+1)
                n_array = []
                n_array.append(name)
                noise_array = []
                noise_array.append(std_noise)
                ang_array = []
                ang_array.append(ang_sep)
                PA_array = []
                PA_array.append(PA)
                f1_std_array = []
                f1_std_array.append(f1_std)
                f2_std_array = []
                f2_std_array.append(f2_std)
                m_f1_array = []
                m_f1_array.append(max_flux_1)
                m_f2_array = []
                m_f2_array.append(max_flux_2)
                flux_array = []
                flux_array.append(flux)
                com_array = []
                com_array.append(comment)
                
                np.savez('/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/final_stars_'+str(select),
                Number= num_array, Name= n_array, Noise= noise_array, Seperation= ang_array, Angle= PA_array, F_STD_1 = f1_std_array,
                F_STD_2 = f2_std_array, Flux_1= m_f1_array, Flux_2= m_f2_array, Flux= flux_array, Comment= com_array)
                ######################
                
                

                ### Checks to see if data verification is complete. ###
                finish = 1
                while finish == 1:
                    x = raw_input("\nNext Star? (y/n) ")
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
                        #p_2.terminate()
                        #p_3.terminate()
                        print('\n')
                    elif x == 'N' or x == 'n':
                        loop = 2
                        finish = 2
                        print('\nAll process are complete!')
                        p.terminate()
                        #p_2.terminate()
                        sys.exit()
                        #p_3.terminate()
                #######################################################
            elif skip == 'y' or skip == 'Y':
                loop = 1
                finish = 2
                var = var + 1
                p.terminate()
                #print('\n')              


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



def centroid(img, width, x_pos, y_pos):
    star_box = img[y_pos-(width/2):y_pos+(width/2), x_pos-(width/2):x_pos+(width/2)]
    
    x_weights = np.sum(star_box, axis = 0)
    x_vector = np.arange(len(star_box[1]))
    y_weights = np.sum(star_box, axis = 1)
    y_vector = np.arange(len(star_box[0]))
    
    x_centroid = np.sum(x_vector*x_weights)/np.sum(x_weights) + x_pos-(width/2)
    y_centroid = np.sum(y_vector*y_weights)/np.sum(y_weights) + y_pos-(width/2)
    
    std = np.std(star_box)
    
    gauss_img = gaussian_filter(star_box, 1)
    img_fix = (star_box - gauss_img)
    
    #print x_centroid, y_centroid
    
    return [x_centroid, y_centroid, std, img_fix]


def aperature(img, x_pos, y_pos, std, rad_out=0):
    flux_array = []
    count_array = []
    ratio_array = []
    rad_array = []
    std_array = []
    
    x_range = np.arange(len(img[1]))
    y_range = np.arange(len(img[0]))
    #rad_range = np.arange(start, radius, 0.5)
    
    # Changed Radius from 5.0 to 3.0
    rad = 3.0
    
    
    #print "\nRadius, Flux, Count, Area"   
    #for rad in rad_range:
    #    flux = 0
    #    count = 0
    #    for i in x_range:
    #        for j in y_range:
    #            r = np.sqrt((i-x_pos)**2 + (j-y_pos)**2)
    #            if r < rad:
    #                count = count + 1
    #                flux = (flux + img[j,i])
    
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

    gain = 9.0  # 9 electrons / ADU
    flux_to_std = flux/np.sqrt(flux/gain + count*std**2)
    flux_out_to_std = flux_outside/np.sqrt(flux_outside/gain + count_out*std**2)

    #    print rad, flux, count, np.pi*rad**2
    #    
    #    flux_array.append(flux)
    #    count_array.append(count)
        
    #    if flux == 0:
    #        rad_array.append(rad)
    #        ratio_array.append(flux)
    #        #std_array.append(flux)
    #    elif flux != 0:
    #        rad_array.append(rad)
    #        ratio_array.append(flux/np.sqrt(flux + count*std**2))
            #std_array.append(np.sqrt( (flux - flux/count)**2/count ))
    
    #print ratio_array
    #max_ratio = max(ratio_array)
    #max_rad = rad_array[ratio_array.index(max(ratio_array))]
    
    #plt.plot(rad_array, flux_array, linewidth=2, color='b')
    #plt.title('Flux', fontsize=20)
    #plt.show()
    
    #print max_ratio, max_rad
    #print count_array
    #flux_ratio = flux_array/count_array
    
    #plt.plot(rad_array, std_array, linewidth=1, color='b')
    #plt.show()
    
    #plt.plot(rad_array, ratio_array, linewidth=2, color='k')
    #plt.title('Flux / Total STD', fontsize=20)
    #plt.show()
    
    return [flux, flux_to_std, flux_outside, flux_out_to_std]
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


def reboot():
    # Reboot script.
    os.system("/Users/ppkantorski/Documents/Research/Stellar_Multiplicity/Code/Photometry/cent_aper.py")
    sys.exit()
    

if __name__ == '__main__':
	main()