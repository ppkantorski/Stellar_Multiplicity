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


def centroid(im, mask=None, w=None, x=None, y=None):
    """Compute the centroid of an image with a specified binary mask projected upon it.
    
    INPUT:
      im -- image array
      mask -- binary mask, 0 in ignored regions and 1 in desired regions
      w is typically 1.0/u**2, where u is the uncertainty on im
      x,y are those generated by meshgrid.

    OUTPUT:
      (x0,y0) tuple of centroid location"""
    from numpy import ones, arange, meshgrid
    # 2009-09-02 13:35 IJC: Created
    if mask==None:
        mask = ones(im.shape)
    if w==None:
        w = ones(im.shape)
    if not (im.shape==mask.shape and im.shape==w.shape):
        print "Image, mask, and weights must have same shape! Exiting."
        return -1
    if x==None or y==None:
        xx = arange(im.shape[1])
        yy = arange(im.shape[0])
        x,y = meshgrid(xx,yy)
    x0 = (x*im*mask*w).sum()/(im*mask*w).sum()
    y0 = (y*im*mask*w).sum()/(im*mask*w).sum()

    return (x0,y0)