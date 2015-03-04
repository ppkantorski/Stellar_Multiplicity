#!/usr/bin/env python

"""Python script for various photometry tasks.  See especially
:func:`aperphot`, for basic aperture photometry.  If you need
something fancier, try PyRAF, DAOPHOT, etc.
"""

# 2008-12-21 18:27 IJC: Created

import numpy as np
from numpy import ones, std, sum, mean, median, array, sign, nan, linalg, tile, concatenate, floor, Inf, arange, array, meshgrid, zeros, sin, cos, tan, arctan, sqrt, exp, nan, max, pi
import pdb
from pylab import find
from scipy import optimize


#try:
#    import psyco
#    psyco.full()
#except ImportError:
#    print 'Psyco not installed, the program will just run slower'

class phot:
    def __init__(self, **kw):
        """Generate a photometry object w/keywords and kw+'str' descriptive keywords

        Inputs cannot be numpy arrays"""
        # 2009-09-14 10:07 IJC: Created
        keylist = ['time', 'phot', 'ephot', 'bg', 'ebg', 'aper', 'position', 'eposition', \
            'ditherposition', 'object', 'filename', 'exptime', 'ra', 'dec']
        defaults = dict(photunit=None)
        for key in keylist:
            defaults[key]=None
            defaults[key+'str']=None
            keylist = keylist + [key+'str']
        for keyword in defaults:
            if (not kw.has_key(keyword)):
                kw[keyword] = defaults[keyword]

        for k in kw.keys():
            if kw[k].__class__==str:
                exec('self.'+k+'="'+str(kw[k]))+'"'
            else:
                exec('self.'+k+'='+str(kw[k]))
        self.comment = "Created by IJC's spitzer.phot"
        return 

 
def estbg(im, mask=None, bins=None, plotalot=False, rout=(3,200), badval=nan):
    """Estimate the background value of a masked image via histogram fitting.

    INPUTS:
      im -- numpy array.  Input image.

    OPTIONAL INPUTS:
      mask -- numpy array. logical mask, False/0 in regions to ignore
      bins -- sequence.  edges of bins to pass to HIST
      plotalot -- bool.  Plot the histogram and fit.
      rout -- 2-tuple of (nsigma, niter) for analysis.removeoutliers.
              Set to (Inf, 0) to not cut any outliers.
      badval -- value returned when things go wrong.

    OUTPUT:
      b, s_b -- tuple of (background, error on background) from gaussian fit.
                 Note that the error is analagous to the standard deviation on the mean

    COMMENTS:
      The fit parameters appear to be robust across a fairly wide range of bin sizes.  """
    # 2009-09-02 17:13 IJC: Created!
    # 2009-09-04 15:07 IJC: Added RemoveOutliers option. Use only non-empty bins in fit.
    # 2009-09-08 15:32 IJC: Error returned is now divided by sqrt(N) for SDOM
    # 2009-11-03 00:16 IJC: Improved guess for gaussian dispersion
    # 2011-05-18 11:47 IJMC: Moved (e)gaussian imports to analysis.
    # 2012-01-01 21:04 IJMC: Added badval option
    # 2012-08-15 17:45 IJMC: Numpy's new histogram no longer accepts 'new' keyword
    # 2013-03-20 08:22 IJMC: Now works better even for small numbers
    #                        of pixels; thanks to A. Weigel @
    #                        ETH-Zurich for catching this!

    from numpy import histogram, mean, median, sqrt, linspace, isfinite, ones,std
    from pylab import find
    from scipy import optimize
    #from analysis import removeoutliers, egaussian, gaussian, stdr
    if plotalot:
        from pylab import figure, errorbar, plot, colorbar, title, hist, mean, std
        ##from analysis import imshow

    def gaussianChiSquared(guess, x, y, err):
        return (egaussian(guess, x, y, e=err)**2).sum()


    if mask==None:
        mask = ones(im.shape)
    dat = im.ravel()[find(mask<>0)]
    if plotalot:
        figure(); plot(im.ravel()); plot(dat)
        print mean(dat), std(dat), rout[0]*std(dat)
        print len(dat), (abs(dat-mean(dat))<(rout[0]*std(dat))).sum()
        figure(); plot(dat-mean(dat)); 
        plot([0,len(dat)], [rout[0]*std(dat),rout[0]*std(dat)],'--k')
        plot([0,len(dat)], [-rout[0]*std(dat),-rout[0]*std(dat)],'--k')
    dat = removeoutliers(dat, rout[0], remove='both', center='mean', niter=rout[1], verbose=plotalot)
    ndat = len(dat)

    if ndat==0:
        print "No data to work with!"
        return (badval, badval)
    if bins==None:
        if plotalot: print "no bins entered!"
        datmean = dat.mean()
        datstd = stdr(dat, nsigma=3)
        nunique = len(np.unique(dat.ravel()))
        #pdb.set_trace()
        if nunique > len(dat)/20.:
            dobin = False
        else:
            dobin = True
            bins = linspace(dat.min(), dat.max(), nunique/2)

    if plotalot: 
        print "dat.mean, dat.std>>" + str((dat.mean(), dat.std()))


    #if plotalot:
    #    figure(); hout = hist(dat[datIndex],bins)
    #else:
    
    if dobin:
        binwidth = mean(bins[1::]-bins[:-1])
        bincenter = 0.5*(bins[1::]+bins[:-1])
        datIndex = (dat>=bins.min()) * (dat<=bins.max())
        hout = histogram(dat[datIndex], bins) #,new=True)
        gy = hout[0]
        erry = sqrt(gy)
        usableIndex = gy>0

        eff_binwidth = mean(bins[usableIndex][1::]-bins[usableIndex][:-1])
        guess = [gy.sum()*eff_binwidth, std(dat[datIndex]), median(dat[datIndex])]

        if 1.0*usableIndex.sum()/usableIndex.size < 0.5:
            out = guess
        else:
            out = optimize.fmin(gaussianChiSquared, guess, \
                                args=(bincenter[usableIndex],gy[usableIndex], erry[usableIndex]), \
                                disp=plotalot)

        if plotalot:
            from pylab import figure, errorbar, plot, colorbar, title
            from nsdata import imshow
            print 'guess>>',guess
            print 'fit>>',out
            figure()
            imshow(im); colorbar()
            figure()
            errorbar(bincenter[usableIndex], gy[usableIndex], erry[usableIndex], fmt='ob')
            plot(bincenter, gaussian(out, bincenter),'-r', linewidth=2)
            title('Mean: %f, Std. Dev.: %f' % (out[2], out[1]))

        ret = out[2], out[1]/sqrt(ndat)
    else:
        ret = datmean, datstd/sqrt(ndat)

    return  ret


def makemask(x,y,params, shape='circle'):
    """Generate a binary (logical) mask with given shape and location.

    INPUTS:
         x      = x-coodinate system (made with meshgrid)
         y      = y-coodinate system (made with meshgrid)
      params:
        shape='circle':
           params(1)  = x-offset
           params(2)  = y-offset
           params(3)  = x-diameter
           params(4)  = OPTIONAL y-diameter
        shape='quad':
           params: list of quadrants to include in the mask.  The
              midpoint for determining quadrants will be
              mid = (xmax+xmin)/2.  Quadrants are:
              0:   x<midX  and  y<midY
              1:   x<midX  and  y>=midY
              2:   x>=midX  and  y<midY
              3:   x>=midX  and  y>=midY

    OPTIONAL INPUTS:
        shape=:  desired mask shape.  Currently only 'circle' is valid.

    OUTPUTS:
      mask   = NxM grided representation of specified mask
                  where NxM are the size of the x,y input meshgrids

    EXAMPLE:
        x=arange(32); y=arange(64)
        xx,yy = meshgrid(x,y)
        m = makemask(xx,yy,(24, 53, 10))
        m[53,24]   # ----> True
        """
    # 2009-09-02 10:47 IJC: Created.  Adapted from Joe Green's MakeEllipse.m
    # 2009-09-27 13:37 IJC: Added 'quad' quadrant mask option.
    from numpy import zeros, bool

    if not x.shape==y.shape:
        print "x,y meshgrid coordinates must be the same shape! Exiting."
        return -1
    if shape=='circle':
        if len(params)<3:
            print "Must give at least 3 parameters to mask."
            return -1
        x0 = params[0]
        y0 = params[1]
        xdia =params[2]
        if len(params)==3:
            ydia = xdia
        else:
            ydia = params[3]
        mask = (  (((x-x0)/(xdia/2.))**2 + ((y-y0)/(ydia/2.))**2) < 1 )
    elif shape=='quad':
        midx = (x.max()+x.min())/2.
        midy = (y.max()+y.min())/2.
        mask = zeros(x.shape, bool)
        for ii in range(len(params)):
            if params[ii]==0:
                mask += (x<midx) * (y<midy)
            elif params[ii]==1:
                mask += (x<midx) * (y>=midy)
            elif params[ii]==2:
                mask += (x>=midx) * (y<midy)
            elif params[ii]==3:
                mask += (x>=midx) * (y>=midy)

    return mask

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


def lmcextinct(ra, dec, **kw):
    """Use the Zaritsky & Harris (ZH) map to get A_V extinction in the LMC.

    INPUT:
       ra  -- decimal degrees of right ascension
       dec -- decimal degrees of declination

    OPTIONAL INPUT:
       method='griddata'  /'nearest'  -- interpolation method
       map='both' /'hot'/'cool'       -- Which ZH map to use
       hot='lmc_hotav.fits'           -- filename of hot map
       cool='lmc_coolav.fits'         -- filename of cool map
       null=0.0                       -- "no data" value in map
       verbose=False / True           -- print out some spam and eggs

    EXAMPLE:
       ra = hms('05:51:56.6')
       dec = dms('-66:25:08.5')
       lmcextinct(ra, dec)
       
    If their map returns null, interpolate from the surroundings.

    Note that these calculations are definitely _not_ optimized.

    SEE ALSO:
       hms, dms"""

    # 2009-02-15 22:11 IJC: Created and tested.

    import pyfits
    from matplotlib.mlab import griddata
    from pylab import meshgrid, arange, array, sqrt, cos, sin, arctan2, arcsin

    ra = array([ra]).copy().ravel()
    dec = array([dec]).copy().ravel()

    defaults = dict(method='griddata', map='hot', hot='lmc_hotav_clean2.fits', 
                    cool='lmc_coolav.fits', null=0.0, verbose=False)

    for key in defaults:
        if (not kw.has_key(key)):
            kw[key] = defaults[key]
    
    if kw['map']=='both':
        kw['map'] = 'hot'
        ret1 = lmcextinct(ra, dec, **kw)
        kw['map'] = 'cool'
        ret2 = lmcextinct(ra, dec, **kw)
        return (ret1, ret2)
    else:
        map = kw[kw['map']]

    verbose = kw['verbose']

    avmap = pyfits.getdata(map)
    avhdr = pyfits.getheader(map)
    
    nx = avhdr['naxis1']
    ny = avhdr['naxis2']
    cx = avhdr['crpix1']
    cy = avhdr['crpix2']
    x0 = avhdr['crval1']
    y0 = avhdr['crval2']
    dx = avhdr['cd1_1']
    dy = avhdr['cd2_2']

    xx,yy = meshgrid(arange(nx),arange(ny))
    
    goodind = (avmap<>kw['null'])

    # I don't know how the following WCS calculation works, but it
    # does -- thank you, Calabretta & Greisen 2002!
    d2r = pi/180.

    phi = arctan2( xx-cx+1, yy-cy+1) + pi
    theta = arctan2(1./(d2r*dy), sqrt((yy-cy)**2 + (xx-cx)**2))
    mapdec = arcsin(sin(theta)*sin(y0*d2r) - cos(theta)*cos(phi)*cos(y0*d2r))/d2r
    mapra = arcsin(cos(theta) * sin(phi) / cos(mapdec*d2r))/d2r + x0

    if kw['method']=='griddata':
        ragood = mapra[goodind]
        decgood = mapdec[goodind]
        avgood = avmap[goodind]

    if verbose:
        print 'ra.shape>>' + str(ra.shape)
    
    # TBD: Vectorize this calculation; an interpolative solution
    # should exist.
    avlist = []
    for ii in range(len(ra)):
        if verbose:
            print 'ra, dec>>' + str((ra[ii], dec[ii]))
        if kw['method']=='nearest':
            distmap = (mapra-ra[ii])**2 + (mapdec-dec[ii])**2
            # If multiple values are equally near, average them:
            val = avmap[distmap==distmap.min()].mean()
            avlist.append(val)
        elif kw['method']=='griddata':
            avlist.append(griddata(ragood, decgood, avgood, array([ra[ii]]), array([dec[ii]])))
        else:
            print "Invalid method specified!"
            avlist.append(-1)
        
 
    return avlist
    


def readogle(filename, **kw):
    """ Read in an OGLE-II photometry map file and output the data.

    Returns a 6-tuple with each element an array:
       0  -- RA.  Strings of Right Ascension values.
       1  -- DEC.  Strings of Declination values
       2  -- x_ref.  OGLE x-coordinate, pixels
       3  -- y_ref.  OGLE y-coordinate, pixels
       4  -- v_mag.  OGLE V magnitude
       5  -- i_mag.  OGLE I magnitude

    If you like, use HMS and DMS to convert the RA and DEC values returned."""
    
    # 2008-12-21 18:53 IJC: Created

    f = open(filename, 'r')
    raw = f.readlines()
    f.close()

    nstars = len(raw)

    raw2 = array([line.split() for line in raw])
    ra = raw2[:,1]
    dec = raw2[:,2]
    xref = raw2[:,3]
    yref = raw2[:,4]
    vmag = raw2[:,5]
    imag = raw2[:,7]
    
    xref = [map(float, [x]) for x in xref]
    yref = [map(float, [y]) for y in yref]
    vmag = [map(float, [v]) for v in vmag]
    imag = [map(float, [i]) for i in imag]

    return (ra, dec, xref, yref, vmag, imag)


def hms(d, delim=':'):
    """Convert hours, minutes, seconds to decimal degrees, and back.

    EXAMPLES:

    hms('15:15:32.8')
    hms([7, 49])
    hms(18.235097)
    
    Also works for negative values.

    SEE ALSO:  dms
    """
    # 2008-12-22 00:40 IJC: Created
    # 2009-02-16 14:07 IJC: Works with spaced or colon-ed delimiters
    from numpy import sign

    if d.__class__==str or hasattr(d, '__iter__'):   # must be HMS
        if d.__class__==str:
            d = d.split(delim)
            if len(d)==1:
                d = d[0].split(' ')
            if (len(d)==1) and (d.find('h')>-1):
                d.replace('h',delim)
                d.replace('m',delim)
                d.replace('s','')
                d = d.split(delim)
        s = sign(float(d[0]))
        if s==0:  s=1
        degval = float(d[0])*15.0
        if len(d)>=2:
            degval = degval + s*float(d[1])/4.0
        if len(d)==3:
            degval = degval + s*float(d[2])/240.0
        return degval
    else:    # must be decimal degrees
        hour = int(d/15.0)
        d = abs(d)
        min = int((d-hour*15.0)*4.0)
        sec = (d-hour*15.0-min/4.0)*240.0
        return [hour, min, sec]


def dms(d, delim=':'):
    """Convert degrees, minutes, seconds to decimal degrees, and back.

    EXAMPLES:

    dms('150:15:32.8')
    dms([7, 49])
    dms(18.235097)
    
    Also works for negative values.

    SEE ALSO:  hms
    """
    # 2008-12-22 00:40 IJC: Created
    # 2009-02-16 14:07 IJC: Works with spaced or colon-ed delimiters
    from numpy import sign

    if d.__class__==str or hasattr(d, '__iter__'):   # must be HMS
        if d.__class__==str:
            d = d.split(delim)
            if len(d)==1:
                d = d[0].split(' ')
        s = sign(float(d[0]))
        if s==0:  s=1
        degval = float(d[0])
        if len(d)>=2:
            degval = degval + s*float(d[1])/60.0
        if len(d)==3:
            degval = degval + s*float(d[2])/3600.0
        return degval
    else:    # must be decimal degrees
        if d<0:  
            sgn = -1
        else:
            sgn = +1
        d = abs(d)
        deg = int(d)
        min = int((d-deg)*60.0)
        sec = (d-deg-min/60.0)*3600.0
        return [sgn*deg, min, sec]


def hess(color, mag, binsize, **kw):
    """Compute a hess diagram (surface-density CMD) on photometry data.

    INPUT:
       color  
       mag
       binsize -- width of bins, in magnitudes

    OPTIONAL INPUT:
       cbin=  -- set the centers of the color bins
       mbin=  -- set the centers of the magnitude bins

    OUTPUT:
       A 3-tuple consisting of:
         Cbin -- the centers of the color bins
         Mbin -- the centers of the magnitude bins
         Hess -- The Hess diagram array"""

    # cbin = out[0]
    # mbin = out[1]
    # imshow(out[2])
    # yticks(range(0, len(mbin), 4), mbin[range(0,len(mbin),4)])
    # xticks(range(0, len(cbin), 4), cbin[range(0,len(cbin),4)])
    # ylim([ylim()[1], ylim()[0]])

    # 2009-02-08 23:01 IJC: Created, on a whim, for LMC data (of course)
    # 2009-02-21 15:45 IJC: Updated with cbin, mbin options

    from numpy import arange, zeros

    defaults = dict(mbin=None, cbin=None, verbose=False)

    for key in defaults:
        if (not kw.has_key(key)):
            kw[key] = defaults[key]

    if kw['mbin']==None:
        mbin = arange(mag.min(), mag.max(), binsize)
    else:
        mbin = array(kw['mbin']).copy()
    if kw['cbin']==None:
        cbin = arange(color.min(), color.max(), binsize)
    else:
        cbin = array(kw['cbin']).copy()

    hess = zeros((len(mbin), len(cbin)), float)
    for ii in range(len(cbin)):
        cindex = (color<(cbin[ii]+binsize/2)) * (color>(cbin[ii]-binsize/2)) 
        for jj in range(len(mbin)):
            index = cindex * (mag<(mbin[jj]+binsize/2)) * (mag>(mbin[jj]-binsize/2)) 
            hess[jj,ii] = index.sum()


    return (cbin, mbin, hess)


def snr(mag=20, itime=1., read=24.5, sky=8.43, npix=24., zero=26.44, dark=0.0):
    """Calculate SNR of a photometric CCD observation of given parameters.

    The default keyword parameters are for the CTIO Blanco MOSAIC
    imager, operating in V band.
    """
    # 2009-02-20 14:40 IJC: Initiated
    
    star = itime * 10**(0.4*(zero-mag))
    noise = npix * (itime*(sky+dark)+read**2)

    return star * (star+noise)**-0.5
    
    

#def sens(texp, mag, npix, tdead=15., rn=8., csky=12., zp=22.8, z=1.0,h=1280., d=1.0):

def sens(texp, mag, lin=3.8e5, tdead=15., rn=8., csky=12., zp=22.8, z=1.0,h=1280., d=1.0):
    """ Calculate sensitiviy for various exposure times.

    texp -- 1D array of times
    mag -- target magnitude
    npix -- number of pixels read out
    
    lin -- linearity limit of the detector (ADU)
    tdead -- detector dead time (reset + readout) between integrations
    rn -- read noise, in ADU
    csky -- sky background per second, in ADU
    zp -- photometric zero point (magnitude for 1 ADU/sec)
    z -- airmass
    h -- observatory altitude, in meters
    d -- telescope mirror diameter, in meters

    TBD:  Flat-field noise!


    For now, I impose an artificial floor to the number of pixels
    needed -- it won't spread it out over less than 8.
    """

    # 2009-03-13 11:48 IJC: Written based on http://arxiv.org/abs/0903.2139

    from numpy import exp, log10, sqrt, floor

    texp = array(texp).copy()

    ctarg = 10**(0.4*(zp-mag))

    Ntarg = ctarg * texp
    npix = floor(Ntarg / (lin-csky))  # spread out the light
    pixind = npix<8
    npix[pixind] = 8

    Nsky = csky * texp * npix
    
    sScint = 0.004 * d**(-2./3.) * z**1.75 * exp(-h/8e3) * (2*texp)**-0.5
    
    sTarg = -2.5*log10((Ntarg - sqrt(Ntarg)) / Ntarg)
    sSky = -2.5*log10((Ntarg - sqrt(Nsky)) / Ntarg)
    sRON = -2.5*log10((Ntarg - rn*sqrt(npix)) / Ntarg)

    sTotal = sqrt(sScint**2 + sSky**2 + sRON**2)

    snrpertime = sTotal * sqrt(texp+tdead)

    return sTotal, snrpertime, npix

def subreg(fn, center=None, dim=None, verbose=False):
    """Load a subsection of a list of 2D FITS files.

    INPUTS:
       fn -- (str) filename or (list) list of filenames to load
       center -- (2-tuple) (x0,y0) center of region to load.
       dim -- (2-tuple) (dx,dy) sizes of region to load. 

    OUTPUT: 
       region -- (array) (N x dx x dy)-sized stack of subregions

    NOTE: center can also be a list of tuples (1 per file), but dim cannot."""
    # 2009-09-24 11:20 IJC: Created
    print "Function subreg is deprecated; please use subreg2 (which is much faster!)"

    import pyfits
    from numpy import zeros, nan, concatenate, int, float, max, min

    if not hasattr(fn, '__iter__'):
        fn = [fn]
    if not hasattr(dim, '__iter__'):
        dim = [dim, dim]

    nfiles = len(fn)
    if (center is None) and (dim is None):
        try:
            temp = pyfits.getdata(fn[0], ignore_missing_end=True)
        except:
            temp = pyfits.getdata(fn[0])
        dosubreg = False
        dim = list(temp.shape)
        center = dim[0]/2, dim[1]/2

    if not hasattr(center[0], '__iter__'):
        center = [center]*nfiles
    stack = zeros((0, dim[0], dim[1]), float)
    dim = [dim]*nfiles

    if verbose: print "fn, center, dim",(fn,center,dim)

    iter = 0
    for file, cen, sz in zip(fn, center, dim):
        if verbose: print "file, cen, sz", (file,cen,sz)
        try:
            temp = pyfits.getdata(file, ignore_missing_end=True)
        except:
            temp = pyfits.getdata(file)
        if verbose: print "file "+file+" shape is: "+str(temp.shape)
        if len(temp.shape)<>2:
            print "File %s did not return a 2D FITS file! Using nan." % file
            subreg = zeros((1,dx,dy))+nan
        else:
            temp = temp.reshape((1,)+temp.shape)
            xstartval = max([0,cen[0] - (sz[0]-1)/2.]).astype(int)
            xendval = min([temp.shape[1], 1+cen[0] + (sz[0]-1)/2.]).astype(int)
            ystartval = max([0,cen[1] - (sz[1]-1)/2.]).astype(int)
            yendval = min([temp.shape[2], 1+cen[1] + (sz[1]-1)/2.]).astype(int)
            if verbose: print "subregion limits: ", xstartval,xendval,ystartval,yendval
            subreg = temp[:,xstartval:xendval,ystartval:yendval]
        if file==fn[0] and stack.shape[1::]<>subreg.shape:
            stack = zeros((0,)+subreg.shape[1::],float)
        if verbose: 
            print "stack.shape>>", stack.shape
            print "subreg.shape>>", subreg.shape
        stack=concatenate((stack,subreg),0)
        iter += 1
            
    return stack
    

def subreg2(fn, center=None, dim=None, verbose=False):
    """Load a subsection of a list of 2D FITS files.

    INPUTS:
       fn -- str, list of str, or 2- or 3D Numpy array.
          i)   filename to load, OR
          ii)  list of filenames to load, OR
          iii) Numpy array of data, already loaded.

       center -- (2-tuple) (x0,y0) center of region to load.

       dim -- (2-tuple) (dx,dy) sizes of region to load. 

    OUTPUT: 
       region -- (array)
         (N x dx x dy)-sized stack of subregions.  Note that this will
         always be 3D!

    NOTE: center can also be a list of tuples (1 per file), but dim cannot."""
    # 2009-09-24 11:20 IJC: Created
    # 2011-12-15 15:53 IJMC: Updated to use memmap. MUCH faster!
    # 2012-06-16 06:57 IJMC: Now 'fn' can also be a Numpy array.

    import pyfits
    from numpy import zeros, nan, concatenate, int, float, max, min

    if not hasattr(fn, '__iter__'):
        fn = [fn]
    elif isinstance(fn, np.ndarray):
        if fn.ndim==3:
            nfiles = fn.shape[0]
        elif fn.ndim==2:
            fn = fn.reshape((1,)+fn.shape)

    nfiles = len(fn)

    if dim is not None and (not hasattr(dim, '__iter__')):
        dim = [dim, dim]

    if center is not None and (not hasattr(center[0], '__iter__')):
        center = [center]*nfiles

    if (center is None) and (dim is None):
        try:
            temp = pyfits.getdata(fn[0], ignore_missing_end=True)
        except:
            temp = pyfits.getdata(fn[0])
        dosubreg = False
        dim = list(temp.shape)
        center = dim[0]/2, dim[1]/2

    stack = zeros((0, dim[0], dim[1]), float)
    dim = [dim]*nfiles
    #center = [center]*nfiles

    if verbose: print "fn, center, dim",(fn,center,dim)

    iter = 0
    for file, cen, sz in zip(fn, center, dim):
        if verbose: print "file, cen, sz", (file,cen,sz)
        if isinstance(file, np.ndarray):
            f = file
        else:
            try:
                f = pyfits.open(file, ignore_missing_end=True, memmap=True)
            except:
                f = pyfits.open(file, memmap=True)
        #if verbose: print "file "+file+" shape is: "+str(temp.shape)
        #if len(temp.shape)<>2:
        #    print "File %s did not return a 2D FITS file! Using nan." % file
        #    subreg = zeros((1,dx,dy))+nan
        #else:
        if iter==0:
            if isinstance(f, np.ndarray):
                temp = f.reshape((1,) + f.shape)
            else:
                temp = f[0].data#.reshape([1]+dim[0])
                temp = temp.reshape((1,) + temp.shape)
            xstartval = max([0,cen[0] - (sz[0]-1)/2.]).astype(int)
            xendval = min([temp.shape[1], 1+cen[0] + (sz[0]-1)/2.]).astype(int)
            ystartval = max([0,cen[1] - (sz[1]-1)/2.]).astype(int)
            yendval = min([temp.shape[2], 1+cen[1] + (sz[1]-1)/2.]).astype(int)
            if verbose: print "subregion limits: ", xstartval,xendval,ystartval,yendval
            subreg = temp[0,xstartval:xendval,ystartval:yendval]
            stack = zeros((nfiles,) + subreg.shape, float)
        else:
            this_dy =  center[0][0] - center[iter][0]
            this_dx =  center[0][1] - center[iter][1]
            try:
                subreg = f[0].data[xstartval+this_dx:xendval+this_dx, \
                                       ystartval+this_dy:yendval+this_dy]
            except IndexError:
                print "Likely invalid center position for Frame %i (%s): %s." % \
                    (iter, file, str(center[iter]))
                print "Using offsets for Frame 0 (%s) instead." % str(center[0])
                subreg = f[0].data[xstartval:xendval, ystartval:yendval]
            except:
                print "Some error occurred. Using offsets for Frame 0 (%s) instead." % \
                    str(center[0])
                subreg = f[0].data[xstartval:xendval, ystartval:yendval]                

        stack[iter] = subreg
        iter += 1
            
    return stack
    



def aperphot(fn, timekey=None, pos=[0,0], dap=[2,4,6], mask=None, verbose=False, nanval=999, resamp=None, retfull=False):
    """Do aperture photometry on a specified file.

    :INPUTS:
      pos : 2-sequence
        center of apertures (as if indexing: fn[pos[0], pos[1]])
  
      dap : 3-sequence
        Photometry aperture DIAMETERS:
           -- target aperture (within which to sum flux)
           -- inner sky aperture
           -- outer sky aperture
  
      resamp : int
        Factor by which to interpolate frame before measuring photometry
        (in essence, does partial-pixel aperture photometry)
  
      Aperture masking:
         If no mask is passed in, use the star's input position and
         aperture diameters to create binary pixel masks for stellar and
         background photometry.  If a mask is passed in, stellar and
         background aperture masks are generated from where all input
         mask elements equal 1 and 2, respectively.
  
      retfull: 
          Also return arrays of target mask, sky mask, and frame used.
          This option is a memory hog!
  
    :OUTPUTS:  
      :class:`phot` object.  
  
    :EXAMPLE:  
      ::

        import astropy.io.fits
        from astropy import wcs
        import numpy as np
        from phot import aperphot

        img='62_z_CDFs_goods_stamp_img.fits'  #path to the image
        RA = 52.9898239
        DEC = -27.7143114
        hdulist = astropy.io.fits.open(img)
        w = wcs.WCS(hdulist['PRIMARY'].header)
        world = np.array([[RA, DEC]])
        pix = w.wcs_world2pix(world,1) # Pixel coordinates of (RA, DEC)
        print "Pixel Coordinates: ", pix[0,0], pix[0,1]

        #call aperture function
        observation=aperphot(img, timekey=None, pos=[pix[0,0], pix[0,1]], dap=[4,8,12], resamp=2, retfull=False)

        # Print outputs
        print "Aperture flux:", observation.phot
        print "Background:   ", observation.bg
  
  
    :REQUIREMENTS:
      scipy.interpolate, pyfits, numpy...
           """
    # 2009-09-14 10:49 IJC: Created
    # 2010-01-15 14:20 IJC: Added numpy "_string" check
    # 2011-12-29 12:01 IJMC: Added peak pixel values to photometry report.
    # 2012-01-25 11:26 IJMC: Adding "resamp" option -- thanks to
    #                        K. Stevenson and J. Harrington of UCF for
    #                        the suggestion.
    # 2012-02-26 11:53 IJMC: Now return 'ntarg' and 'nsky' -- number of pixels used.
    # 2012-06-07 08:27 IJMC: 'peak' values are now corrected for the
    #                        resampling factor.
    # 2012-07-03 10:35 IJMC: Fixed a key bug: frames were not
    #                        correctly background-subtracted when
    #                        applying partial-pixel resampling.
    # 2012-10-19 13:41 IJMC: Documented 'retfull' option; changed default.
    # 2013-03-20 09:21 IJMC: More error-checking for saving header
    #                        keywords.  Thanks to A. Weigel @
    #                        ETH-Zurich for catching this!

    from numpy import meshgrid, median,isfinite,sort,ndarray,string_
    import numpy as np
    import pyfits
    #from analysis import fixval
    from os import path
    from scipy import interpolate

    thisobs = phot()
    x0, y0 = pos
    dap_targ, dap_skyinner, dap_skyouter = dap
    if resamp is None or resamp<1:
        resamp = 1
    else:
        resamp = float(resamp)
        
    # Determine size:
    if isinstance(fn,str):
        nx = pyfits.getval(fn, 'NAXIS1')
        ny = pyfits.getval(fn, 'NAXIS2')
    elif isinstance(fn,ndarray):
        nx,ny = fn.shape

    nx0, ny0 = nx, ny
    nx = ((nx - 1)*resamp + 1.)  # Avoid resampling at pixel locations
    ny = ((ny - 1)*resamp + 1.)  #   outside the original boundaries.

    # Generate or load masks:
    if mask==None:
        xx,yy = meshgrid(np.arange(ny)/resamp, np.arange(nx)/resamp)
        mask_targ = makemask(xx, yy, (x0, y0, dap_targ))
        mask_s1 = makemask(xx, yy, (x0,y0, dap_skyinner))
        mask_s2 = makemask(xx, yy, (x0,y0, dap_skyouter))
        mask_sky = mask_s2 - mask_s1
    else:
        mask_targ = mask==1
        mask_sky = mask==2
        if resamp>1:
            print "In aperphot, resamp>1 and user-specified mask passed in... beware!"

    # Load data frame:
    thisobs = phot()
    if isinstance(fn,ndarray):
        frame = fn
    elif isinstance(fn, str) or isinstance(fn,string_):
        if not path.isfile(fn):
            print "file %s not found! exiting..." % fn
            return thisobs
        frame = pyfits.getdata(fn)
        fixval(frame, nanval)

    # Resample data frame
    if resamp>1:
        frame0 = frame.copy()
        xx0 = range(nx0)
        yy0 = range(ny0)
        x1,y1 = np.arange(nx)/resamp, np.arange(ny)/resamp
        rectspline = interpolate.fitpack2.RectBivariateSpline(xx0, yy0, frame0, kx=1, ky=1, s=0)
        frame = rectspline(x1, y1)

    #from pylab import *
    #pdb.set_trace()
    # Measure background and aperture photometry
    thisbg, thisebg = estbg(frame, mask=mask_sky, plotalot=verbose, rout=[3,99])
    thisphot = (mask_targ*(frame - thisbg)).sum() /resamp/resamp
    peak = frame.max()
    peak_targ = (mask_targ * frame).max()
    peak_annulus = (mask_sky * frame).max()

    thisobs.bg=thisbg
    thisobs.ebg=thisebg
    thisobs.bgstr='phot.estbg: SDOM on bg histogram mean & dispersion after outlier rejection'
    thisobs.phot=thisphot
    thisobs.photstr='by-hand background-subtracted aperture photometry'
    thisobs.ntarg = mask_targ.sum()/resamp/resamp
    thisobs.nsky = mask_sky.sum()/resamp/resamp

    thisobs.peak = peak
    thisobs.peak_targ = peak_targ
    thisobs.peak_annulus = peak_annulus
    thisobs.peakstr = 'peak pixel value in frame'
    thisobs.peak_targstr = 'peak pixel value in target aperture'
    thisobs.peak_annulusstr = 'peak pixel value in sky annulus'
    thisobs.position = pos
    thisobs.positionstr = 'user-specified, zero-indexed pixel coordinates.'
    if isinstance(fn, str):
        header = pyfits.getheader(fn)
        if not timekey==None:
            if timekey in header: 
                thisobs.time=header['timekey']
                thisobs.timestr='heliocentric modified julian date'
        if 'object' in header:  thisobs.object = header['object']
        if 'exptime' in header: thisobs.exptime = header['exptime']
    thisobs.aper = dap
    thisobs.aperstr = 'target, inner, outer aperture diameters, in pixels.'
    thisobs.filename=fn
    thisobs.resamp = resamp
    if retfull:
        thisobs.mask_targ = mask_targ
        thisobs.mask_sky  = mask_sky
        thisobs.frame = frame

    if verbose:
        from pylab import figure, colorbar
        from nsdata import imshow
        figure(); imshow(frame*mask_targ); colorbar()
        figure(); imshow(frame*mask_sky); colorbar()

    return thisobs

def psffiterr(xyoffset, psf, frame, w=None, scale=100, dframe=9, verbose=False):
    """ Usage:
          optimize.fmin_powell(psffiterr, [0,0], args=(psf, stack[6],goodind[6],100,13),xtol=0.5,ftol=1)
          """
    # 2009-11-13 11:27 IJC: Created
    from numpy import round
    import pdb
    out = psffit(psf, frame, loc=None, w=w, scale=scale, dframe=dframe, \
                     xoffs=[round(xyoffset[0])], yoffs=[round(xyoffset[1])], verbose=verbose)
    sumsqres = out[2][0,0]
    #pdb.set_trace()
    return sumsqres

def psffit(psf, frame, loc=None, w=None, scale=100, dframe=9, xoffs=range(0,100,10), yoffs=range(0,100,10), verbose=False):
    """
    INPUT:
       psf -- model PSF (supersampled by 'scale')
       frame -- science frame to which psf will be fit. best if it's odd-sized
       
    OPTIONAL INPUTS:
       loc -- (x,y) integers, star location in data frame (e.g., data[x,y])
       w -- [array] weights of pixels in data frame, (typ. 1/sigma^2)
       scale -- supersampling level of PSF
       dframe -- [odd int] diameter of square box around target location
       xoffs -- [int array] subpixel x offsets to test.  
       yoffs -- [int array] subpixel y offsets to test.  
    """
    # 2009-10-07 14:18 IJC: Created.
    # 2011-05-11 22:16 IJC: Added a try/except/pdb debugging step
    from numpy import arange, prod, zeros,vstack,dot, nonzero, diag,floor,abs,max,hstack
    from numpy.linalg import pinv
    #from analysis import binarray
    from time import time
    import pdb

    tic = time()

    
    if w==None:
        w = zeros(frame.shape)+1
    if loc==None:
        loc = ((frame.shape[1]-1)/2,(frame.shape[0]-1)/2)
    if xoffs==None:
        xoffsets = arange(scale) #arange(scale)
    if yoffs==None:
        yoffs = arange(scale) #arange(scale)

    ycen = int(loc[0])
    xcen = int(loc[1])
    pycen, pxcen = nonzero(psf==psf.max())
    # Pick a thumbnail frame size to use, and cut it out of the larger frame
    if verbose:
        print "frame.shape>>", frame.shape
        print "(xcen, ycen, dframe)>>", xcen,ycen,dframe
        print "limits>>" , (ycen-(dframe-1)/2.), (ycen+(dframe+1)/2.), (xcen-(dframe-1)/2.), (xcen+(dframe+1)/2.)
        print "xoffs, yoffs>>", xoffs, yoffs
    data = frame[(ycen-(dframe-1)/2.):(ycen+(dframe+1)/2.), 
                 (xcen-(dframe-1)/2.):(xcen+(dframe+1)/2.)]
    weights = w[(ycen-(dframe-1)/2.):(ycen+(dframe+1)/2.), 
                 (xcen-(dframe-1)/2.):(xcen+(dframe+1)/2.)]
    wmat = diag(weights.ravel())

    extrasize = 2*max(abs(floor(1.0*hstack((xoffs,yoffs))/scale)))
    exs = extrasize*scale/2
    if verbose: print "extrasize>> ",extrasize

    # Determine how much of the PSF to cut out, and cut it out
    dpsf0 = (dframe+1)*scale-1
    dpsf1 = dframe*scale-1
    pxmin = int(pxcen-(dpsf0-1)/2-exs)
    pxmax = int(pxcen+(dpsf0+1)/2+exs)
    pymin = int(pycen-(dpsf0-1)/2-exs)
    pymax = int(pycen+(dpsf0+1)/2+exs)
    if verbose: print psf.shape, pymin, pymax, pxmin, pxmax
    smpsf = psf[pymin:pymax, pxmin:pxmax]

    if verbose: print "data.shape>>" , data.shape
    ndata = prod(data.shape)
    if verbose: print "ndata>> %i" % ndata
    const = zeros(ndata,float)+1
    background = zeros((len(xoffs),len(yoffs)), float)
    fluxscale =  zeros((len(xoffs),len(yoffs)), float)
    chisq = zeros((len(xoffs),len(yoffs)), float)
    if verbose: 
        print "wmat.shape>>", wmat.shape
        print "data.ravel().shape>>", data.ravel().shape

    wpmat = dot(wmat, data.ravel()) # outside of loop for efficiency
    dfs = dframe * scale            # outside of loop for efficiency
    initoffset_min = scale - 1 + exs    # outside of loop for efficiency
    initoffset_max = scale - 1 + exs + dfs    # outside of loop for efficiency
    nx = len(xoffs)
    ny = len(yoffs)
    rangeny = range(ny)
    for ii in range(nx):
        xoffset = xoffs[ii]
        xmin, xmax = int(initoffset_min-xoffset), int(initoffset_max-xoffset)
        for jj in rangeny:
            #   Cut out the correct portion of the model PSF
            yoffset = yoffs[jj]
            ymin, ymax = int(initoffset_min-yoffset), int(initoffset_max-yoffset)
            #   Bin down the PSF by the correct factor.  Sizes should now match!
            binpsf = binarray(smpsf[ymin:ymax, xmin:xmax],scale)
            #   Compute the best-fit background & PSF scaling factor
            if verbose:
                print "xmat shapes>> ",const.shape, binpsf.ravel().shape
                print "ymin,ymax,xmin,xmax>> ",ymin,ymax, xmin,xmax
                print "binpsf.shape>> ",binpsf.shape
            try:
                xmat = vstack((const,binpsf.ravel())).transpose()
                wxmat = dot(wmat,xmat)
                fitvec = dot(pinv(wxmat), wpmat) 
                background[ii,jj], fluxscale[ii,jj] = fitvec
                chisq[ii,jj] = ((dot(wxmat, fitvec) - wpmat)**2).sum()
            except:
                print "error occurred"
                chisq[ii,jj] = 9e99
                pdb.set_trace()
                

    ii,jj = nonzero(chisq==chisq.min())
    if len(ii)>1: # more than one chisquared minimum found!
        ii = ii[0]
        jj = jj[0]
    xoffset = xoffs[ii]
    xmin, xmax = int(scale-xoffset-1+exs), int(scale-xoffset-1 + dfs+exs)
    yoffset = yoffs[jj]
    ymin, ymax = int(scale-yoffset-1+exs), int(scale-yoffset-1 + dfs+exs)
    #   Bin down the PSF by the correct factor.  Sizes should now match!
    binpsf = binarray(smpsf[ymin:ymax, xmin:xmax],scale)
    modelpsf = background[ii,jj]+fluxscale[ii,jj]*binpsf
    #print "%f seconds for completion!" % (time()-tic)
    return modelpsf, data, chisq, background, fluxscale, xoffset, yoffset, chisq[ii,jj],background[ii,jj], fluxscale[ii,jj]



def prffit(prf, frame, loc=None, w=None, scale=100, dframe=9, xoffs=range(0,100,10), yoffs=range(0,100,10), verbose=False):
    """
    INPUT:
       prf -- model PRF (supersampled by 'scale')
       frame -- science frame to which psf will be fit. best if it's odd-sized
       
    OPTIONAL INPUTS:
       loc -- (x,y) integers, star location in data frame (e.g., data[x,y])
       w -- [array] weights of pixels in data frame, (typ. 1/sigma^2)
       scale -- supersampling level of PSF
       dframe -- [odd int] diameter of square box around target location
       xoffs -- [int array] subpixel x offsets to test.  
       yoffs -- [int array] subpixel y offsets to test.  
    """
    # 2009-10-07 14:18 IJC: Created.
    from numpy import arange, prod, zeros,vstack,dot, nonzero, diag,floor,abs,max,hstack
    from numpy.linalg import pinv
    #from analysis import binarray
    from time import time
    tic = time()

    
    if w==None:
        w = zeros(frame.shape)+1
    if loc==None:
        loc = ((frame.shape[1]-1)/2,(frame.shape[0]-1)/2)
    if xoffs==None:
        xoffsets = arange(scale) #arange(scale)
    if yoffs==None:
        yoffs = arange(scale) #arange(scale)

    ycen = int(loc[0])
    xcen = int(loc[1])
    pycen, pxcen = nonzero(prf==prf.max())
    # Pick a thumbnail frame size to use, and cut it out of the larger frame
    if verbose:
        print "frame.shape>>", frame.shape
        print "(xcen, ycen, dframe)>>", xcen,ycen,dframe
        print "limits>>" , (ycen-(dframe-1)/2.), (ycen+(dframe+1)/2.), (xcen-(dframe-1)/2.), (xcen+(dframe+1)/2.)
    data = frame[(ycen-(dframe-1)/2.):(ycen+(dframe+1)/2.), 
                 (xcen-(dframe-1)/2.):(xcen+(dframe+1)/2.)]
    weights = w[(ycen-(dframe-1)/2.):(ycen+(dframe+1)/2.), 
                 (xcen-(dframe-1)/2.):(xcen+(dframe+1)/2.)]
    wmat = diag(weights.ravel())

    extrasize = 2*max(abs(floor(1.0*hstack((xoffs,yoffs))/scale)))
    exs = extrasize*scale/2
    if verbose: print "extrasize>> ",extrasize


    if verbose: print "data.shape>>" , data.shape
    ndata = prod(data.shape)
    if verbose: print "ndata>> %i" % ndata
    const = zeros(ndata,float)+1
    background = zeros((len(xoffs),len(yoffs)), float)
    fluxscale =  zeros((len(xoffs),len(yoffs)), float)
    chisq = zeros((len(xoffs),len(yoffs)), float)
    if verbose: 
        print "wmat.shape>>", wmat.shape
        print "data.ravel().shape>>", data.ravel().shape

    wpmat = dot(wmat, data.ravel()) # outside of loop for efficiency
    dfs = dframe * scale            # outside of loop for efficiency
    initoffset_min = scale - 1 + exs    # outside of loop for efficiency
    initoffset_max = scale - 1 + exs + dfs    # outside of loop for efficiency
    nx = len(xoffs)
    ny = len(yoffs)
    rangeny = range(ny)
    for ii in range(nx):
        xoffset = xoffs[ii]
        xmin, xmax = int(initoffset_min-xoffset), int(initoffset_max-xoffset)
        for jj in rangeny:
            #   Extract the correct indices of the model PRF. Sizes should now match!
            yoffset = yoffs[jj]
            ymin, ymax = int(initoffset_min-yoffset), int(initoffset_max-yoffset)
            binpsf = prf[indy, indx]
            #   Compute the best-fit background & PSF scaling factor
            if verbose and (ii==0) and (jj==0): 
                print "xmat shapes>> ",const.shape, binpsf.ravel().shape
                print "ymin,ymax,xmin,xmax>> ",ymin,ymax, xmin,xmax
                print "binpsf.shape>> ",binpsf.shape
            xmat = vstack((const,binpsf.ravel())).transpose()
            wxmat = dot(wmat,xmat)
            fitvec = dot(pinv(wxmat), wpmat) 
            background[ii,jj], fluxscale[ii,jj] = fitvec
            chisq[ii,jj] = ((dot(wxmat, fitvec) - wpmat)**2).sum()

    ii,jj = nonzero(chisq==chisq.min())
    if len(ii)>1: # more than one chisquared minimum found!
        ii = ii[0]
        jj = jj[0]
    xoffset = xoffs[ii]
    xmin, xmax = int(scale-xoffset-1+exs), int(scale-xoffset-1 + dfs+exs)
    yoffset = yoffs[jj]
    ymin, ymax = int(scale-yoffset-1+exs), int(scale-yoffset-1 + dfs+exs)
    #   Bin down the PSF by the correct factor.  Sizes should now match!
    binpsf = binarray(smpsf[ymin:ymax, xmin:xmax],scale)
    modelpsf = background[ii,jj]+fluxscale[ii,jj]*binpsf
    print "%f seconds for completion!" % (time()-tic)
    return modelpsf, data, chisq, background, fluxscale, xoffset, yoffset, chisq[ii,jj],background[ii,jj], fluxscale[ii,jj]


def gauss2d(param, x, y):
    """ Compute a gaussian distribution at the points x, y.

        p is a three- or four-component array, list, or tuple:

        z =  [p4 +] p0/(p1*sqrt(4pi)) * exp(-r**2 / (2*p1**2))

             where r = sqrt((x-p2)**2 + (y-p3)**2)

        p[0] -- Volume under the gaussian
        p[1] -- one-sigma dispersion
        p[2] -- X- offset of center 
        p[3] -- Y- offset of center
        p[4] -- optional constant, vertical offset

        x & y must be equal-sized arrays from numpy.meshgrid

        NOTE: FWHM = 2*sqrt(2*ln(2)) * p1  ~ 2.3548*p1

        SEE ALSO: egauss2d, numpy.meshgrid"""
    #2010-01-11 22:46 IJC: Created
    from numpy import array, abs, concatenate, exp
    x = array(x, dtype=float).copy()
    y = array(y, dtype=float).copy()
    p = array(param).copy()

    r = abs((x-p[2]) + 1j*(y-p[3]))

    if len(p)==4:
        p = concatenate((p, [0]))

    z = p[4] + p[0]/(p[1]*4*pi) * exp(-r**2 / (2*p[1]**2))
    
    return z
    

def egauss2d(param, x, y, z, ez=None):
    """ Return the chi-squared error on a 2D gaussian fit.  See gauss2d
        for more details on the input parameters.

        z is the array of data to be fit
        ez is an optional array of one-sigma errors to the data in z.
        """
    # 2010-01-11 22:59 IJC: Created
    from numpy import array, float, ones
    x = array(x, dtype=float).copy()
    y = array(y, dtype=float).copy()
    z = array(z, dtype=float).copy()
    p = array(param).copy()
    if ez==None:
        ez = ones(z.shape,float)
    else:
        ez = array(ez, dtype=float).copy()        

    model = gauss2d(param,x,y)
    chisq = (((z-model)/ez)**2).sum()
    return chisq
    
    
    
    



c   = 299792458  # speed of light, m/s
h = 6.626068e-34 # SI units: Planck's constant
k = 1.3806503e-23 # SI units: Boltzmann constant, J/K
G = 6.67300e-11 # SI units: Gravitational constant
sigma = 5.670373e-8 # SI units: Stefan-Boltzmann constant

qe = 1.602176565e-19 # Electron charge, in Coulombs
me = 9.11e-31  # electron mass, in kg
ev = 1.602176565e-19 # electron Volt, in Joules
amu = 1.66053886e-27 # atomic mass unit, in kg
mh = 1.008 * amu # mass of hydrogen atom, in kg

pi  = 3.14159265358979
AU  = 149597870691.0  # AU in meters
day = 86400.0  # seconds in a Julian Day
rsun = 6.95508e8  # Solar mean radius, in m
msun = 1.9891e30  # solar mass in kg
rearth = 6.378136e6 # Earth's equatorial radius in m; [Allen's]
mearth = 5.9737e24 # in kg; [Allen's]
rjup = 7.1492e7 # Jupiter equatorial radius in m
mjup = 1898.7e24  # Jupiter mass in kg
pc = 3.08568025e16 # parsec in meters



class planet:
    """Very handy planet object.

    Best initialized using :func:`getobj`.

    :REQUIREMENTS: Database file `exoplanets.csv` from http://exoplanets.org/

    """
    # 2010-03-07 22:21 IJC: Created
    # 2011-01-22 17:15 IJMC: Updated format b/c CPS folks keep changing
    #                       their database file format

    # 2011-05-19 16:11 IJMC: Updated format b/c CPS folks keep
    #                       changing their database file format -- but
    #                       it's almost worth it to finally have
    #                       stellar radii.
    def __init__(self, *args):
        keys = ['name','comp','ncomp','mult','discmeth','firstref','firsturl','date','jsname','etdname','per','uper','t0','ut0','ecc','uecc','ueccd','om','uom','k','uk','msini','umsini','a','ua','orbref','orburl','transit','t14','ut14','tt','utt','ar','uar','uard','i','ui','uid','b','ub','ubd','depth','udepth','udepthd','r','ur','density','udensity','gravity','ugravity','transitref','transiturl','trend','dvdt','udvdt','freeze_ecc','rms','chi2','nobs','star','hd','hr','hipp','sao','gl','othername','sptype','binary','v','bmv','j','h','ks','ra','dec','ra_string','dec_string','rstar', 'urstar', 'urstard', 'rstarref', 'rstarurl','mstar','umstar','umstard','teff','uteff','vsini','uvsini','fe','ufe','logg','ulogg','shk','rhk','par','upar','distance','udistance','lambd', 'ulambd', 'massref','massurl','specref','specurl','distref','disturl','simbadname','nstedid','binaryref', 'binaryurl']

        if len(keys)<>len(args):
            print "Incorrect number of input arguments (%i, but should be %i)" % (len(args), len(keys))
            return None

        for key,arg in zip(keys, args):
            try:
                temp = float(arg)+1
                isnumber = True
            except:
                isnumber = False
                

            if isnumber:
                exec('self.%s=%s' % (key,arg) )
            else:
                exec('self.%s="%s"' % (key,arg) )

        return None


    def get_t23(self, *args):
        """Compute full transit duration (in days) for a transiting planet.

        Returns:
           nan if required fields are missing.

        Using Eq. 15 of J. Winn's chapter in S. Seager's book "Exoplanets." 

        :SEE ALSO:
          :func:`get_t14`
          """ 
        # 2011-06-21 12:53 IJMC: Created

        # Get necessary parameters:
        per, ra, k, b, inc, ecc, om = self.per, 1./self.ar, sqrt(self.depth), self.b, self.i, self.ecc, self.om

        inc *= np.pi/180.
        om *= np.pi/180.

        ret = 0.

        # Check that no parameters are empty:
        if per=='' or k=='':
            ret = nan

        if b=='':
            try:
                b = (cos(inc)/ra) * (1. - ecc**2) / (1. + ecc * sin(om))
            except:
                ret = nan
        elif ra=='':
            try:
                ra = (cos(inc)/b) * (1. - ecc**2) / (1. + ecc * sin(om))
            except:
                ret = nan
        elif inc=='':
            try:
                inc = np.arccos((b * ra) / ((1. - ecc**2) / (1. + ecc * sin(om))))
            except:
                ret = nan
        
        if np.isnan(ret):
            print "Could not compute t_23.  Parameters are:"
            print "period>>", per
            print "r_*/a>>", ra
            print "r_p/r_*>>", k
            print "impact parameter (b)>>", b
            print "inclination>>", inc*180./np.pi, " deg"
            print "eccentricity>>", ecc
            print "omega>>", om*180./np.pi, " deg"
        else:
            ret = (per/np.pi) * np.arcsin(ra * np.sqrt((1. - k)**2 - b**2) / np.sin(inc))

        return ret



    def get_t14(self, *args):
        """Compute total transit duration (in days) for a transiting planet.

        Returns:
           nan if required fields are missing.

        Using Eq. 14 of J. Winn's chapter in S. Seager's book "Exoplanets." 

        :SEE ALSO:
          :func:`get_t23`
          """ 
        # 2011-06-21 12:53 IJMC: Created

        # Get necessary parameters:
        per, ra, k, b, inc, ecc, om = self.per, 1./self.ar, sqrt(self.depth), self.b, self.i, self.ecc, self.om

        inc *= np.pi/180.
        om *= np.pi/180.

        ret = 0.

        # Check that no parameters are empty:
        if per=='' or k=='':
            ret = nan

        if b=='':
            try:
                b = (cos(inc)/ra) * (1. - ecc**2) / (1. + ecc * sin(om))
            except:
                ret = nan
        elif ra=='':
            try:
                ra = (cos(inc)/b) * (1. - ecc**2) / (1. + ecc * sin(om))
            except:
                ret = nan
        elif inc=='':
            try:
                inc = np.arccos((b * ra) / ((1. - ecc**2) / (1. + ecc * sin(om))))
            except:
                ret = nan
        
        if np.isnan(ret):
            print "Could not compute t_14.  Parameters are:"
            print "period>>", per
            print "r_*/a>>", ra
            print "r_p/r_*>>", k
            print "impact parameter (b)>>", b
            print "inclination>>", inc*180./np.pi, " deg"
            print "eccentricity>>", ecc
            print "omega>>", om*180./np.pi, " deg"
        else:
            ret = (per/np.pi) * np.arcsin(ra * np.sqrt((1. + k)**2 - b**2) / np.sin(inc))

        return ret



    def get_teq(self, ab, f, reterr=False):
        """Compute equilibrium temperature.

        :INPUTS:
          ab : scalar, 0 <= ab <= 1
            Bond albedo.

          f : scalar, 0.25 <= ab <= 2/3.
            Recirculation efficiency.  A value of 0.25 indicates full
            redistribution of incident heat, while 2/3 indicates zero
            redistribution.

        :EXAMPLE:
           ::

               import analysis
               planet = analysis.getobj('HD 189733 b')
               planet.get_teq(0.0, 0.25) # zero albedo, full recirculation

        :REFERENCE:
           S. Seager, "Exoplanets," 2010.  Eq. 3.9
        """
        # 2012-09-07 16:24 IJMC: Created

        return self.teff/np.sqrt(self.ar) * (f * (1. - ab))**0.25


    def rv(self, **kw):
        """Compute radial velocity on a planet object for given Julian Date.

        :EXAMPLE:
           ::

               import analysis
               p = analysis.getobj('HD 189733 b')
               jd = 2400000.
               print p.rv(jd)
        
        refer to function `analysis.rv` for full documentation.

        SEE ALSO: :func:`analysis.rv`, :func:`analysis.mjd`
        """
        return rv(self, **kw)


    def rveph(self, jd):
        """Compute the most recently elapsed RV emphemeris of a given
        planet at a given JD.  RV ephemeris is defined by the having
        radial velocity equal to zero.
        
        refer to  :func:`analysis.rv` for full documentation.
        
        SEE ALSO: :func:`analysis.getobj`, :func:`analysis.phase`
        """
        return rveph(self, jd)


    def phase(self, hjd):
        """Get phase of an orbiting planet.

        refer to function `analysis.getorbitalphase` for full documentation.

        SEE ALSO: :func:`analysis.getorbitalphase`, :func:`analysis.mjd`
        """
        # 2009-09-28 14:07 IJC: Implemented object-oriented version
        return getorbitalphase(self, hjd)



    def writetext(self, filename, **kw):
        """See :func:`analysis.planettext`"""
        
        return planettext(self, filename, **kw)


def loaddata(filelist, path='', band=1):
    """Load a set of reduced spectra into a single data file.

   datalist  = ['file1.fits', 'file2.fits']
   datapath = '~/data/'

   data = loaddata(datalist, path=datapath, band=1)


   The input can also be the name of an IRAF-style file list.
   """
    # 2008-07-25 16:26 IJC: Created
    # 2010-01-20 12:58 IJC: Made function work for IRTF low-res data.
    #                       Replaced 'warn' command with 'print'.
    # 2011-04-08 11:42 IJC: Updated; moved inside analysis.py.
    # 2011-04-12 09:57 IJC: Fixed misnamed imports

    import pyfits

    data = array([])

    if filelist.__class__==str or isinstance(filelist,np.string_):
        filelist = ns.file2list(filelist)
    elif filelist.__class__<>list:
        print('Input to loaddata must be a python list or string')
        return data

    num = len(filelist)

    # Load one file just to get the dimensions right.
    irspec = pyfits.getdata(filelist[0])

    ii = 0
    for element in filelist:
        irspec = pyfits.getdata(element)

        if ii==0:
            irsh = irspec.shape
            data  = zeros((num,)+irsh[1::], float)
            
        if len(irsh)>2:
            for jj in range(irsh[1]):
                data[ii, jj, :] = irspec[band-1, jj, :]
        else:
            data[ii,:] = irspec[band-1,:]

        ii=ii+1

    return data



def getobj(*args, **kw):
    """Get data for a specified planet.  

       :INPUTS:  (str) -- planet name, e.g. "HD 189733 b"

       :OPTIONAL INPUTS:  
           datafile : str 
                datafile name

           verbose : bool
                verbosity flag                          

       :EXAMPLE:
           ::

                   p = getobj('55cnce')
                   p.period   ---> 2.81705

       The attributes of the returned object are many and varied, and
       can be listed using the 'dir' command on the returned object.

       This looks up data from the local datafile, which could be out
       of date.

       SEE ALSO: :func:`rv`"""
    # 2008-07-30 16:56 IJC: Created
    # 2010-03-07 22:24 IJC: Updated w/new exoplanets.org data table! 
    # 2010-03-11 10:01 IJC: If planet name not found, return list of
    #                       planet names.  Restructured input format.
    # 2010-11-01 13:30 IJC: Added "import os"
    # 2011-05-19 15:56 IJC: Modified documentation.

    import os

    if kw.has_key('datafile'):
        datafile=kw['datafile']
    else:
        datafile=os.path.expanduser('~/python/exoplanets.csv')
    if kw.has_key('verbose'):
        verbose = kw['verbose']
    else:
        verbose=False

    if len(args)==0:
        inp = 'noplanetname'
    else:
        inp = args[0]

    if verbose:  print "datafile>>" + datafile
    f = open(datafile, 'r')
    data = f.readlines()
    f.close()
    data = data[1::]  # remove header line
    names = array([line.split(',')[0] for line in data])

    foundobj = (names==inp)
    if (not foundobj.any()):
        if verbose: print "could not find desired planet; returning names of known planets"
        return names
    else:
        planetind = int(find(foundobj))
        pinfo  = data[planetind].strip().split(',')
        myplanet = planet(*pinfo)
        
    return myplanet
 


def getorbitalphase(planet, hjd, **kw):
    """Get phase of an orbiting planet.
    
    INPUT: 
       planet  -- a planet from getobj; e.g., getobj('55cnce')
       hjd

    OUTPUT:
       orbital phase -- from 0 to 1.

    NOTES: 
       If planet.transit==True, phase is based on the transit time ephemeris.  
       If planet.transit==False, phase is based on the RV ephemeris as
          computed by function rveph
    

    SEE ALSO:  :func:`getobj`, :func:`mjd`, :func:`rveph`
    """

    hjd = array(hjd).copy()
    if bool(planet.transit)==True:
        thiseph = planet.tt
    else:
        thiseph = planet.rveph(hjd.max())

    orbphase = ((hjd - thiseph) ) / planet.per
    orbphase -= int(orbphase.mean())

    return orbphase


def mjd(date):
    """Convert Julian Date to Modified Julian Date, or vice versa.

    if date>=2400000.5, add 2400000.5
    if date<2400000.5, subtract 2400000.5
    """
    # 2009-09-24 09:54 IJC: Created 

    date = array(date, dtype=float, copy=True, subok=True)
    offset = 2400000.5
    if (date<offset).all():
        date += offset
    elif (date>=offset).all():
        date -= offset
    else:
        print "Input contains date both below and above %f" % offset

    return date


def rveph(p, jd):
    """Compute the most recently elapsed RV emphemeris of a given
    planet at a given JD.  RV ephemeris is defined by the having
    radial velocity equal to zero.



        :EXAMPLE:
            ::

                #from analysis import getobj, rveph
                jd = 2454693            # date: 2008/08/14
                p  = getobj('55cnce')   # planet: 55 Cnc e
                t = rveph(p, jd)
            
            returns t ~ 


        SEE ALSO: :func:`getobj`, :func:`phase`
        """
    # 2009-12-08 11:20 IJC: Created.  Ref: Beauge et al. 2008 in
    #    "Extrasolar Planets," R. Dvorak ed.
    # 2010-03-12 09:34 IJC: Updated for new planet-style object.

    from numpy import cos, arccos, arctan, sqrt, tan, pi, sin, int

    if p.__class__<>planet:
        raise Exception, "First input must be a 'planet' object."
    
    omega = p.om*pi/180 
    tau = p.t0
    ecc = p.ecc
    per = p.per
    f = arccos(-ecc * cos(omega)) - omega  # true anomaly
    u = 2.*arctan(sqrt((1-ecc)/(1+ecc))*tan(f/2.)) # eccentric anomaly
    n = 2*pi/per

    time0 = tau+ (u-ecc*sin(u))/n
    norb = int((time0-jd)/per)
    time = time0-norb*per
    return time



def rv(p, jd=None, e=None, reteanom=False, tol=1e-8):
    """ Compute unprojected astrocentric RV of a planet for a given JD in m/s.
    
        :INPUTS:
          p : planet object, or 5- or 6-sequence
            planet object: see :func:`get_obj`

           OR:

            sequence: [period, t_peri, ecc, a, long_peri, gamma]
                      (if gamma is omitted, it is set to zero)
                      (long_peri should be in radians!)

          jd : NumPy array
            Dates of observation (in same time system as t_peri).

          e : NumPy array
            Eccentric Anomaly of observations (can be precomputed to
            save time)

        :EXAMPLE:
            ::

                jd = 2454693            # date: 2008/08/14
                p  = getobj('55 Cnc e')   # planet: 55 Cnc e
                vp = rv(p, jd)
            
            returns vp ~ 1.47e5  [m/s]

        The result will need to be multiplied by the sine of the
        inclination angle (i.e., "sin i").  Positive radial velocities
        are directed _AWAY_ from the observer.

        To compute the barycentric radial velocity of the host star,
        scale the returned values by the mass ratio -m/(m+M).

        SEE ALSO: :func:`getobj`, :func:`rvstar`
    """
    # 2008-08-13 12:59 IJC: Created with help from Debra Fischer,
    #    Murray & Dermott, and Beauge et al. 2008 in "Extrasolar
    #    Planets," R. Dvorak ed.
    # 2008-09-25 12:55 IJC: Updated documentation to be more clear.
    # 2009-10-01 10:25 IJC: Moved "import" statement within func.
    # 2010-03-12 09:13 IJC: Updated w/new planet-type objects
    # 2012-10-15 17:20 IJMC: First input can now be a list of
    #                        elements.  Added option to pass in
    #                        eccentric anomaly.
    
    jd = array(jd, copy=True, subok=True)
    if jd.shape==():  
        singlevalueinput = True
        jd = array([jd])
    else:
        singlevalueinput = False
    if ((jd-2454692) > 5000).any():
        raise Exception, "Implausible Julian Date entered."

    if hasattr(p, '__iter__'):
        if len(p)==5:
            per, tau, ecc, a, omega = p
            gamma = 0.
        else:
            per, tau, ecc, a, omega, gamma = p[0:6]
        if ecc > 1:  # Reset eccentricity directly
            ecc = 1. - tol
            p[2] = ecc
        elif ecc < 0:
            ecc = np.abs(ecc)
            p[2] = ecc
    else:
        if p.__class__<>planet:
            raise Exception, "First input must be a 'planet' object."
        try:
            per = p.per
            tau = p.t0
            ecc = p.ecc
            a   = p.a
            omega = p.om * pi/180.0
        except:
            raise Exception, "Could not load all desired planet parameters."

    if ecc < 0:
        ecc = np.abs(ecc)
    if ecc > 1:
        ecc = 1. - tol

    if e is None:
        n = 2.*pi/per    # mean motion
        m = n*(jd - tau) # mean anomaly
        e = []
        for element in m: # compute eccentric anomaly
            def kep(e): return element - e + ecc*sin(e)
            e.append(optimize.brentq(kep, element-1, element+1,  xtol=tol, disp=False))
            #e.append(optimize.newton(kep, 0, tol=tol))
    else:
        pass

    e = array(e, copy=False)
    f = 2. * arctan(  sqrt((1+ecc)/(1.-ecc)) * tan(e/2.)  )
    #r = a*(1-ecc*cos(e))
    #x = r*cos(f)
    #y = r*sin(f)

    K = n * a / sqrt(1-ecc**2)

    vz = -K * ( cos(f+omega) + ecc*cos(omega) )
    vzms = vz * AU/day  # convert to m/s

    if singlevalueinput:
        vzms = vzms[0]

    if reteanom:
        ret = vzms, e
    else:
        ret = vzms
    return ret




def rvstar(p, jd=None, e=None, reteanom=False, tol=1e-8):
    """ Compute radial velocity of a star which has an orbiting planet.

        :INPUTS:
          p : planet object, or 5- or 6-sequence
            planet object: see :func:`get_obj`

           OR:

            sequence: [period, t_peri, ecc, K, long_peri, gamma]
                      (if gamma is omitted, it is set to zero)

          jd : NumPy array
            Dates of observation (in same time system as t_peri).

          e : NumPy array
            Eccentric Anomaly of observations (can be precomputed to
            save time)

        :EXAMPLE:
            ::

                jd = 2454693            # date: 2008/08/14
                p  = getobj('55 Cnc e')   # planet: 55 Cnc e
                vp = rv(p, jd)

          Positive radial velocities are directed _AWAY_ from the
          observer.

        :SEE_ALSO: :func:`rv`, :func:`getobj`
    """
    # 2012-10-15 22:34 IJMC: Created from function 'rv'

    jd = array(jd, copy=True, subok=True)
    if jd.shape==():  
        singlevalueinput = True
        jd = array([jd])
    else:
        singlevalueinput = False
    if ((jd-2454692) > 5000).any():
        raise Exception, "Implausible Julian Date entered."

    if hasattr(p, '__iter__'):
        if len(p)==5:
            per, tau, ecc, k, omega = p
            gamma = 0.
        else:
            per, tau, ecc, k, omega, gamma = p[0:6]
        omega *= np.pi/180.
        if ecc < 0:
            ecc = np.abs(ecc)
            p[2] = ecc
        elif ecc > 1:
            ecc = 1. - tol
            p[2] = ecc

    else:
        if p.__class__<>planet:
            raise Exception, "First input must be a 'planet' object."
        try:
            per = p.per
            tau = p.t0
            ecc = p.ecc
            k   = p.k
            omega = p.om * pi/180.0
            gamma = 0.
        except:
            raise Exception, "Could not load all desired planet parameters."

    if ecc < 0:
        ecc = np.abs(ecc)
    if ecc > 1:
        ecc = 1. - tol

    if e is None:
        n = 2.*pi/per    # mean motion
        m = n*(jd - tau) # mean anomaly
        e = np.zeros(m.shape)
        for ii,element in enumerate(m): # compute eccentric anomaly
            def kep(e): return element - e + ecc*sin(e)
            e[ii] = optimize.brentq(kep, element-1, element+1,  xtol=tol, disp=False)
            #e.append(optimize.newton(kep, 0, tol=tol))
    else:
        pass

    # Compute true anomaly:
    f = 2. * arctan(  sqrt((1+ecc)/(1.-ecc)) * tan(e/2.)  )
    
    vrstar = k * (np.cos(f + omega) + ecc*np.cos(omega)) + gamma

    if singlevalueinput:
        vrstar = vrstar[0]

    if reteanom:
        ret = vrstar, e
    else:
        ret = vrstar

    return ret




def dopspec(starspec, planetspec, starrv, planetrv, disp, starphase=[], planetphase=[], wlscale=True):
    """ Generate combined time series spectra using planet and star
    models, planet and star RV profiles.

    D = dopspec(sspec, pspec, sRV, pRV, disp, sphase=[], pphase=[])

    :INPUTS:
       sspec, pspec:  star, planet spectra; must be on a common
                         logarithmic wavelength grid 
       sRV, pRV:      star, planet radial velocities in m/s
       disp:          constant logarithmic dispersion of the wavelength 
                         grid: LAMBDA_i/LAMBDA_(i-1)

    :OPTIONAL INPUTS:
       sphase, pphase:  normalized phase functions of star and planet.  
                           The inputs sspec and pspec will be scaled
                           by these values for each observation.
       wlscale:         return relative wavelength scale for new data

    NOTE: Input spectra must be linearly spaced in log wavelength and increasing:
            that is, they must have [lambda_i / lambda_(i-1)] = disp =
            constant > 1
          Positive velocities are directed AWAY from the observer."""

#2008-08-19 16:30 IJC: Created

# Options: 1. chop off ends or not?  2. phase function. 
#   4. Noise level 5. telluric? 6. hold star RV constant


# Initialize:
    starspec   = array(starspec  ).ravel()
    planetspec = array(planetspec).ravel()
    starrv     = array(starrv    ).ravel()
    planetrv   = array(planetrv  ).ravel()

    ns = len(starspec)
    nr = len(starrv)

    starphase   = array(starphase  ).ravel()
    planetphase = array(planetphase).ravel()
    if len(starphase)==0:
        starphase = ones(nr, float)
    if len(planetphase)==0:
        planetphase = ones(nr, float)
    

# Check inputs: 
    if ns<>len(planetspec):
        raise Exception, "Star and planet spectra must be same length."
    if nr<>len(planetrv):
        raise Exception, "Star and planet RV profiles must be same length."

    logdisp = log(disp)

# Calculate wavelength shift limits for each RV point
    sshift = ( log(1.0+starrv  /c) / logdisp ).round() 
    pshift = ( log(1.0+planetrv/c) / logdisp ).round() 

    limlo =  int( concatenate((sshift, pshift)).min() )
    limhi =  int( concatenate((sshift, pshift)).max() )

    ns2 = ns + (limhi - limlo)

    data = zeros((nr, ns2), float)

# Iterate over RV values, constructing spectra
    for ii in range(nr):
        data[ii, (sshift[ii]-limlo):(ns+sshift[ii]-limlo)] = \
            starphase[ii] * starspec
        data[ii, (pshift[ii]-limlo):(ns+pshift[ii]-limlo)] = \
            data[ii, (pshift[ii]-limlo):(ns+pshift[ii]-limlo)] + \
            planetphase[ii] * planetspec

    if wlscale:
        data = (data, disp**(arange(ns2) + limlo))
    return data




def loadatran(filename, wl=True, verbose=False):
    """ Load ATRAN atmospheric transmission data file.

        t = loadatran(filename, wl=True)

        INPUT: 
           filename -- filename of the ATRAN file.  This should be an
                       ASCII array where the second column is
                       wavelength and the third is the atmospheric
                       transmission.
                     (This can also be a list of filenames!)  
           
        :OPTIONAL INPUT: 
           wl -- if True (DEFAULT) also return the wavelength scale.
                 This can take up to twice as long for large files.

        RETURNS:
           if wl==True:   returns a 2D array, with columns [lambda, transmission]
           if wl==False:  returns a 1D Numpy array of the transmission
           
           NOTE: A list of these return values is created if
                 'filename' is actually an input list."""
    # 2008-08-21 09:42 IJC: Created to save myself a bit of time
    # 2008-08-25 10:08 IJC: Read in all lines at once; should go
    #                        faster with sufficient memory
    # 2008-09-09 13:56 IJC: Only convert the wavelength and flux
    #                        columns(#1 & #2) -- speed up slightly.
    if filename.__class__==list:
        returnlist = []
        for element in filename:
            returnlist.append(loadatran(element, wl=wl))
        return returnlist
    
    f = open(filename, 'r')
    dat = f.readlines()
    f.close()
    if verbose:
        print dat[0]
        print dat[0].split()
        print dat[0].split()[1:3]
        print dat[0].split()[2]
    
    if wl:
        data = array([map(float, line.split()[1:3]) for line in dat])
    else:
        data = array([float(line.split()[2]) for line in dat])

    return data


def poly2cheby(cin):
    """Convert straight monomial coefficients to chebychev coefficients.

    INPUT: poly coefficients (e.g., for use w/polyval)
    OUTPUT: chebyt coefficients

    SEE ALSO: :func:`gpolyval`; scipy.special.chebyt
    """
    # 2009-07-07 09:41 IJC: Created
    from scipy.special import poly1d, chebyt
    
    cin = poly1d(cin)
    cout = []

    ord = cin.order
    for ii in range(ord+1):
        chebyii = chebyt(ord-ii)
        cout.append(cin.coeffs[0]/chebyii.coeffs[0])
        cin -= chebyii*cout[ii]

    return cout


def cheby2poly(cin):
    """Convert  chebychev coefficients to 'normal' polyval coefficients .

    :INPUT: chebyt coefficients 

    :OUTPUT: poly coefficients (e.g., for use w/polyval)

    :SEE ALSO: :func:`poly2cheby`, :func:`gpolyval`; scipy.special.chebyt
    """
    # 2009-10-22 22:19 IJC: Created
    from scipy.special import poly1d, chebyt
    
    cin = poly1d(cin)
    cout = poly1d(0)

    ord = cin.order
    for ii in range(ord+1):
        cout += chebyt(ii)*cin[ii]

    return cout



def gpolyval(c,x, mode='poly', retp=False):
    """Generic polynomial evaluator.

    INPUT:
            c (1D array) -- coefficients of polynomial to evaluate,
                          from highest-order to lowest.
            x (1D array) -- pixel values at which to evaluate C

    OPTINAL INPUTS:
            MODE='poly' -- 'poly' uses standard monomial coefficients
                            as accepted by, e.g., polyval.  Other
                            modes -- 'cheby' (1st kind) and 'legendre'
                            (P_n) -- convert input 'x' to a normalized
                            [-1,+1] domain
            RETP=False  -- Return coefficients as well as evaluated poly.

    OUTPUT:
            y -- array of shape X; evaluated polynomial.  
            (y, p)  (if retp=True)

    SEE ALSO:  :func:`poly2cheby`

     """
    # 2009-06-17 15:42 IJC: Created 
    # 2011-12-29 23:11 IJMC: Fixed normalization of the input 'x' array
    from scipy import special
    from numpy import zeros, polyval, concatenate


    c = array(c).copy()
    nc = len(c)

    if mode=='poly':
        totalcoef = c
        ret = polyval(totalcoef, x)
    elif mode=='cheby':
        x = 2. * (x - 0.5*(x.max() + x.min())) / (x.max() - x.min())
        totalcoef = special.poly1d([0])
        for ii in range(nc):
            totalcoef += c[ii]*special.chebyt(nc-ii-1)
        ret = polyval(totalcoef, x)
    elif mode=='legendre':
        x = 2. * (x - 0.5*(x.max() + x.min())) / (x.max() - x.min())
        totalcoef = special.poly1d([0])
        for ii in range(nc):
            totalcoef += c[ii]*special.legendre(nc-ii-1)
        ret = polyval(totalcoef, x)

    if retp:
        return (ret, totalcoef)
    else:
        return ret
    return -1


def stdr(x, nsigma=3, niter=Inf, finite=True, verbose=False, axis=None):
    """Return the standard deviation of an array after removing outliers.
    
    :INPUTS:
      x -- (array) data set to find std of

    :OPTIONAL INPUT:
      nsigma -- (float) number of standard deviations for clipping
      niter -- number of iterations.
      finite -- if True, remove all non-finite elements (e.g. Inf, NaN)
      axis -- (int) axis along which to compute the mean.

    :EXAMPLE:
      ::

          from numpy import *
          #from analysis import stdr
          x = concatenate((randn(200),[1000]))
          print std(x), stdr(x, nsigma=3)
          x = concatenate((x,[nan,inf]))
          print std(x), stdr(x, nsigma=3)

    SEE ALSO: :func:`meanr`, :func:`medianr`, :func:`removeoutliers`, 
              :func:`numpy.isfinite`
    """
    # 2010-02-16 14:57 IJC: Created from mear
    # 2010-07-01 14:06 IJC: ADded support for higher dimensions
    from numpy import array, isfinite, zeros, swapaxes

    x = array(x, copy=True)
    xshape = x.shape
    ndim =  len(xshape)
    if ndim==0:
        return x

    if  ndim==1 or axis is None:
        # "1D" array
        x = x.ravel()
        if finite:
            x = x[isfinite(x)]
        x = removeoutliers(x, nsigma, niter=Inf, verbose=verbose)
        return x.std()
    else:
        newshape = list(xshape)
        oldDimension = newshape.pop(axis) 
        ret = zeros(newshape, float)

        # Prevent us from taking the action along the axis of primary incidices:
        if axis==0: 
            x=swapaxes(x,0,1)

        if axis>1:
            nextaxis = axis-1
        else:
            nextaxis = 0

        for ii in range(newshape[0]):
            #print 'x.shape>>',x.shape, 'newshape>>',newshape, 'x[ii].shape>>',x[ii].shape, 'ret[ii].shape>>',ret[ii].shape,'ii>>',ii
            ret[ii] = stdr(x[ii], nsigma=nsigma,niter=niter,finite=finite,\
                                 verbose=verbose, axis=nextaxis)
        return ret



def meanr(x, nsigma=3, niter=Inf, finite=True, verbose=False,axis=None):
    """Return the mean of an array after removing outliers.
    
    :INPUTS:
      x -- (array) data set to find mean of

    :OPTIONAL INPUT:
      nsigma -- (float) number of standard deviations for clipping
      niter -- number of iterations.
      finite -- if True, remove all non-finite elements (e.g. Inf, NaN)
      axis -- (int) axis along which to compute the mean.

    :EXAMPLE:
      ::

          from numpy import *
          #from analysis import meanr
          x = concatenate((randn(200),[1000]))
          print mean(x), meanr(x, nsigma=3)
          x = concatenate((x,[nan,inf]))
          print mean(x), meanr(x, nsigma=3)

    SEE ALSO: :func:`medianr`, :func:`stdr`, :func:`removeoutliers`, 
              :func:`numpy.isfinite`
    """
    # 2009-10-01 10:44 IJC: Created
    # 2010-07-01 13:52 IJC: Now handles higher dimensions.
    from numpy import array, isfinite, zeros, swapaxes

    x = array(x, copy=True)
    xshape = x.shape
    ndim =  len(xshape)
    if ndim==0:
        return x

    if  ndim==1 or axis is None:
        # "1D" array
        x = x.ravel()
        if finite:
            x = x[isfinite(x)]
        x = removeoutliers(x, nsigma, niter=Inf, verbose=verbose)
        return x.mean()
    else:
        newshape = list(xshape)
        oldDimension = newshape.pop(axis) 
        ret = zeros(newshape, float)

        # Prevent us from taking the mean along the axis of primary incidices:
        if axis==0: 
            x=swapaxes(x,0,1)

        if axis>1:
            nextaxis = axis-1
        else:
            nextaxis = 0

        for ii in range(newshape[0]):
            #print 'x.shape>>',x.shape, 'newshape>>',newshape, 'x[ii].shape>>',x[ii].shape, 'ret[ii].shape>>',ret[ii].shape,'ii>>',ii
            ret[ii] = meanr(x[ii], nsigma=nsigma,niter=niter,finite=finite,\
                                 verbose=verbose, axis=nextaxis)
        return ret
            
        



def medianr(x, nsigma=3, niter=Inf, finite=True, verbose=False,axis=None):
    """Return the median of an array after removing outliers.
    
    :INPUTS:
      x -- (array) data set to find median of

    :OPTIONAL INPUT:
      nsigma -- (float) number of standard deviations for clipping
      niter -- number of iterations.
      finite -- if True, remove all non-finite elements (e.g. Inf, NaN)
      axis -- (int) axis along which to compute the mean.

    :EXAMPLE:
      ::

          from numpy import *
          #from analysis import medianr
          x = concatenate((randn(200),[1000]))
          print median(x), medianr(x, nsigma=3)
          x = concatenate((x,[nan,inf]))
          print median(x), medianr(x, nsigma=3)

    SEE ALSO: :func:`meanr`, :func:`stdr`, :func:`removeoutliers`, 
              :func:`numpy.isfinite`
    """
    # 2009-10-01 10:44 IJC: Created
    #2010-07-01 14:04 IJC: Added support for higher dimensions
    from numpy import array, isfinite, zeros, median, swapaxes

    x = array(x, copy=True)
    xshape = x.shape
    ndim =  len(xshape)
    if ndim==0:
        return x

    if  ndim==1 or axis is None:
        # "1D" array
        x = x.ravel()
        if finite:
            x = x[isfinite(x)]
        x = removeoutliers(x, nsigma, niter=Inf, verbose=verbose)
        return median(x)
    else:
        newshape = list(xshape)
        oldDimension = newshape.pop(axis) 
        ret = zeros(newshape, float)

        # Prevent us from taking the action along the axis of primary incidices:
        if axis==0: 
            x=swapaxes(x,0,1)

        if axis>1:
            nextaxis = axis-1
        else:
            nextaxis = 0

        for ii in range(newshape[0]):
            #print 'x.shape>>',x.shape, 'newshape>>',newshape, 'x[ii].shape>>',x[ii].shape, 'ret[ii].shape>>',ret[ii].shape,'ii>>',ii
            ret[ii] = medianr(x[ii], nsigma=nsigma,niter=niter,finite=finite,\
                                 verbose=verbose, axis=nextaxis)
        return ret

        
    

def amedian(a, axis=None):
    """amedian(a, axis=None)

    Median the array over the given axis.  If the axis is None,
    median over all dimensions of the array.  

    Think of this as normal Numpy median, but preserving dimensionality.

    """
#    2008-07-24 14:12 IJC: Copied from
#         http://projects.scipy.org/scipy/numpy/ticket/558#comment:3,
#         with a few additions of my own (i.e., keeping the same
#         dimensionality).
#  2011-04-08 11:49 IJC: Moved to "analysis.py"

    sorted = array(a, subok=True, copy=True)

    if axis==None:
        return median(sorted.ravel())

    ash  = list(sorted.shape)
    ash[axis] = 1

    sorted = np.rollaxis(sorted, axis)
    
    sorted.sort(axis=0)
    
    index = int(sorted.shape[0]/2)
    
    if sorted.shape[0] % 2 == 1:
        returnval = sorted[index]
    else:
        returnval = (sorted[index-1]+sorted[index])/2.0
     
    return returnval.reshape(ash)




def polyfitr(x, y, N, s, fev=100, w=None, diag=False, clip='both', \
                 verbose=False, plotfit=False, plotall=False, eps=1e-13, catchLinAlgError=False):
    """Matplotlib's polyfit with weights and sigma-clipping rejection.

    :DESCRIPTION:
      Do a best fit polynomial of order N of y to x.  Points whose fit
      residuals exeed s standard deviations are rejected and the fit is
      recalculated.  Return value is a vector of polynomial
      coefficients [pk ... p1 p0].

    :OPTIONS:
        w:   a set of weights for the data; uses CARSMath's weighted polynomial 
             fitting routine instead of numpy's standard polyfit.

        fev:  number of function evaluations to call before stopping

        'diag'nostic flag:  Return the tuple (p, chisq, n_iter)

        clip: 'both' -- remove outliers +/- 's' sigma from fit
              'above' -- remove outliers 's' sigma above fit
              'below' -- remove outliers 's' sigma below fit

        catchLinAlgError : bool
          If True, don't bomb on LinAlgError; instead, return [0, 0, ... 0].

    :REQUIREMENTS:
       :doc:`CARSMath`

    :NOTES:
       Iterates so long as n_newrejections>0 AND n_iter<fev. 


     """
    # 2008-10-01 13:01 IJC: Created & completed
    # 2009-10-01 10:23 IJC: 1 year later! Moved "import" statements within func.
    # 2009-10-22 14:01 IJC: Added 'clip' options for continuum fitting
    # 2009-12-08 15:35 IJC: Automatically clip all non-finite points
    # 2010-10-29 09:09 IJC: Moved pylab imports inside this function
    # 2012-08-20 16:47 IJMC: Major change: now only reject one point per iteration!
    # 2012-08-27 10:44 IJMC: Verbose < 0 now resets to 0
    # 2013-05-21 23:15 IJMC: Added catchLinAlgError

    from CARSMath import polyfitw
    from numpy import polyfit, polyval, isfinite, ones
    from numpy.linalg import LinAlgError
    from pylab import plot, legend, title

    if verbose < 0:
        verbose = 0

    xx = array(x, copy=False)
    yy = array(y, copy=False)
    noweights = (w==None)
    if noweights:
        ww = ones(xx.shape, float)
    else:
        ww = array(w, copy=False)

    ii = 0
    nrej = 1

    if noweights:
        goodind = isfinite(xx)*isfinite(yy)
    else:
        goodind = isfinite(xx)*isfinite(yy)*isfinite(ww)
    
    xx2 = xx[goodind]
    yy2 = yy[goodind]
    ww2 = ww[goodind]

    while (ii<fev and (nrej<>0)):
        if noweights:
            p = polyfit(xx2,yy2,N)
            residual = yy2 - polyval(p,xx2)
            stdResidual = std(residual)
            clipmetric = s * stdResidual
        else:
            if catchLinAlgError:
                try:
                    p = polyfitw(xx2,yy2, ww2, N)
                except LinAlgError:
                    p = np.zeros(N+1, dtype=float)
            else:
                p = polyfitw(xx2,yy2, ww2, N)

            p = p[::-1]  # polyfitw uses reverse coefficient ordering
            residual = (yy2 - polyval(p,xx2)) * np.sqrt(ww2)
            clipmetric = s

        if clip=='both':
            worstOffender = abs(residual).max()
            if worstOffender <= clipmetric or worstOffender < eps:
                ind = ones(residual.shape, dtype=bool)
            else:
                ind = abs(residual) <= worstOffender
        elif clip=='above':
            worstOffender = residual.max()
            if worstOffender <= clipmetric:
                ind = ones(residual.shape, dtype=bool)
            else:
                ind = residual < worstOffender
        elif clip=='below':
            worstOffender = residual.min()
            if worstOffender >= -clipmetric:
                ind = ones(residual.shape, dtype=bool)
            else:
                ind = residual > worstOffender
        else:
            ind = ones(residual.shape, dtype=bool)
    
        xx2 = xx2[ind]
        yy2 = yy2[ind]
        if (not noweights):
            ww2 = ww2[ind]
        ii = ii + 1
        nrej = len(residual) - len(xx2)
        if plotall:
            plot(x,y, '.', xx2,yy2, 'x', x, polyval(p, x), '--')
            legend(['data', 'fit data', 'fit'])
            title('Iter. #' + str(ii) + ' -- Close all windows to continue....')

        if verbose:
            print str(len(x)-len(xx2)) + ' points rejected on iteration #' + str(ii)

    if (plotfit or plotall):
        plot(x,y, '.', xx2,yy2, 'x', x, polyval(p, x), '--')
        legend(['data', 'fit data', 'fit'])
        title('Close window to continue....')

    if diag:
        chisq = ( (residual)**2 / yy2 ).sum()
        p = (p, chisq, ii)

    return p



def spliner(x, y, k=3, sig=5, s=None, fev=100, w=None, clip='both', \
                 verbose=False, plotfit=False, plotall=False, diag=False):
    """Matplotlib's polyfit with sigma-clipping rejection.

    Do a scipy.interpolate.UnivariateSpline of order k of y to x.
     Points whose fit residuals exeed s standard deviations are
     rejected and the fit is recalculated.  Returned is a spline object.

     Iterates so long as n_newrejections>0 AND n_iter<fev. 

     :OPTIONAL INPUTS:
        err:   a set of errors for the data
        fev:  number of function evaluations to call before stopping
        'diag'nostic flag:  Return the tuple (p, chisq, n_iter)
        clip: 'both' -- remove outliers +/- 's' sigma from fit
              'above' -- remove outliers 's' sigma above fit
              'below' -- remove outliers 's' sigma below fit
     """
    # 2010-07-05 13:51 IJC: Adapted from polyfitr
    from numpy import polyfit, polyval, isfinite, ones
    from scipy import interpolate
    from pylab import plot, legend, title

    xx = array(x, copy=True)
    yy = array(y, copy=True)
    noweights = (w==None)
    if noweights:
        ww = ones(xx.shape, float)
    else:
        ww = array(w, copy=True)

    #ww = 1./err**2

    ii = 0
    nrej = 1

    goodind = isfinite(xx)*isfinite(yy)*isfinite(ww)
    
    #xx = xx[goodind]
    #yy = yy[goodind]
    #ww = ww[goodind]

    while (ii<fev and (nrej<>0)):
        spline = interpolate.UnivariateSpline(xx[goodind],yy[goodind],w=ww[goodind],s=s,k=k)
        residual = yy[goodind] - spline(xx[goodind])
        stdResidual = std(residual)
        #if verbose: print stdResidual
        if clip=='both':
            ind =  abs(residual) <= (sig*stdResidual) 
        elif clip=='above':
            ind = residual < sig*stdResidual
        elif clip=='below':
            ind = residual > -sig*stdResidual
        else:
            ind = ones(residual.shape, bool)

        goodind *= ind
        #xx = xx[ind]
        #yy = yy[ind]
        #ww = ww[ind]

        ii += 1
        nrej = len(residual) - len(xx)
        if plotall:
            plot(x,y, '.', xx[goodind],yy[goodind], 'x', x, spline(x), '--')
            legend(['data', 'fit data', 'fit'])
            title('Iter. #' + str(ii) + ' -- Close all windows to continue....')

        if verbose:
            print str(len(x)-len(xx[goodind])) + ' points rejected on iteration #' + str(ii)

    if (plotfit or plotall):
        plot(x,y, '.', xx[goodind],yy[goodind], 'x', x, spline(x), '--')
        legend(['data', 'fit data', 'fit'])
        title('Close window to continue....')

    if diag:
        chisq = ( (residual)**2 / yy )[goodind].sum()
        spline = (spline, chisq, ii, goodind)

    return spline




def neworder(N):
    """Generate a random order the integers [0, N-1] inclusive.

    """
    #2009-03-03 15:15 IJC: Created
    from numpy import random, arange, int
    from pylab import find

    neworder = arange(N)
    random.shuffle(neworder)

    #print N

    return  neworder
    


def im2(data1, data2, xlab='', ylab='', tit='', bar=False, newfig=True, \
            cl=None, x=[], y=[], fontsize=16):
    """Show two images; title will only be drawn for the top one."""
    from pylab import figure, subplot, colorbar, xlabel, ylabel, title, clim
    from nsdata import imshow

    if newfig:  figure()
    subplot(211)
    imshow(data1,x=x,y=y); 
    if clim<>None:   clim(cl)
    if bar:  colorbar()
    xlabel(xlab, fontsize=fontsize); ylabel(ylab, fontsize=fontsize)
    title(tit)

    subplot(212)
    imshow(data2,x=x,y=y); 
    if clim<>None:   clim(cl)
    if bar:  colorbar()
    xlabel(xlab, fontsize=fontsize); ylabel(ylab, fontsize=fontsize)

    return


def dumbconf(vec, sig, type='central', mid='mean', verbose=False):
    """
    Determine two-sided and one-sided confidence limits, using sorting.

    :INPUTS:
      vec : sequence
        1D Vector of data values, for which confidence levels will be
        computed.

      sig : scalar
        Confidence level, 0 < sig < 1. If type='central', we return
        the value X for which the range (mid-X, mid+x) encloses a
        fraction sig of the data values.

    :OPTIONAL INPUTS:
       type='central' -- 'upper', 'lower', or 'central' confidence limits
       mid='mean'  -- compute middle with mean or median

    :EXAMPLES:
       ::

           from numpy import random
           #from analysis import dumbconf
           x = random.randn(10000)
           dumbconf(x, 0.683)    #  --->   1.0  (one-sigma)
           dumbconf(3*x, 0.954)  #  --->   6.0  (two-sigma)
           dumbconf(x+2, 0.997, type='lower')   #  --->   -0.74
           dumbconf(x+2, 0.997, type='upper')   #  --->    4.7

    
    Some typical values for a Normal (Gaussian) distribution:

       type     confidence level
       ----     ----------------
      one-sigma	   0.6826895
      2 sigma	   0.9544997
      3 sigma	   0.9973002
      4 sigma	   0.9999366
      5 sigma	   0.9999994
    """
    #2009-03-25 22:47 IJC: A Better way to do it (using bisector technique)
    # 2009-03-26 15:37 IJC: Forget bisecting -- just sort.
    # 2013-04-25 12:05 IJMC: Return zero if vector input is empty.
    # 2013-05-15 07:30 IJMC: Updated documentation.
    from numpy import sort, array

    vec = array(vec).copy()
    sig = array([sig]).ravel()
    if vec.size==0: return array([0])

    #vec = sort(vec)
    N = len(vec)
    Ngoal = sig*N

    if mid=='mean':
        mid = vec.mean()
    elif mid=='median':
        mid = median(vec)
    else:
        try:
            mid = mid + 0.0
        except MidMethodException:
            print "mid must be median, mean, or numeric in value!"
            return -1
    
    if type =='central':
        vec2 = sort(abs(vec-mid))
    elif type=='upper':
        vec2 = sort(vec)
    elif type=='lower':
        vec2 = -sort(-vec)
    else:
        print "Invalid type -- must be central, upper, or lower"
        return -1
    
    ret = []
    for ii in range(len(sig)):
        ret.append(vec2[int(Ngoal[ii])])
    return ret



def error_dropoff(data):
    """   Calculates the dropoff in measurement uncertainty with increasing
    number of samples (a random and uncorrelated set of data should
    drop of as 1/sqrt[n] ).  

    E(0), the first returned element, always returns the uncertainty
    in a single measurement (i.e., the standard deviation).
    
    :EXAMPLE: Compute the errors on an array of 3 column vectors
       ::

           data = randn(1000,3)
           e = error_dropoff(data)
           plot(e[1], 1./sqrt(e[1]), '-', e[1], e[0], 'x')
           xlim([0,30])
           legend(['Theoretical [1/sqrt(N)]', 'Computed errors'])
    """
    # 2009-05-05 08:58 IJC: Adapted to Python from Matlab.
    # 2006/06/06 IJC: Made it work with arrays of column vectors.
    #                 Added the '--nomean' option.
    
    
# PARSE INPUTS
    data = array(data).copy()
    
#interval = max([1 round(extract_from_options('--interval=', 1, options))]);
    
    
    if len(data)==len(data.ravel()):
        data = data.ravel()
        data = data.reshape(len(data),1)
    
    nsets = data.shape[1]
    npts_vec = arange(data.shape[0]/2)+1.0
    errors = zeros((data.shape[0]/2, nsets))
 
# LOOP AND CALCULATE STUFF
    for ii in range(len(npts_vec)):
        npts = npts_vec[ii]  # number of points we average over
        nsamp = floor(data.shape[0]/npts) # number of subsamples
        dre = reshape(data[0:nsamp*npts,:], (npts, nsamp, nsets))
        error_values = std(dre.mean(1))
        errors[ii,:] = error_values
        
    return (errors, npts_vec)



def binarray(img,ndown, axis=None):
    """downsample a 2D image

    Takes a 1D vector or 2D array and reduce resolution by an integer factor
    "ndown".  This is done by binning the array -- i.e., subaveraging
    over square blocks of pixels of width "ndown"

    If keyword "axis" is None, bin over all axes.  Otherwise, bin over
    the single specified axis.

    Note that 'ndown' can also be a sequence: e.g., [2, 1]

    :EXAMPLE:
       ::
       
           [img_ds]=binarray(img,ndown)        
    """
    # Renamed (and re-commented) by IJC 2007/01/31 from "downsample.m" to 
    #      "binarray.m"
    # 2009-05-06 14:15 IJC: Converted from Matlab to Python
    # 2009-09-27 14:37 IJC: Added 1D vector support.
    # 2010-09-27 16:08 IJC: ADded axis support.
    # 2010-10-26 10:55 IJC: Much simpler algorithm for 1D case
    # 2011-05-21 19:46 IJMC: Actually got axis support to work (2D
    #                        only). Fixed indexing bug (in x, y meshgrid)
    # 2012-09-08 18:50 IJMC: Big change -- 2D mode is now ~20x faster,
    #                        owing to emphasis on array-based
    #                        calculations.
    # 2013-03-11 14:43 IJMC: Cast 'ndown' to int.
    # 2013-04-04 11:48 IJMC: ndown can now be a sequence!

    if ndown==1:
        return img

    img = np.array(img, copy=False)

    if hasattr(ndown, '__iter__') and len(ndown)>1:
        ndowny, ndownx = ndown[0:2]
    else:
        ndown, ndownx, ndowny = int(ndown), int(ndown), int(ndown)

    if axis==0:
        ndownx = 1
    elif axis==1:
        ndowny = 1

    #if axis is None:
    if len(img.shape)==2:
        nrows, ncols = img.shape

        x0 = np.arange(0,ncols,ndownx, dtype=int)
        y0 = np.arange(0,nrows,ndowny, dtype=int)
        #x,y = np.meshgrid(x0,y0)
        img_ds = np.zeros((y0.size, x0.size), dtype=img.dtype)
        
        for ii in range(x0.size):
            temp = img[:,x0[ii]:x0[ii]+ndownx].sum(1)
            img_ds[:,ii] = binarray(temp, ndowny)

    elif len(img.shape)==1:
        ncols = len(img)
        n_rep = ncols / ndown
        img_ds = np.array([img[ii::ndown][0:n_rep] for ii in range(ndown)]).sum(0)


    return img_ds



def fixval(arr, repval, retarr=False):
    """Fix non-finite values in a numpy array, and replace them with repval.

    :INPUT:
       arr -- numpy array, with values to be replaced.

       repval -- value to replace non-finite elements with

    :OPTIONAL INPUT:

       retarr -- if False, changes values in arr directly (more
       efficient).  if True, returns a fixed copy of the input array,
       which is left unchanged.

    :example:
     ::

       fixval(arr, -1)
       """
    # 2009-09-02 14:07 IJC: Created
    # 2012-12-23 11:49 IJMC: Halved run time.

    if retarr:
        arr2 = arr.ravel().copy()
    else:
        arr2 = arr.ravel()

    finiteIndex = np.isfinite(arr2)
    if not finiteIndex.any():
        badIndex = find((1-finiteIndex))
        arr2[badIndex] = repval

    if retarr:
        return arr2.reshape(arr.shape)
    else:
        return



def removeoutliers(data, nsigma, remove='both', center='mean', niter=Inf, retind=False, verbose=False):
    """Strip outliers from a dataset, iterating until converged.

    :INPUT:
      data -- 1D numpy array.  data from which to remove outliers.

      nsigma -- positive number.  limit defining outliers: number of
                standard deviations from center of data.

    :OPTIONAL INPUTS:               
      remove -- ('min'|'max'|'both') respectively removes outliers
                 below, above, or on both sides of the limits set by
                 nsigma.

      center -- ('mean'|'median'|value) -- set central value, or
                 method to compute it.

      niter -- number of iterations before exit; defaults to Inf,
               which can occasionally result in empty arrays returned

      retind -- (bool) whether to return index of good values as
                second part of a 2-tuple.

    :EXAMPLE: 
       ::

           from numpy import hist, linspace, randn
           #from analysis import removeoutliers
           data = randn(1000)
           hbins = linspace(-5,5,50)
           d2 = removeoutliers(data, 1.5, niter=1)
           hist(data, hbins)
           hist(d2, hbins)

       """
    # 2009-09-04 13:24 IJC: Created
    # 2009-09-24 17:34 IJC: Added 'retind' feature.  Tricky, but nice!
    # 2009-10-01 10:40 IJC: Added check for stdev==0
    # 2009-12-08 15:42 IJC: Added check for isfinite

    from numpy import median, ones, isfinite

    def getcen(data, method):
        "Get central value of a 1D array (helper function)"
        if method.__class__==str:
            if method=='median':
                cen = median(data)
            else:
                cen = data.mean()
        else:
            cen = method
        return cen

    def getgoodindex(data, nsigma, center, stdev, remove):
        "Get number of outliers (helper function!)"
        if stdev==0:
            distance = data*0.0
        else:
            distance = (data-center)/stdev
        if remove=='min':
            goodind = distance>-nsigma
        elif remove=='max':
            goodind = distance<nsigma
        else:
            goodind = abs(distance)<=nsigma
        return goodind

    data = data.ravel().copy()

    ndat0 = len(data)
    ndat = len(data)
    iter=0
    goodind = ones(data.shape,bool)
    goodind *= isfinite(data)
    while ((ndat0<>ndat) or (iter==0)) and (iter<niter) and (ndat>0) :
        ndat0 = len(data[goodind])
        cen = getcen(data[goodind], center)
        stdev = data[goodind].std()
        thisgoodind = getgoodindex(data[goodind], nsigma, cen, stdev, remove)
        goodind[find(goodind)] = thisgoodind
        if verbose:
            print "cen>>",cen
            print "std>>",stdev
        ndat = len(data[goodind])
        iter +=1
        if verbose:
            print ndat0, ndat
    if retind:
        ret = data[goodind], goodind
    else:
        ret = data[goodind]
    return ret
        


def xcorr2_qwik(img0, img1):
    """
    Perform quick 2D cross-correlation between two images.

    Images must be the same size.

    Computed via squashing the images along each dimension and
    computing 1D cross-correlations.
    """
    # 2009-12-17 10:13 IJC: Created.  Based on idea by J. Johnson.
    from numpy import zeros, max, min, sum

    im00 = img0.sum(0)
    im01 = img0.sum(1)
    im10 = img1.sum(0)
    im11 = img1.sum(1)
    n0 = len(im00)
    n1 = len(im01)
    noffsets0 = 2*n0-1
    noffsets1 = 2*n1-1
    corr0 = zeros(noffsets0,float)
    corr1 = zeros(noffsets1,float)

    for ii in range(noffsets0):
        firstind0 = max((ii-n0+1,0))
        lastind0 = min((n0,  ii+1))
        firstind1 = max((n0-ii-1,0))
        lastind1 = min((2*n0-ii-1,n0))
        corr0[ii] = sum(im00[firstind0:lastind0]*im10[firstind1:lastind1])

    for jj in range(noffsets1):
        firstind0 = max((jj-n0+1,0))
        lastind0 = min((n0,  jj+1))
        firstind1 = max((n0-jj-1,0))
        lastind1 = min((2*n0-jj-1,n0))
        corr1[jj] = sum(im01[firstind0:lastind0]*im11[firstind1:lastind1])

    ret = find([corr0==corr0.max()])-n0+1, find([corr1==corr1.max()])-n0+1
    return  ret
        

def lsq(x, z, w=None, retcov=False):
    """Do weighted least-squares fitting.  

    :INPUTS:
      x : sequence
        tuple of 1D vectors of equal lengths N, or the transposed
        numpy.vstack of this tuple

      z : sequence
        vector of length N; data to fit to.

      w : sequence
        Either an N-vector or NxN array of weights (e.g., 1./sigma_z**2)

      retcov : bool.  
        If True, also return covariance matrix.


    :RETURNS: 
       the tuple of (coef, coeferrs, {cov_matrix})"""
    # 2010-01-13 18:36 IJC: Created
    # 2010-02-08 13:04 IJC: Works for lists or tuples of x
    # 2012-06-05 20:04 IJMC: Finessed the initial checking of 'x';
    #                        updated documentation, cleared namespace.
    # 2013-01-24 15:48 IJMC: Explicitly cast 'z' as type np.ndarray

#    from numpy import vstack, dot, sqrt, isfinite,diag,ones,float, array, ndarray
#    from numpy.linalg import pinv


    if isinstance(x,tuple) or isinstance(x,list):
        Xmat = np.vstack(x).transpose()
    elif isinstance(x, np.ndarray) and x.ndim < 2:
        Xmat = x.reshape(len(x),1)
    else:
        Xmat = np.array(x, copy=False)

    z = np.array(z, copy=False)

    if w==None:
        w = np.diag(np.ones(Xmat.shape[0],float))
    else:
        w = np.array(w,copy=True)
        if w.ndim < 2:
            w = np.diag(w)

    goodind = np.isfinite(Xmat.sum(1))*np.isfinite(z)*np.isfinite(np.diag(w))
    Wmat = w[goodind][:,goodind]

    XtW = np.dot(Xmat[goodind,:].transpose(),Wmat)
    fitcoef = np.dot(np.dot(np.linalg.pinv(np.dot(XtW,Xmat[goodind,:])),XtW), z[goodind])
    
    covmat = (np.linalg.pinv(np.dot(XtW, Xmat[goodind,:])))
    efitcoef = np.sqrt(np.diag(covmat))

    if retcov:
        return fitcoef, efitcoef, covmat
    else:
        return fitcoef, efitcoef



def lsqsp(x, z, w=None, retcov=False):
    """Do weighted least-squares fitting on sparse matrices.  

    :INPUTS:
      x : sparse matrix, shape N x M
        data used in the least-squares fitting, a set of N rows of M
        elements each.

      z : sequence (shape N) or sparse matrix (shape N x 1)
        data to fit to.

      w : sequence (shape N) or sparse matrix (shape N x N)
        Data weights and/or inverse covariances (e.g., 1./sigma_z**2)

      #retcov : bool.  
      #  If True, also return covariance matrix.

    :RETURNS: 
       the tuple of (coef, coeferrs, {cov_matrix})

    :SEE_ALSO:
       :func:`lsq`

    :REQUIREMENTS:
       SciPy's `sparse` module.
       """
    # 2012-09-17 14:57 IJMC: Created from lsq

    from scipy import sparse

    
    M, N = x.shape
    #x2 = sparse.dia_matrix(x)
    #pdb.set_trace()
    if w==None:
        w = sparse.dia_matrix((1./np.ones(M), 0), shape=(M, M))
    if max(w.shape)==np.prod(w.shape): # w is 1D:
        w = sparse.dia_matrix((w, 0), shape=(M, M))

    z = sparse.csr_matrix(z)
    if z.shape[0]==1:
        z = z.transpose()
    w = sparse.csr_matrix(w)


    XtW = np.dot(x.transpose(), w)
    pinv0 = sparse.csr_matrix(np.linalg.pinv(np.dot(XtW, x).todense()))
    fitcoef = np.array(np.dot(np.dot(pinv0, XtW), z).todense()).squeeze()
    
    covmat = np.linalg.pinv(np.dot(XtW, x).todense())
    efitcoef = np.sqrt(covmat)

    if retcov:
        return fitcoef, efitcoef, covmat
    else:
        return fitcoef, efitcoef



def medianfilter(data, filtersize, threshold=None,verbose=False):
    """ For now, we assume FILTERSIZE is odd, and that DATA is square!
    
    filt = medianfilter(data, filtersize)
    
    This is about the slowest way to do it, but it was easy to write.
    """
    # 2006/02/01 IJC at the Jet Propulsion Laboratory
    # 2010-02-18 13:52 IJC: Converted to python
    from numpy import zeros, median, abs, std

    print "Just use scipy.signal.medfilt !!!"
    print "Just use scipy.signal.medfilt !!!"
    print "Just use scipy.signal.medfilt !!!"

    if len(filtersize)<1:
        print 'medianfilter2 requires that filtersize be a 1- or 2-element vector'
        return -1
    elif len(filtersize)==1:
        filtersize = [filtersize[0], filtersize[0]]
    else:
        filtersize = filtersize[0:2]

    npix = data.shape[0]
    npiy = data.shape[1]
    bigsize = npix+2*(filtersize[0]-1)
    bigdata = zeros((bigsize,bigsize),float)
    ind = filtersize[0]-1
    if ind==0:
        bigdata = data
    else:
        bigdata[ind:(bigsize-ind), ind:(bigsize-ind)] = data


    # FOR NOW, WE ASSUME FILTERSIZE IS ODD!!
    # AND THAT DATA IS SQUARE!
    niter_x = npix + (filtersize[0]-1)
    niter_y = npiy + (filtersize[1]-1)
    filt = zeros((niter_x,niter_y), float)

    for ii in range(niter_x):
        for jj in range(niter_y):
            if verbose>1:
                print "ii,jj>>",ii,jj
            if filtersize[0]==1:
                indi = 1
            else:
                indi = filtersize[0]-1
            if filtersize[1]==1:
                indj = 1
            else:
                indj = filtersize[1]-1
            select = bigdata[ii:(ii+indi),jj:(jj+indj)].ravel()
            select = select[isfinite(select)]
            #residualSelection = abs(select - median(select))

            if verbose: 
                print "select.shape>>",select.shape
                print "threshold>>",threshold

            if threshold is not None:
                if threshold >= 0: # raw threshold
                    doFilter = abs(bigdata[ii,jj]-median(select))/std(select)>=threshold
                elif threshold<0:  # remove outliers before applying threshold
                    npts_init = len(select)
                    select = removeoutliers(select, abs(threshold), center='median')
                    npts_final = len(select)
                    if verbose>1:
                        print "threshold=",threshold,", removed %i points" % (npts_init-npts_final)
                    
                    doFilter = abs(bigdata[ii,jj]-median(select))/std(select)>=threshold                    
            else:  # filter everything; threshold not set.
                doFilter = True

            if verbose:
                print "doFilter?>>",doFilter
            if verbose>1:
                print "select>>",select

            if doFilter: 
                newval =  median( select )
            else:
                newval = bigdata[ii,jj]

            if verbose>1:
                print "newval>>",newval

            filt[ii,jj] = newval

    print filt.shape, [(filtersize[0]-1)/2,niter_x-(filtersize[0]-1)/2,(filtersize[0]-1)/2,niter_y-(filtersize[0]-1)/2]
    return filt[(filtersize[0]-1)/2:niter_x-(filtersize[0]-1)/2,(filtersize[0]-1)/2:niter_y-(filtersize[0]-1)/2]


def stdfilt2d(data, filtersize, threshold=None,verbose=False):
    """ For now, we assume FILTERSIZE is odd, and that DATA is square!
    
    filt = stdfilt2d(data, filtersize)
    
    This is about the slowest way to do it, but it was easy to write.
    """
    # 2012-08-07 13:42 IJMC: Created from medianfilter
    from numpy import zeros, median, abs, std, isfinite

    if not hasattr(filtersize, '__iter__'):
        filtersize = [filtersize]

    if len(filtersize)<1:
        print 'medianfilter2 requires that filtersize be a 1- or 2-element vector'
        return -1
    elif len(filtersize)==1:
        filtersize = [filtersize[0], filtersize[0]]
    else:
        filtersize = filtersize[0:2]

    npix = data.shape[0]
    npiy = data.shape[1]
    bigsize_x = npix+2*(filtersize[0]-1)
    bigsize_y = npiy+2*(filtersize[1]-1)
    bigdata = zeros((bigsize_x,bigsize_y),float)
    ind = filtersize[0]-1
    if ind==0:
        bigdata = data
    else:
        bigdata[ind:(bigsize_x-ind), ind:(bigsize_y-ind)] = data


    # FOR NOW, WE ASSUME FILTERSIZE IS ODD!!
    # AND THAT DATA IS SQUARE!
    niter_x = npix + (filtersize[0]-1)
    niter_y = npiy + (filtersize[1]-1)
    filt = zeros((niter_x,niter_y), float)

    for ii in range(niter_x):
        for jj in range(niter_y):
            if verbose>1:
                print "ii,jj>>",ii,jj
            if filtersize[0]==1:
                indi = 1
            else:
                indi = filtersize[0]-1
            if filtersize[1]==1:
                indj = 1
            else:
                indj = filtersize[1]-1
            select = bigdata[ii:(ii+indi),jj:(jj+indj)].ravel()
            #select = select[isfinite(select)]
            #residualSelection = abs(select - median(select))

            doFilter = True

            if verbose:
                print "doFilter?>>",doFilter
            if verbose>1:
                print "select>>",select

            if doFilter: 
                newval =  ( select ).std()
            else:
                newval = bigdata[ii,jj]

            if verbose>1:
                print "newval>>",newval

            filt[ii,jj] = newval

    #print filt.shape, [(filtersize[0]-1)/2,niter_x-(filtersize[0]-1)/2,(filtersize[0]-1)/2,niter_y-(filtersize[0]-1)/2]
    return filt[(filtersize[0]-1)/2:niter_x-(filtersize[0]-1)/2,(filtersize[0]-1)/2:niter_y-(filtersize[0]-1)/2]



def wmean(a, w, axis=None, reterr=False):
    """wmean(a, w, axis=None)

    Perform a weighted mean along the specified axis.

    :INPUTS:
      a : sequence or Numpy array
        data for which weighted mean is computed

      w : sequence or Numpy array
        weights of data -- e.g., 1./sigma^2

      reterr : bool
        If True, return the tuple (mean, err_on_mean), where
        err_on_mean is the unbiased estimator of the sample standard
        deviation.

    :SEE ALSO:  :func:`wstd`
    """
    # 2008-07-30 12:44 IJC: Created this from ...
    # 2012-02-28 20:31 IJMC: Added a bit of documentation
    # 2012-03-07 10:58 IJMC: Added reterr option

    newdata    = array(a, subok=True, copy=True)
    newweights = array(w, subok=True, copy=True)

    if axis==None:
        newdata    = newdata.ravel()
        newweights = newweights.ravel()
        axis = 0

    ash  = list(newdata.shape)
    wsh  = list(newweights.shape)

    nsh = list(ash)
    nsh[axis] = 1

    if ash<>wsh:
        warn('Data and weight must be arrays of same shape.')
        return []
    
    wsum = newweights.sum(axis=axis).reshape(nsh) 
    
    weightedmean = (a * newweights).sum(axis=axis).reshape(nsh) / wsum
    if reterr:
        # Biased estimator:
        #e_weightedmean = sqrt((newweights * (a - weightedmean)**2).sum(axis=axis) / wsum)

        # Unbiased estimator:
        #e_weightedmean = sqrt((wsum / (wsum**2 - (newweights**2).sum(axis=axis))) * (newweights * (a - weightedmean)**2).sum(axis=axis))
        
        # Standard estimator:
        e_weightedmean = np.sqrt(1./newweights.sum(axis=axis))

        ret = weightedmean, e_weightedmean
    else:
        ret = weightedmean

    return ret



def wstd(a, w, axis=None):
    """wstd(a, w, axis=None)

    Perform a weighted standard deviation along the specified axis.
    If axis=None, then the weighted standard deviation of the entire
    array is computed.

    Note that this computes the _sample_ standard deviation;
    Numpy/Scipy computes the _population_ standard deviation, which is
    greater by a factor sqrt(N/N-1).  This effect is small for large
    datasets.

    :SEE ALSO:  :func:`wmean`

    Taken from http://en.wikipedia.org/wiki/Weighted_standard_deviation
    """
# 2008-07-30 12:44 IJC: Created this from 


    newdata    = array(a, subok=True, copy=True)
    newweights = array(w, subok=True, copy=True)

    if axis==None:
        newdata    = newdata.ravel()
        newweights = newweights.ravel()
        axis = 0

    ash  = list(newdata.shape)
    wsh  = list(newweights.shape)

    nsh = list(ash)
    nsh[axis] = 1

    if ash<>wsh:
        warn('Data and weight must be arrays of same shape.')
        return []
    
    wsum = newweights.sum(axis=axis).reshape(nsh) 
    omega = 1.0 * wsum / (wsum**2 - (newweights**2).sum(axis=axis).reshape(nsh))
    
    weightedstd = omega * (newweights * (newdata-wmean(newdata, newweights, axis=axis))**2 ).sum(axis=axis).reshape(nsh)

    return sqrt(weightedstd)



def fmin(func, x0, args=(), kw=dict(),  xtol=1e-4, ftol=1e-4, maxiter=None, maxfun=None,
         full_output=0, disp=1, retall=0, callback=None, zdelt = 0.00025, nonzdelt = 0.05, 
         holdfixed=None):
    """Minimize a function using the downhill simplex algorithm -- now with KEYWORDS.

    :Parameters:

      func : callable func(x,*args)
          The objective function to be minimized.
      x0 : ndarray
          Initial guess.
      args : tuple
          Extra arguments passed to func, i.e. ``f(x,*args)``.
      callback : callable
          Called after each iteration, as callback(xk), where xk is the
          current parameter vector.

    :Returns: (xopt, {fopt, iter, funcalls, warnflag})

      xopt : ndarray
          Parameter that minimizes function.
      fopt : float
          Value of function at minimum: ``fopt = func(xopt)``.
      iter : int
          Number of iterations performed.
      funcalls : int
          Number of function calls made.
      warnflag : int
          1 : Maximum number of function evaluations made.
          2 : Maximum number of iterations reached.
      allvecs : list
          Solution at each iteration.

    *Other Parameters*:

      xtol : float
          Relative error in xopt acceptable for convergence.
      ftol : number
          Relative error in func(xopt) acceptable for convergence.
      maxiter : int
          Maximum number of iterations to perform.
      maxfun : number
          Maximum number of function evaluations to make [200*len(x0)]
      full_output : bool
          Set to True if fval and warnflag outputs are desired.
      disp : bool
          Set to True to print convergence messages.
      retall : bool
          Set to True to return list of solutions at each iteration.
      zdelt : number
          Set the initial stepsize for x0[k] equal to zero
      nonzdelt : number
          Set the initial stepsize for x0[k] nonzero
      holdfixed : sequence
          Indices of x0 to hold fixed (e.g., [1, 2, 4])


    :TBD:  gprior : tuple or sequence of tuples
          Set a gaussian prior on the indicated parameter, such that
          chisq += ((x0[p] - val)/unc_val)**2, where the parameters
          are defined by the tuple gprior=(param, val, unc_val)

    :Notes:

        Uses a Nelder-Mead simplex algorithm to find the minimum of
        function of one or more variables.

    """
    # 2011-04-13 14:26 IJMC: Adding Keyword option
    # 2011-05-11 10:48 IJMC: Added the zdelt and nonzdelt options
    # 2011-05-30 15:36 IJMC: Added the holdfixed option

    def wrap_function(function, args, **kw):
        ncalls = [0]
        def function_wrapper(x):
            ncalls[0] += 1
            return function(x, *args, **kw)
        return ncalls, function_wrapper

    # Set up holdfixed arrays
    if holdfixed is not None:
        holdfixed = np.array(holdfixed)
        #x0[holdfixed] = x0[holdfixed]
        holdsome = True
    else:
        holdsome = False
        #holdfixed = np.zeros(params.size, dtype=bool)
    
    #if holdsome:
    #    print "holdfixed>>", holdfixed

    fcalls, func = wrap_function(func, args, **kw)
    x0 = np.asfarray(x0).flatten()
    xoriginal = x0.copy()
    N = len(x0)
    rank = len(x0.shape)
    if not -1 < rank < 2:
        raise ValueError, "Initial guess must be a scalar or rank-1 sequence."
    if maxiter is None:
        maxiter = N * 200
    if maxfun is None:
        maxfun = N * 200

    rho = 1; chi = 2; psi = 0.5; sigma = 0.5;
    one2np1 = range(1,N+1)

    if rank == 0:
        sim = np.zeros((N+1,), dtype=x0.dtype)
    else:
        sim = np.zeros((N+1,N), dtype=x0.dtype)
    fsim = np.zeros((N+1,), float)
    sim[0] = x0
    if retall:
        allvecs = [sim[0]]
    #print func.__name__
    #print x0
    fsim[0] = func(x0)
    for k in range(0,N):
        y = np.array(x0,copy=True)
        if y[k] != 0:
            y[k] = (1+nonzdelt)*y[k]
        else:
            y[k] = zdelt
        if holdsome and k in holdfixed:
            y[k] = xoriginal[k]
        sim[k+1] = y
        f = func(y)
        fsim[k+1] = f

    ind = np.argsort(fsim)
    fsim = np.take(fsim,ind,0)
    # sort so sim[0,:] has the lowest function value
    sim = np.take(sim,ind,0)

    iterations = 1

    while (fcalls[0] < maxfun and iterations < maxiter):
        ### IJC Edit to understand fmin!
        ##print 'xtol>> ' + str(max(np.ravel(abs(sim[1:]-sim[0])))) + ' > ' + str(xtol)
        ##print 'ftol>> ' + str(max(abs(fsim[0]-fsim[1:]))) + ' > ' + str(ftol)
        if (max(np.ravel(abs(sim[1:]-sim[0]))) <= xtol \
            and max(abs(fsim[0]-fsim[1:])) <= ftol):
            break

        xbar = np.add.reduce(sim[:-1],0) / N
        xr = (1+rho)*xbar - rho*sim[-1]
        if holdsome:
            xr[holdfixed] = xoriginal[holdfixed]
        fxr = func(xr)
        doshrink = 0

        if fxr < fsim[0]:
            xe = (1+rho*chi)*xbar - rho*chi*sim[-1]
            if holdsome:
                xe[holdfixed] = xoriginal[holdfixed]
            fxe = func(xe)

            if fxe < fxr:
                sim[-1] = xe
                fsim[-1] = fxe
            else:
                sim[-1] = xr
                fsim[-1] = fxr
        else: # fsim[0] <= fxr
            if fxr < fsim[-2]:
                sim[-1] = xr
                fsim[-1] = fxr
            else: # fxr >= fsim[-2]
                # Perform contraction
                if fxr < fsim[-1]:
                    xc = (1+psi*rho)*xbar - psi*rho*sim[-1]
                    if holdsome:
                        xc[holdfixed] = xoriginal[holdfixed]
                    fxc = func(xc)

                    if fxc <= fxr:
                        sim[-1] = xc
                        fsim[-1] = fxc
                    else:
                        doshrink=1
                else:
                    # Perform an inside contraction
                    xcc = (1-psi)*xbar + psi*sim[-1]
                    if holdsome:
                        xcc[holdfixed] = xoriginal[holdfixed]
                    fxcc = func(xcc)

                    if fxcc < fsim[-1]:
                        sim[-1] = xcc
                        fsim[-1] = fxcc
                    else:
                        doshrink = 1

                if doshrink:
                    for j in one2np1:
                        sim[j] = sim[0] + sigma*(sim[j] - sim[0])
                        if holdsome:
                            sim[j, holdfixed] = xoriginal[holdfixed]
                        fsim[j] = func(sim[j])

        ind = np.argsort(fsim)
        sim = np.take(sim,ind,0)
        fsim = np.take(fsim,ind,0)
        if callback is not None:
            callback(sim[0])
        iterations += 1
        if retall:
            allvecs.append(sim[0])

    x = sim[0]
    fval = min(fsim)
    warnflag = 0

    if fcalls[0] >= maxfun:
        warnflag = 1
        if disp:
            print "Warning: Maximum number of function evaluations has "\
                  "been exceeded."
    elif iterations >= maxiter:
        warnflag = 2
        if disp:
            print "Warning: Maximum number of iterations has been exceeded"
    else:
        if disp:
            print "Optimization terminated successfully."
            print "         Current function value: %f" % fval
            print "         Iterations: %d" % iterations
            print "         Function evaluations: %d" % fcalls[0]


    if full_output:
        retlist = x, fval, iterations, fcalls[0], warnflag
        if retall:
            retlist += (allvecs,)
    else:
        retlist = x
        if retall:
            retlist = (x, allvecs)

    return retlist


def fmin_powell(func, x0, args=(), kw=dict(), xtol=1e-4, ftol=1e-4, maxiter=None,
                maxfun=None, full_output=0, disp=1, retall=0, callback=None,
                direc=None, holdfixed=None):
    """Minimize a function using modified Powell's method -- now with KEYWORDS.

    :Parameters:

      func : callable f(x,*args)
          Objective function to be minimized.
      x0 : ndarray
          Initial guess.
      args : tuple
          Eextra arguments passed to func.
      kw : dict
          Keyword arguments passed to func.
      callback : callable
          An optional user-supplied function, called after each
          iteration.  Called as ``callback(xk)``, where ``xk`` is the
          current parameter vector.
      direc : ndarray
          Initial direction set.

    :Returns: (xopt, {fopt, xi, direc, iter, funcalls, warnflag}, {allvecs})

        xopt : ndarray
            Parameter which minimizes `func`.
        fopt : number
            Value of function at minimum: ``fopt = func(xopt)``.
        direc : ndarray
            Current direction set.
        iter : int
            Number of iterations.
        funcalls : int
            Number of function calls made.
        warnflag : int
            Integer warning flag:
                1 : Maximum number of function evaluations.
                2 : Maximum number of iterations.
        allvecs : list
            List of solutions at each iteration.

    *Other Parameters*:

      xtol : float
          Line-search error tolerance.
      ftol : float
          Relative error in ``func(xopt)`` acceptable for convergence.
      maxiter : int
          Maximum number of iterations to perform.
      maxfun : int
          Maximum number of function evaluations to make.
      full_output : bool
          If True, fopt, xi, direc, iter, funcalls, and
          warnflag are returned.
      disp : bool
          If True, print convergence messages.
      retall : bool
          If True, return a list of the solution at each iteration.


    :Notes:

        Uses a modification of Powell's method to find the minimum of
        a function of N variables.

    """
    # 2010-07-01 11:17 IJC: Added keyword option

    from scipy import optimize
    from numpy import asarray, eye, pi, squeeze

    def wrap_function(function, args, **kw):
        ncalls = [0]
        def function_wrapper(x):
            ncalls[0] += 1
            return function(x, *args, **kw)
        return ncalls, function_wrapper

    def _linesearch_powell(func, p, xi, tol=1e-3):
        """Line-search algorithm using fminbound.

        Find the minimium of the function ``func(x0+ alpha*direc)``.

        """
        def myfunc(alpha):
            return func(p + alpha * xi)
        alpha_min, fret, iter, num = optimize.brent(myfunc, full_output=1, tol=tol)
        xi = alpha_min*xi
        return squeeze(fret), p+xi, xi


    # Set up holdfixed arrays
    if holdfixed is not None:
        holdfixed = np.array(holdfixed)
        #x0[holdfixed] = x0[holdfixed]
        holdsome = True
    else:
        holdsome = False
        #holdfixed = np.zeros(params.size, dtype=bool)

    # we need to use a mutable object here that we can update in the
    # wrapper function
    fcalls, func = wrap_function(func, args, **kw)
    x = asarray(x0).flatten()
    xoriginal = x.copy()
    if retall:
        allvecs = [x]
    N = len(x)
    rank = len(x.shape)
    if not -1 < rank < 2:
        raise ValueError, "Initial guess must be a scalar or rank-1 sequence."
    if maxiter is None:
        maxiter = N * 1000
    if maxfun is None:
        maxfun = N * 1000


    if direc is None:
        direc = eye(N, dtype=float)
    else:
        direc = asarray(direc, dtype=float)

    fval = squeeze(func(x))
    x1 = x.copy()
    iter = 0;
    ilist = range(N)
    while True:
        fx = fval
        bigind = 0
        delta = 0.0
        for i in ilist:
            direc1 = direc[i]
            fx2 = fval
            if (not holdsome) or (i not in holdfixed):
                fval, x, direc1 = _linesearch_powell(func, x, direc1, tol=xtol*100)
                if (fx2 - fval) > delta:
                    delta = fx2 - fval
                    bigind = i
        iter += 1
        if callback is not None:
            callback(x)
        if retall:
            allvecs.append(x)
        if (2.0*(fx - fval) <= ftol*(abs(fx)+abs(fval))+1e-20): break
        if fcalls[0] >= maxfun: break
        if iter >= maxiter: break

        # Construct the extrapolated point
        direc1 = x - x1
        x2 = 2*x - x1
        if holdsome:
            x2[holdfixed] = xoriginal[holdfixed]
        x1 = x.copy()
        fx2 = squeeze(func(x2))

        if (fx > fx2):
            t = 2.0*(fx+fx2-2.0*fval)
            temp = (fx-fval-delta)
            t *= temp*temp
            temp = fx-fx2
            t -= delta*temp*temp
            if t < 0.0:
                fval, x, direc1 = _linesearch_powell(func, x, direc1,
                                                     tol=xtol*100)
                if holdsome:
                    x[holdfixed] = xoriginal[holdfixed]
                direc[bigind] = direc[-1]
                direc[-1] = direc1

    warnflag = 0
    if fcalls[0] >= maxfun:
        warnflag = 1
        if disp:
            print "Warning: Maximum number of function evaluations has "\
                  "been exceeded."
    elif iter >= maxiter:
        warnflag = 2
        if disp:
            print "Warning: Maximum number of iterations has been exceeded"
    else:
        if disp:
            print "Optimization terminated successfully."
            print "         Current function value: %f" % fval
            print "         Iterations: %d" % iter
            print "         Function evaluations: %d" % fcalls[0]

    x = squeeze(x)

    if full_output:
        retlist = x, fval, direc, iter, fcalls[0], warnflag
        if retall:
            retlist += (allvecs,)
    else:
        retlist = x
        if retall:
            retlist = (x, allvecs)

    return retlist



def gaussian2d(p, x, y):
    """ Compute a 2D gaussian distribution at the points x, y.

    :INPUTS:
        p : sequence
          a four- or five-component array, list, or tuple:

          z =  [p4 +] p0/(2*pi*p1**2) * exp(-((x-p2)**2+(y-p3)) / (2*p1**2))

          p[0] -- Area of the gaussian
          p[1] -- one-sigma dispersion
          p[2] -- x-central offset
          p[3] -- y-central offset
          p[4] -- optional constant, vertical offset

        x : NumPy array
          X-coordinate values at which the above relation will be computed.

        y : NumPy array
          Y-coordinate values at which the above relation will be computed.

    :SEE_ALSO:
      :func:`gaussian` (1D)
        """
    #2010-06-08 20:00 IJC: Created
    #2013-04-19 23:49 IJMC: Improved documentation, per BACM's request.
    
    x = array(x, dtype=float).copy()
    y = array(y, dtype=float).copy()
    p = array(p).copy()

    if len(p)==4:
        p = concatenate((p, [0]))

    z = p[4] + p[0]/(2*pi*p[1]**2) * exp(-((x-p[2])**2 + (y-p[3])**2) / (2*p[1]**2))
    
    return z


def gaussiannd(mu, cov, x):
    """ Compute an N-dimensional gaussian distribution at the position x.

        mu is the length-N 1D vector of mean positions

        cov is the NxN covariance matrix of the multinormal distribution.  

        x are the positions at which to compute.  If X is 2D (size M x
          N), it is taken as M sets of N-point positions.

        SEE ALSO:  :func:`gaussian`, :func:`gaussian2d`
        """
    #2012-05-08 11:36 IJMC: Created
    
    x = np.array(x, dtype=float, copy=False)
    mu = np.array(mu, dtype=float, copy=False)
    cov = np.array(cov, dtype=float, copy=True)
    
    if x.ndim==1:
        nx = x.size
        niter = 0
    elif x.ndim==2:
        niter, nx = x.shape
        
    if cov.size==1:
        cov = cov.reshape((1,1))

    # Test if cov is square:

    # invert
    invcov = np.linalg.inv(cov)

    # Compute mean vector:
    if niter==0:
        xmu = (x - mu).reshape(nx, 1)
        term1 = ((2*np.pi)**(nx/2.) * np.sqrt(np.linalg.det(cov)))
        term2 = np.exp(-0.5 * np.dot(xmu.transpose(), np.dot(invcov, xmu)))
        ret = term2 / term1
    else:
        for ii in range(niter):
            xmu = (x[ii] - mu).reshape(nx, 1)
            term1 = ((2*np.pi)**(nx/2.) * np.sqrt(np.linalg.det(cov)))
            term2 = np.exp(-0.5 * np.dot(xmu.transpose(), np.dot(invcov, xmu)))
            ret[ii] = term2 / term1
            

    ret = np.zeros(nx, dtype=float)


    return term2 / term1



def gaussian2d_ellip(p, x, y):
    """ Compute a 2D elliptical gaussian distribution at the points x, y.

        p is a 5-, 6-, or 7-component sequence, defined as:

            p[0] -- Amplitude (Area of the function)

            p[1] -- x-dispersion

            p[2] -- y-dispersion

            p[3] -- x-central offset

            p[4] -- y-central offset

            p[5] -- optional rotation angle (radians)

            p[6] -- optional constant, vertical offset

        X, Y are gridded data from :func:`numpy.meshgrid`

        First define:
          x' = (x - p[3]) cos p[5] - (y - p[4]) sin p[5]

          y' = (x - p[3]) sin p[5] + (y - p[4]) cos p[5]

        Then calculate:
          U = (x' / p[1])**2 + (y' / p[2])**2

          z =  p[6] + p0/(2*pi*p1*p2) * exp(-U / 2)

        SEE ALSO:  :func:`gaussian2d`, :func:`lorentzian2d`
        """
    #2012-02-11 18:06 IJMC: Created from IDL GAUSS2DFIT
    
    x = array(x, dtype=float).copy()
    y = array(y, dtype=float).copy()
    p = array(p).copy()

    if len(p)==5:
        p = concatenate((p, [0, 0]))
    elif len(p)==6:
        p = concatenate((p, [0]))

    xp = (x - p[3]) * np.cos(p[5]) - (y - p[4]) * np.sin(p[5])
    yp = (x - p[3]) * np.sin(p[5]) + (y - p[4]) * np.cos(p[5])

    z = p[6] + p[0]/(2*pi*p[1]*p[2]) * exp(-0.5 * ((xp / p[1])**2 + (yp / p[2])**2))
    
    return z


def lorentzian2d(p, x, y):
    """ Compute a 2D Lorentzian distribution at the points x, y.

        p is a 5-, 6-, or 7--component sequence:

          z = (x-p3) ** 2 / p1 ** 2 + (y-p4) ** 2 / p2 ** 2  [ + (x-p3) * (y-p4) * p5 ]
            lorentz = p0 / (1.0 + z)   [ + p6]

        p[0] -- Amplitude (Area of the function)
        p[1] -- x-dispersion
        p[2] -- y-dispersion
        p[3] -- x-central offset
        p[4] -- y-central offset
        p[5] -- optional ellipticitity parameter
        p[6] -- optional constant, vertical offset

        SEE ALSO:  :func:`gaussian2d`
        """
    #2012-02-04 11:38 IJMC: Created
    
    x = array(x, dtype=float).copy()
    y = array(y, dtype=float).copy()
    p = array(p).copy()

    if len(p)==5:
        p = concatenate((p, [0, 0]))
    elif len(p)==6:
        p = concatenate((p, [0]))

    z = ((x - p[3]) / p[1])**2 + ((y - p[4]) / p[2])**2 + p[5] * (x - p[3]) * (y - p[4])
    
    return p[6] + p[0]/(1. + z)


def egaussian2d(p,x,y,z,w=None):
    """ Return the error associated with a 2D gaussian fit, using gaussian2d.

    w is an array of weights, typically 1./sigma**2"""
    # 2010-06-08 20:02 IJC: Created
    from numpy import ones, array
    x = array(x, dtype=float).copy()
    if w is None:
        w = ones(w.shape,float)
    z0 = gaussian2d(p,x,y)
    return (((z-z0)*w)**2).sum()



def getblocks(vec):
    """Return start and end indices for consecutive sequences of
    integer-valued indices.

    :Example:
        ::

             import analysis as an
             vec = range(5) +range(10,14) + range(22,39)
             starts,ends = an.getblocks(vec)
             print zip(starts,ends)
             """
    # 2010-08-18 17:01 IJC: Created
    # 2010-11-15 23:26 IJC: Added numpy imports

    from numpy import sort, diff, nonzero

    vec = sort(vec)
    starts = [vec[0]]
    ends = []
    dvec = diff(vec)
    start_inds = nonzero(dvec>1)[0]
    for ind in start_inds:
        starts.append(vec[ind+1])
        ends.append(vec[ind])

    ends.append(vec[-1])

    return starts, ends


def snr(data, axis=None, nsigma=None):
    """
    Compute the quantity:
    data.mean(axis=axis)/data.std(axis=axis)
    
    for the specified data array/vector along the specified axis.
    
    Output will be a scalar (axis is None) or numpy array, as
    appropriate.
    """
    # 2010-09-02 08:10 IJC: Created
    # 2011-12-16 14:51 IJMC: Added optional nsigma flag

    data = array(data)
    if nsigma is None:
        ret = data.mean(axis=axis)/data.std(axis=axis)
    else:
        ret = meanr(data, axis=axis, nsigma=nsigma) / \
            stdr(data, axis=axis, nsigma=nsigma)
    return  ret


def pad(inp, npix_rows, npix_cols=None):
    """Pads input matrix to size specified. 
    ::

       out = pad(in, npix)     
       out = pad(in, npix_rows, npix_cols);  # alternate usage
      
    Written by J. Green @ JPL; converted to Python by I. Crossfield"""
    #2008-10-18 12:50 IJC: Converted from Matlab function
    # 2010-10-29 09:35 IJC: Moved from nsdata.py to analysis.py

    from numpy import imag, zeros, complex128

    inp = array(inp, copy=True)
    if len(inp.shape)==0:
        inp = inp.reshape((1,1))
    elif len(inp.shape)==1:
        inp = inp.reshape((1, len(inp)))

    if npix_cols==None:
        npix_cols = npix_rows
        
    if (imag(inp)**2).sum()==0:
        out = zeros((npix_rows, npix_cols))
    else:
        out = zeros((npix_rows, npix_cols), complex128)
    
    nrows, ncols  = inp.shape

    ixc = floor(ncols/2 + 1);
    iyc = floor(nrows/2 + 1);

    oxc = floor(npix_cols/2 + 1);
    oyc = floor(npix_rows/2 + 1);

    dx = npix_cols-ncols;
    dy = npix_rows-nrows;

    if dx<=0:
        ix1 = ixc - floor(npix_cols/2);
        ix2 = ix1 + npix_cols - 1;
        ox1 = 1;
        ox2 = npix_cols;
    else:
        ix1 = 1;
        ix2 = ncols;
        ox1 = oxc - floor(ncols/2);
        ox2 = ox1 + ncols - 1;

   
    if dy<=0:
        iy1 = iyc - floor(npix_rows/2);
        iy2 = iy1 + npix_rows - 1;
        oy1 = 1;
        oy2 = npix_rows;
    else:
        iy1 = 1;
        iy2 = nrows;
        oy1 = oyc - floor(nrows/2);
        oy2 = oy1 + nrows - 1;

    out[ oy1-1:oy2, ox1-1:ox2]  = inp[ iy1-1:iy2, ix1-1:ix2];

# Uncomment for testing
#    print inp
#    print ixc, iyc, iy1, iy2, ix1, ix2 
#    print oxc, oyc, oy1, oy2, ox1, ox2 

    return out



def fftfilter1d(vec, bandwidth, retfilter=False):
    """ Apply a hard-edged low-pass filter to an input vector.

    :INPUTS:

       vec -- sequence -- 1D vector, assumed to be evenly sampled

       bandwidth -- integer -- size of the filter passband in cycles
                              per signal duration.  f <= bandwidth is
                              passed through; f > bandwidth is
                              rejected.

       retfilter -- bool -- if True, return the tuple (filtered_vec, filter)

    :OUTPUT:
       
       Lopass-filtered version of vec

    :NOTE:

       Assumes the input is real-valued.
       """
    # 2011-03-11 14:15 IJC: Created

    from numpy import real, fft, floor, ceil

    vec = array(vec, copy=True)

    # Errorchecking
    if len(vec.shape)<>1:
        print "Input array must be 1D -- try using .ravel()"
        return -1


    npts = vec.size

    filter = concatenate((zeros(floor(npts/2.) - bandwidth), 
                          ones(bandwidth * 2 + 1),
                          zeros(ceil(npts/2.) - bandwidth - 1)))

    ret = real(fft.ifft(fft.ifftshift( fft.fftshift(fft.fft(vec)) * filter )))

    if retfilter==True:
        ret = [ret, filter]

    return ret



def stdres(data, bins=None, oversamp=None, dataindex=None):
    """Compute the standard deviation in the residuals of a data
    series after average-binning by specified amounts.

    :INPUTS:
      data - 1D numpy array
         Data to analyze.

      bins - sequence
         Factors by which to bin down.  If None, use 1:sqrt(data.size)
         and set dataindex=None.
         
      oversamp - int
         Number of times to shift, resample, and bin the data.  Large
         values take longer, but give a less "noisy" estimate (which
         can be a problem at large bin sizes)

      dataindex - 1D numpy array

         Values across which data are indexed (i.e., 'time').  If not
         None, bins apply to dataindex rather than to data and should
         be increasing intervals of dataindex (rather than the number
         of points to bin down by).

    :REQUIREMENTS:
       :doc:`tools`, :doc:`numpy`

    :EXAMPLE:
      ::
      
        import numpy as np
        import analysis as an
        import pylab as py

        npts = 1e4
        t = np.arange(npts)
        data = np.random.normal(size=npts)
        binfactors = np.arange(1, npts/2.+1)
        bindown_result = an.stdres(data, binfactors, dataindex=t, oversamp=1)

        py.figure()
        py.subplot(211)
        py.plot(t, data, 'k')
        py.xlabel('Time')
        py.ylabel('Data value')
        py.minorticks_on()
        py.title('Bin-down test: Gaussian Noise')

        py.subplot(212)
        py.loglog(binfactors, bindown_result, '-b', linewidth=2)
        py.loglog(binfactors, data.std()/np.sqrt(binfactors), '--r')
        py.xlabel('Binning factor')
        py.ylabel('RMS of binned data')
        py.legend(['Binned RMS', '1/sqrt(N)'])

         """
    # 2011-06-16 16:50 IJMC: Created
    # 2012-03-20 14:33 IJMC: Added oversamp option.
    # 2012-03-22 09:21 IJMC: Added dataindex option.
    # 2012-04-30 06:50 IJMC: Changed calling syntax to errxy.

    from tools import errxy
    from numpy import isfinite

    ndata = data.size
    if bins is None:
        bins = arange(1, sqrt(int(ndata)))
        dataindex = None

    nout = len(bins)
    if oversamp is None:
        invoversamp = 1
        oversamp = 1
    else:
        invoversamp = 1./oversamp

    ret = zeros(nout, dtype=float)
    if dataindex is None:
        for jj, binfactor in enumerate(bins):
            if binfactor > 0:
                sample_shifts = arange(0., binfactor, binfactor * invoversamp).astype(int)
                for kk in range(oversamp):
                    ret[jj] += binarray(data[sample_shifts[kk]::], binfactor).std()

            else:
                ret[jj] = data.std()*oversamp

    else:
        startval = dataindex.min()
        endval  = dataindex.max()

        for jj, binwidth in enumerate(bins):
            if binwidth > 0:
                thesebins = arange(startval, endval+binwidth, binwidth) - binwidth/2.
                for kk in range(oversamp):
                    di2,d2,edi2,ed2 = errxy(dataindex, data, thesebins + binwidth*kk/oversamp, xerr=None, yerr=None, xmode=None,ymode='mean')
                    if isfinite(d2).all():
                        ret[jj] += d2.std()
                    else:
                        ret[jj] += d2[isfinite(d2)].std()
            else:
                ret[jj] = data.std()*oversamp

    ret /= oversamp
    return ret
         


def allanvariance(data, dt=1):
    """Compute the Allan variance on a set of regularly-sampled data (1D).

       If the time between samples is dt and there are N total
       samples, the returned variance spectrum will have frequency
       indices from 1/dt to (N-1)/dt."""
    # 2008-07-30 10:20 IJC: Created
    # 2011-04-08 11:48 IJC: Moved to analysis.py

    newdata = array(data, subok=True, copy=True)
    dsh = newdata.shape

    newdata = newdata.ravel()

    nsh = newdata.shape

    alvar = zeros(nsh[0]-1, float)

    for lag in range(1, nsh[0]):
        alvar[lag-1]  = mean( (newdata[0:-lag] - newdata[lag:])**2 )

    return (alvar*0.5)
    

def trueanomaly(ecc, eanom=None, manom=None):
    """Calculate (Keplerian, orbital) true anomaly.

    One optional input must be given.

    :INPUT:
       ecc -- scalar.  orbital eccentricity.

    :OPTIONAL_INPUTS:
       eanom -- scalar or Numpy array.  Eccentric anomaly.  See
               :func:`eccentricanomaly`

       manom -- scalar or sequence.  Mean anomaly, equal to 
                2*pi*(t - t0)/period
    """
    # 2011-04-22 14:35 IJC: Created

    if manom is not None:
        eanom = eccentricanomaly(ecc, manom=manom)

    if eanom is not None:
        ret = 2. * np.arctan(  np.sqrt((1+ecc)/(1.-ecc)) * np.tan(eanom/2.)  )
    else:
        ret = None

    return ret


def eccentricanomaly(ecc, manom=None, tanom=None, tol=1e-8):
    """Calculate (Keplerian, orbital) eccentric anomaly.

    One optional input must be given.

    :INPUT:
       ecc -- scalar.  orbital eccentricity.

    :OPTIONAL_INPUTS:

       manom -- scalar or sequence.  Mean anomaly, equal to 
                2*pi*(t - t0)/period

       tanom -- scalar or Numpy array.  True anomaly.  See
               :func:`trueanomaly`.
    """
    # 2011-04-22 14:35 IJC: Created

    

    ret = None
    if manom is not None:
        if not hasattr(manom, '__iter__'):
            mwasscalar = True
            manom = [manom]
        else:
            mwasscalar = False
        # Solve Kepler's equation for each element of mean anomaly:
        e = np.zeros(len(manom)) # Initialize eccentric anomaly
        for ii,element in enumerate(manom):
            def kep(e): return element - e + ecc*sin(e)
            e[ii] = optimize.newton(kep, 0., tol=tol)

        if mwasscalar:
            e = e[0]
        ret = e
    
    elif tanom is not None:
        ret = 2. * np.arctan(np.tan(0.5 * tanom) / \
                                 np.sqrt((1. + ecc) / (1. - ecc)))
        
    else:
        ret = None

    return ret
    


def gaussian(p, x):
    """ Compute a gaussian distribution at the points x.

        p is a three- or four-component array, list, or tuple:

        y =  [p3 +] p0/(p1*sqrt(2pi)) * exp(-(x-p2)**2 / (2*p1**2))

        p[0] -- Area of the gaussian
        p[1] -- one-sigma dispersion
        p[2] -- central offset (mean location)
        p[3] -- optional constant, vertical offset

        NOTE: FWHM = 2*sqrt(2*ln(2)) * p1  ~ 2.3548*p1

        SEE ALSO:  :func:`egaussian`"""
    #2008-09-11 15:11 IJC: Created for LINEPROFILE
    # 2011-05-18 11:46 IJC: Moved to analysis.
    # 2013-04-11 12:03 IJMC: Tried to speed things up slightly via copy=False
    # 2013-05-06 21:42 IJMC: Tried to speed things up a little more.

    if not isinstance(x, np.ndarray):
        x = array(x, dtype=float, copy=False)

    if len(p)==3:
        p = array(p, copy=True)
        p = concatenate((p, [0]))
    #elif len(p)==4:
    #    p = array(p, copy=False)

    return  p[3] + p[0]/(p[1]*sqrt(2*pi)) * exp(-(x-p[2])**2 / (2*p[1]**2))


def doubleGaussian(p, x):
    """ Compute the sum of two gaussian distributions at the points x.

        p is a six- or seven-component sequence:

        y =  [p6 +] p0/(p1*sqrt(2pi)) * exp(-(x-p2)**2 / (2*p1**2)) + 
                    p3/(p4*sqrt(2pi)) * exp(-(x-p5)**2 / (2*p4**2))

        p[0] -- Area of gaussian A
        p[1] -- one-sigma dispersion of gaussian A
        p[2] -- central offset (mean location) of gaussian A 
        p[3] -- Area of gaussian B
        p[4] -- one-sigma dispersion of gaussian B
        p[5] -- central offset (mean location) of gaussian B
        p[6] -- optional constant, vertical offset

        NOTE: FWHM = 2*sqrt(2*ln(2)) * p1  ~ 2.3548*p1

        SEE ALSO:  :func:`gaussian`
        """
    # 2013-05-06 20:29 IJMC: Created

    x = array(x, dtype=float, copy=False)
    return gaussian(p[0:3], x) + gaussian(p[3:], x)


def doubleGaussianCen(p, x, mu1, mu2):
    """ Compute the sum of two gaussian distributions at the points x.
        The distributions have central moments mu1 and mu2.

        Useful for fitting to partially blended spectral data.

        p is a four- or five-component sequence:

        y =  [p6 +] p0/(p1*sqrt(2pi)) * exp(-(x-mu1)**2 / (2*p1**2)) + 
                    p3/(p4*sqrt(2pi)) * exp(-(x-mu2)**2 / (2*p4**2))

        p[0] -- Area of gaussian A
        p[1] -- one-sigma dispersion of gaussian A
        p[2] -- Area of gaussian B
        p[3] -- one-sigma dispersion of gaussian B
        p[4] -- optional constant, vertical offset

        mu1 -- central offset (mean location) of gaussian A 
        mu2 -- central offset (mean location) of gaussian B

        NOTE: FWHM = 2*sqrt(2*ln(2)) * p1  ~ 2.3548*p1

        SEE ALSO:  :func:`doubleGaussian`, :func:`gaussian`
        """
    # 2013-05-06 20:29 IJMC: Created

    x = array(x, dtype=float, copy=False)
    param1 = [p[0], p[1], mu1, 0]
    if len(p)==4:
        param2 = [p[2], p[3], mu2, 0]
    elif len(p)==5:
        param2 = [p[2], p[3], mu2, p[4]]

    return gaussian(param1, x) + gaussian(param2, x)


def nGaussianCen(p, x, mu):
    """ Compute the sum of N gaussian distributions at the points x.
        The distributions have central moments defined by the vector mu.

        Useful for fitting to partially blended spectral data when you
        have good measurements of positions (i.e., from 2D tracing).

        p is a sequence of length (2N+1).  If N=2:

        y =  [p6 +] p0/(p1*sqrt(2pi)) * exp(-(x-mu1)**2 / (2*p1**2)) + 
                    p3/(p4*sqrt(2pi)) * exp(-(x-mu2)**2 / (2*p4**2))

        p[0] -- Area of gaussian 1
        p[1] -- one-sigma dispersion of gaussian 1
        p[2] -- Area of gaussian 2
        p[3] -- one-sigma dispersion of gaussian 2
          ... etc.
        p[-1] -- optional constant, vertical offset
          and
        mu1 -- central offset (mean location) of gaussian A 
        mu2 -- central offset (mean location) of gaussian B

        NOTE: FWHM = 2*sqrt(2*ln(2)) * p1  ~ 2.3548*p1

        SEE ALSO:  :func:`doubleGaussian`, :func:`gaussian`
        """
    # 2013-05-06 20:29 IJMC: Created

    x = array(x, dtype=float, copy=False)
    ret = np.zeros(x.size)
    ngaussians = int(len(p)/2)
    for ii in xrange(ngaussians):
        ret += gaussian([p[ii*2], p[ii*2+1], mu[ii], 0], x)
    if len(p)/2.<>len(p)/2: # P is odd, so the last value is our
        ret += p[-1]        # additive constant.

    return ret


def egaussian(p, x, y, e=None):
    """ Compute the deviation between the values y and the gaussian defined by p, x:

    p is a three- or four-component array, list, or tuple.

    Returns:   y - p3 - p0/(p1*sqrt(2pi)) * exp(-(x-p2)**2 / (2*p1**2))

    if an error array, e (typ. one-sigma) is entered, the returned value is divided by e.

    SEE ALSO:  :func:`gaussian`"""
    # 2008-09-11 15:19 IJC: Created
    # 2009-09-02 15:20 IJC: Added weighted case
    # 2011-05-18 11:46 IJMC: Moved to analysis.
    from numpy import ones

    if e==None:
        e=ones(x.shape)
    fixval(e,y.max()*1e10)

    z = (y - gaussian(p, x))/e
    fixval(z,0)

    return z



def generic_mcmc(*arg, **kw):
    """Run a Markov Chain Monte Carlo (Metropolis-Hastings algorithm)
    on an arbitrary function.

    :INPUTS:
      EITHER:
        func : function to generate model.  
          First argument must be "params;" subsequent arguments are
          passed in via the "args" keyword

        params : 1D sequence
          parameters to be fit

        stepsize :  1D or 2D array
                If 1D: 1-sigma change in parameter per iteration
                If 2D: covariance matrix for parameter changes.

        z : 1D array
                    Contains dependent data (to be modeled)

        sigma : 1D array
                    Contains standard deviation (errors) of "z" data

        numit : int
                Number of iterations to perform

      OR:
        (allparams, (arg1, arg2, ...), numit)

        where allparams is a concatenated list of parameters for each
        of several functions, and the arg_i are tuples of (func_i,
        stepsize_i, z_i, sigma_i). In this case the keyword 'args'
        must also be a tuple of sequences, one for each function to be
        MCMC'ed.

    :OPTIONAL_INPUTS:    
        args : 1D sequence
                Second, third, etc.... arguments to "func"

        nstep : int
                Saves every "nth" step of the chain

        posdef : None, 'all', or sequences of indices.
                Which elements should be restricted to positive definite?
                If indices, it should be of the form (e.g.): [0, 1, 4]

        holdfixed : None, or sequences of indices.
                    Which elements should be held fixed in the analysis?
                    If indices, it should be of the form (e.g.): [0, 1, 4]

        jointpars : None, or sequence of 2-tuples.
                    Only for simultaneous multi-function fitting.  For
                    each pair of values passed, we set the parameters
                    values so: allparams[pair[1]] = allparams[pair[0]]

    :OUTPUTS:
        allparams : 2D array
                Contains all parameters at each step
        bestp : 1D array
                Contains best paramters as determined by lowest Chi^2
        numaccept: int
                Number of accepted steps
        chisq: 1D array
                Chi-squared value at each step
    
    :REFERENCES:
        Numerical Recipes, 3rd Edition (Section 15.8)
        Wikipedia

    :NOTES:
        If you need an efficient MCMC algorithm, you should be using
        http://danfm.ca/emcee/

    """
    # 2011-06-07 07:50 IJMC: Created from various other MCMC codes,
    #                        eventually deriving from K. Stevenson's
    #                        sample code.
    # 2011-06-14 09:48 IJMC: Allow for covariance matrix pass-in to stepsize
    # 2011-06-27 17:39 IJMC: Now link joint parameters for initial chisq. 
    # 2011-09-16 13:31 IJMC: Fixed bug for nextp when nfits==1
    # 2011-11-02 22:08 IJMC: Now cast numit as an int

    import numpy as np
    
    # Parse keywords/optional inputs:
    defaults = dict(args=(), nstep=1, posdef=None, holdfixed=None, \
                        jointpars=None, verbose=False)
    for key in defaults:
        if (not kw.has_key(key)):
            kw[key] = defaults[key]

    args = kw['args']
    nstep = kw['nstep']
    posdef = kw['posdef']
    holdfixed = kw['holdfixed']
    jointpars = kw['jointpars']
    verbose = kw['verbose']

    # Parse inputs:
    if len(arg)==6:
        func, params, stepsize, z, sigma, numit = arg
        stepsize = np.array(stepsize, copy=True)
        weights = 1./sigma**2
        nfits = 1

    elif len(arg)==3:
        params, allargs, numit = arg[0:3]
        nfits = len(allargs)
        funcs = []
        stepsizes = []
        zs = []
        multiargs = []
        multiweights = []
        npars = []
        for ii, these_args in enumerate(allargs):
            funcs.append(these_args[0])
            stepsizes.append(np.array(these_args[1], copy=True))
            zs.append(these_args[2])
            multiweights.append(1./these_args[3]**2)
            multiargs.append(args[ii])
            npars.append(stepsizes[-1].shape[0])
    else:
        print "Must pass either 3 or 6 parameters as input."
        print "You passed %i." % len(arg)
        return -1
    
    

    #Initial setup
    numaccept  = 0
    numit = int(numit)
    nout = numit/nstep
    bestp      = np.copy(params)
    original_params = np.copy(params)
    allparams  = np.zeros((len(params), nout))
    allchi     = np.zeros(nout,float)

    # Set indicated parameters to be positive definite:
    if posdef=='all':
        params = np.abs(params)
        posdef = np.arange(params.size)
    elif posdef is not None:
        posdef = np.array(posdef)
        params[posdef] = np.abs(params[posdef])
    else:
        posdef = np.zeros(params.size, dtype=bool)

    # Set indicated parameters to be held fixed:
    if holdfixed is not None:
        holdfixed = np.array(holdfixed)
        params[holdfixed] = np.abs(params[holdfixed])
    else:
        holdfixed = np.zeros(params.size, dtype=bool)

    if verbose:
        print params[posdef]

    # Set joint parameters:
    if jointpars is not None:
        for jp in jointpars:
            params[jp[1]] = params[jp[0]]


    #Calc chi-squared for model using current params
    if nfits==1:
        zmodel     = func(params, *args)
        currchisq  = (((zmodel - z)**2)*weights).ravel().sum()
        bestchisq  = currchisq
    else:
        tempchisq = 0
        for ii in range(nfits):
            i0 = sum(npars[0:ii])
            i1 = i0 + npars[ii]
            this_zmodel = funcs[ii](params[i0:i1], *multiargs[ii])
            thischisq = (((this_zmodel - zs[ii])**2) * multiweights[ii]).ravel().sum()
            tempchisq += thischisq
        currchisq = tempchisq
        bestchisq = currchisq

    if verbose:
        print currchisq

    #Run Metropolis-Hastings Monte Carlo algorithm 'numit' times
    for j in range(numit):
        #Take step in random direction for adjustable parameters
        if nfits==1:
            if len(stepsize.shape)==1:
                nextp    = np.array([np.random.normal(params,stepsize)]).ravel()
            else:
                nextp = np.random.multivariate_normal(params, stepsize)
        else:
            nextstep = np.zeros(len(params), dtype=float)
            for ii in range(nfits):
                i0 = sum(npars[0:ii])
                i1 = i0 + npars[ii]
                if len(stepsizes[ii].shape)==1:
                    nextstep[i0:i1] = np.random.normal([0]*npars[ii], stepsizes[ii])
                else:                
                    nextstep[i0:i1] = np.random.multivariate_normal([0]*npars[ii], stepsizes[ii])
            nextp = params + nextstep

        # Constrain the desired parameters:
        nextp[posdef] = np.abs(nextp[posdef])
        nextp[holdfixed] = original_params[holdfixed]
        if jointpars is not None:
            for jp in jointpars:
                nextp[jp[1]] = nextp[jp[0]]
                #print nextp[jp[1]], nextp[jp[0]], jp

        #COMPUTE NEXT CHI SQUARED AND ACCEPTANCE VALUES
        if nfits==1:
            zmodel     = func(nextp, *args)
            nextchisq  = (((zmodel - z)**2)*weights).ravel().sum() 
        else:
            tempchisq = 0
            for ii in range(nfits):
                i0 = sum(npars[0:ii])
                i1 = i0 + npars[ii]
                this_zmodel = funcs[ii](nextp[i0:i1], *multiargs[ii])
                thischisq = (((this_zmodel - zs[ii])**2) * multiweights[ii]).ravel().sum()
                tempchisq += thischisq
            nextchisq = tempchisq

        if verbose:
            print nextchisq
            print nextp == original_params

        accept = np.exp(0.5 * (currchisq - nextchisq))

        if (accept >= 1) or (np.random.uniform(0, 1) <= accept):
                #Accept step
                numaccept += 1
                params  = np.copy(nextp)
                currchisq  = nextchisq
        if (currchisq < bestchisq):
                        #New best fit
                        bestp     = np.copy(params)
                        bestchisq = currchisq

        if (j%nstep)==0:
            allparams[:, j/nstep] = params
            allchi[j/nstep] = currchisq

    return allparams, bestp, numaccept, allchi




def scale_mcmc_stepsize(accept, func, params, stepsize, z, sigma, numit=1000, scales=[0.1, 0.3, 1., 3., 10.], args=(), nstep=1, posdef=None, holdfixed=None, retall=False, jointpars=None):
    """Run :func:`generic_mcmc` and scale the input stepsize to match
    the desired input acceptance rate.

    :INPUTS:
       mostly the same as for :func:`generic_mcmc`, but also with:

       accept : float between 0 and 1
          desired acceptance rate; typically between 0.15 - 0.5.

       scales : sequence of floats
          test scaling parameters; measure for these, then interpolate to get 'accept'

       retall : bool
          if True, return tuple (scalefactor, acceptances, scales).
          Otherwise return only the scaler 'scalefactor.'

    :REQUIREMENTS:
       :doc:`pylab` (for :func:`pylab.interp`)
          """
    # 2011-06-13 16:06 IJMC: Created

    from pylab import interp

    stepsize = array(stepsize, copy=True)

    nfactors = len(scales)
    mcmc_accept = []
    for factor in scales:
        out = generic_mcmc(func, params, stepsize/factor, z, sigma, numit, args=args, nstep=nstep, posdef=posdef, holdfixed=holdfixed, jointpars=jointpars)
        mcmc_accept.append(1.0 * out[2]/numit)

    final_factor = interp(accept, mcmc_accept, scales)

    if retall:
        ret = (final_factor, mcmc_accept, scales)
    else:
        ret = final_factor

    return ret


def unityslope(slope, ttt):
    return 1. + slope*(ttt - ttt.mean())


def travisplanet(p):
    """Generate a line of text for Travis Barman's planet table.

    INPUT: a planet object from :func:`getobj`.
    """
    # 2012-02-14 14:52 IJMC: Created

    vals1 = (p.name.replace(' ','').replace('b', ''), p.msini, p.umsini, p.r, p.r-p.ur, p.r+p.ur)
    vals2 = (p.per, p.a, p.mstar, p.umstar, p.rstar, p.urstar, p.teff, p.uteff, p.fe, p.ufe)
    nvals = len(vals1)+len(vals2)
    fstr = '%s' + ' '*(10-len(vals1)) + '  %1.2f'*5 + '  %1.6f  %1.4f' + '  %1.2f'*4 + '  %i'*2 + '  %1.2f'*2

    return  fstr  % (vals1 + vals2 ) 


def stdfilt(vec, wid=3):
    """Compute the standard deviation in a sliding window.

    :INPUTS:
      vec : 1D sequence
        data to filter

      wid : int, odd
        width of filter; ideally odd (not even).
        """
    # 2012-04-05 13:58 IJMC: Created

    filt = 0*vec
    if wid<1:
        wid = 1
        
    wid = int(wid)

    n = len(vec)

    for ii in range(n):
        i0 = np.max([0, ii -wid/2])
        i1 = np.min([n-1, ii + wid/2])
        filt[ii] = np.std(vec[i0:i1+1])
        #print ii, i0, i1

    return filt


def wmeanfilt(vec, wid=3, w=None):
    """Compute the (weighted) mean in a sliding window.

    :INPUTS:
      vec : 1D sequence
        data to filter

      wid : int, odd
        width of filter; ideally odd (not even).
        """
    # 2012-04-28 06:09 IJMC: Created

    filt = 0*vec
    if wid<1:
        wid = 1
        
    wid = int(wid)

    n = len(vec)

    for ii in range(n):
        i0 = np.max([0, ii -wid/2])
        i1 = np.min([n-1, ii + wid/2])
        filt[ii] = wmean(vec[i0:i1+1], w[i0:i1+1])
        #print ii, i0, i1

    return filt



def planettext(planets, filename, delimiter=',', append=True):
    """Write planet object info into a delimited line of text.
    
    :INPUTS:
     planets : planet object or list thereof

     filename : str

     delimiter : str
     """
    # 2012-01-24 16:42 IJMC: Created
    
    if not hasattr(planets, '__iter__'):
        planets = [planets]

    column_headers = 'Planet Name', 'KIC', 'wfc3', 'stis', 'OIR', 'HST', 'SST', \
        'M_p/M_J', 'R_p/R_J', 'P/d', 'a/AU', 'e', 'I', 'a/R*', 'b', 'k', 'T_14', 'd/pc', \
        'ST', 'T_*', 'M_*', 'RA', 'Dec', 'Vmag', 'Jmag', 'Hmag', 'Kmag', 'R_s', \
        'T_eff', 'g_p', '~H (gas-dom.)/km', 'Delta-D', 'Fp/Fs', 'NIR comp.?', \
        '"goodness"', 'kepler_vetting', 'ECL_metric', 'TRA_metric', 'MAX_metric'

    field_names = 'name', None, None, None, None, None, None, 'msini', 'r', 'per', 'a', \
        'ecc', 'i', 'ar', 'b', None, 't14', 'distance', 'sptype', 'teff', 'mstar', \
        'ra_string', 'dec_string', 'v', 'j', 'h', 'ks', 'rstar'

    if append:
        f = open(filename, 'a')
    else:
        f = open(filename, 'w')

    for header in column_headers:
        f.write('%s%s' % (header, delimiter))

    f.write('\n')

    for p in planets:
        for field in field_names:
            if field is None:
                f.write(delimiter)
            elif hasattr(getattr(p, field), 'upper'): # STRING
                f.write('%s%s' % (getattr(p, field), delimiter))
            else: # FLOAT
                f.write('%1.18f%s' % (getattr(p, field), delimiter))
        f.write('\n')

    return




def prayerbead(*arg, **kw):
    """Generic function to perform Prayer-Bead (residual permutation) analysis.

    :INPUTS:
       (fitparams, modelfunction, arg1, arg2, ... , data, weights)

      OR:
       
       (allparams, (args1, args2, ..), npars=(npar1, npar2, ...))

       where allparams is an array concatenation of each functions
       input parameters.


    :OPTIONAL INPUTS:
      jointpars -- list of 2-tuples.  
                   For use with multi-function calling (w/npars
                   keyword).  Setting jointpars=[(0,10), (0,20)] will
                   always set params[10]=params[0] and
                   params[20]=params[0].

      parinfo -- None, or list of dicts
                   'parinfo' to pass to the kapteyn.py kpmfit routine.

      gaussprior -- list of 2-tuples, same length as "allparams."
                   The i^th tuple (x_i, s_i) imposes a Gaussian prior
                   on the i^th parameter p_i by adding ((p_i -
                   x_i)/s_i)^2 to the total chi-squared.  

      axis -- int or None
                   If input is 2D, which axis to permute over.
                   (NOT YET IMPLEMENTED!)

      step -- int > 0
                   Stepsize for permutation steps.  1 by default.
                   (NOT YET IMPLEMENTED!)

      verbose -- bool
                   Print various status lines to console.

      maxiter -- int
                   Maximum number of iterations for _each_ fitting step.

      maxfun -- int
                   Maximum number of function evaluations for _each_ fitting step.

    :EXAMPLE: 
      ::

        TBW

    :REQUIREMENTS: 
      :doc:`kapteyn`, :doc:`phasecurves`, :doc:`numpy`
    """
    # 2012-04-30 07:29 IJMC: Created
    # 2012-05-03 16:35 IJMC: Now can impose gaussian priors
    # 2012-09-17 14:08 IJMC: Fixed bug when shifting weights (thanks
    #                        to P. Cubillos)
    
    #from kapteyn import kmpfit
    import phasecurves as pc

    if kw.has_key('axis'):
        axis = kw['axis']
    else:
        axis = None

    if kw.has_key('parinfo'):
        parinfo = kw.pop('parinfo')
    else:
        parinfo = None

    if kw.has_key('verbose'):
        verbose = kw.pop('verbose')
    else:
        verbose = None

    if kw.has_key('step'):
        step = kw.pop('step')
    else:
        step = None

    if kw.has_key('maxiter'):
        maxiter = kw.pop('maxiter')
    else:
        maxiter = 3000

    if kw.has_key('maxfun'):
        maxfun = kw.pop('maxfun')
    else:
        maxfun = 6000

    if kw.has_key('xtol'):
        xtol = kw.pop('xtol')
    else:
        xtol = 1e-12

    if kw.has_key('ftol'):
        ftol = kw.pop('ftol')
    else:
        ftol = 1e-12

    guessparams = arg[0]
    modelfunction = arg[1]
    nparam = len(guessparams)

    if isinstance(arg[-1], dict): 
        # Surreptiously setting keyword arguments:
        kw2 = arg[-1]
        kw.update(kw2)
        arg = arg[0:-1]
    else:
        pass

    narg = len(arg)
    helperargs = arg[2:narg-2]
    data = np.array(arg[-2], copy=False)
    weights = arg[-1]

    if data.ndim > 1:
        print "I haven't implemented 2D multi-dimensional data handling yet!"
    else:
        ndata = data.size

    
    if kw.has_key('npars'):
        print "I haven't yet dealt with this for prayerbead analyses!"
        npars = kw['npars']
        ret = []
        # Excise "npars" kw for recursive calling:
        lower_kw = kw.copy()
        junk = lower_kw.pop('npars')

        # Keep fixed pairs of joint parameters:
        if kw.has_key('jointpars'):
            jointpars = kw['jointpars']
            for jointpar in jointpars:
                params[jointpar[1]] = params[jointpar[0]]

        for ii in range(len(npars)):
            i0 = sum(npars[0:ii])
            i1 = i0 + npars[ii]
            these_params = arg[0][i0:i1]
            ret.append(resfunc(these_params, *arg[1][ii], **lower_kw))

        return ret


    

    fitter_args = (modelfunction,) + helperargs + (data, weights, kw)
    #fitter = kmpfit.Fitter(residuals=pc.devfunc, data=fitter_args)
    #fitter.parinfo = parinfo
    #fitter.fit(params0=guessparams)
    fmin_fit = fmin(pc.errfunc, guessparams, args=fitter_args, full_output=True, disp=False, maxiter=maxiter, maxfun=maxfun)
    bestparams = np.array(fmin_fit[0], copy=True)
    bestmodel = modelfunction(*((guessparams,) + helperargs))
    residuals = data - bestmodel
    allfits = np.zeros((ndata, nparam), dtype=float)
    allfits[0] = bestparams
    if verbose: print "Finished prayer bead step ",
    for ii in range(1, ndata):
        shifteddata = bestmodel + np.concatenate((residuals[ii::], residuals[0:ii]))
        shiftedweights = np.concatenate((weights[ii::], weights[0:ii]))
        shifted_args = (modelfunction,) + helperargs + (shifteddata, shiftedweights, kw)

        fmin_fit = fmin(pc.errfunc, bestparams, args=shifted_args, full_output=True, disp=False, maxiter=maxiter, maxfun=maxfun, xtol=xtol, ftol=ftol)
        theseparams = fmin_fit[0]

        #lsq_fit = optimize.leastsq(pc.devfunc, bestparams, args=shifted_args, full_output=True)
        #theseparams = lsq_fit[0]
        #lsq_fit = lsq_fit[1]
        #bestchisq = pc.errfunc(bestparams, *fitargs)



        #newfitter = kmpfit.Fitter(residuals=pc.devfunc, data=shifted_args)
        #newfitter.parinfo = parinfo
        #newfitter.ftol = 1e-12
        #newfitter.xtol = 1e-12


        #try:
        #    newfitter.fit(params0=bestparams)
        #except:
        #    print "Fitter crashed -- entering debug.  Enter 'q' to quit."
        #theseparams = newfitter.params
        #del newfitter

        #bestmodel = modelfunction(*((guessparams,) + helperargs))
        #residuals = data - bestmodel
        #chisq = pc.errfunc(newfitter.params, *shifted_args)
        allfits[ii] = theseparams
        if verbose: print ("%i of %1." % (ii+1, ndata)),
        #pdb.set_trace()

    return allfits

def morlet(scale, k, k0=6.0, retper=False, retcoi=False, retcdelta=False, retpsi0=False):   # From Wavelet.pro; still incomplete!
    n = len(k)
    expnt = -0.5 * (scale * k - k0)**2 * (k > 0.) 
    dt = 2 * np.pi / (n*k[1])
    norm = np.sqrt(2*np.pi*scale/dt) * (np.pi**-0.25) # total energy=N
    morlet = norm * np.exp( np.max(np.array([expnt, 0.*expnt]), 0) )
    morlet = morlet * (expnt > -100) # avoid underflow errors
    morlet = morlet * (k > 0) # Heaviside step function (Morlet is complex)
    fourier_factor = (4 * np.pi) / (k0 + np.sqrt(2. + k0**2)) # Scale --> Fourier
    period = scale * fourier_factor
    coi = fourier_factor / np.sqrt(2)  # Cone-of-influence
    dofmin = 2
    Cdelta = -1
    if k0==6:  Cdelta = 0.776
    psi0 = np.pi**-0.25
    ret =  (morlet,)
    if retper:
        ret = ret + (period,)
    if retcoi:
        ret = ret + (coi,)
    if retcdelta:
        ret = ret + (cdelta,)
    if retpsi0:
        ret = ret + (psi0,)
    if len(ret)==1:
        ret = ret[0]
    return ret




def test_eccentric_anomaly(ecc, manom, tol=1e-8):
    """ Test various methods of computing the eccentric anomaly.

    ecc = scalar; manom = 1D NumPy array

    Just run, e.g.:
      ::

        ecc = 0.15
        p_orb = 3.3
        mean_anom = 2*pi*linspace(0, p_orb, 10000)/p_orb
        an.test_eccentric_anomaly(ecc, mean_anom, tol=1e-10)

        """
    # 2012-10-15 21:46 IJMC: Created, for my own curiosity.
    from time import time

    e0 = np.zeros(manom.size)
    e1 = np.zeros(manom.size)
    e2 = np.zeros(manom.size)
    e3 = np.zeros(manom.size)

    tic = time()
    for ii,element in enumerate(manom):
        def kep(e): return element - e + ecc*sin(e)
        e0[ii] = optimize.brentq(kep, element-1, element+1,  xtol=tol, disp=False)
    toc0 = time() - tic

    tic = time()
    for ii,element in enumerate(manom):
        def kep(e): return element - e + ecc*sin(e)
        e1[ii] = optimize.newton(kep, ecc, tol=tol)
    toc1 = time() - tic

    tic = time() 
    guessfactor = np.pi * (ecc+0.01) / 0.81 # guess=pi for ecc=0.8
    for ii,element in enumerate(manom): # Explicit Newton's method
        err = tol*10
        val = guessfactor
        while np.abs(err) > tol:
            err = (element + ecc*np.sin(val) - val) / (1. - ecc*np.cos(val))
            val += err
        e2[ii] = val
    toc2 = time() - tic
    
    tic = time()
    for ii,element in enumerate(manom): # simple iteration:
        err = tol*10
        oldval = 0.
        while np.abs(err) > tol:
            val = element + ecc * np.sin(oldval)
            err = val - oldval
            oldval = val
        e3[ii] = val
    toc3 = time() - tic
    
    print "SciPy BrentQ:     [%1.6f, %1.6f, ....] -- %1.4f s" % (e0[0], e0[1], toc0)
    print "SciPy Newton:     [%1.6f, %1.6f, ....] -- %1.4f s" % (e1[0], e1[1], toc1)
    print "Explicit Newton:  [%1.6f, %1.6f, ....] -- %1.4f s" % (e2[0], e2[1], toc2)
    print "Simple iteration: [%1.6f, %1.6f, ....] -- %1.4f s" % (e3[0], e3[1], toc3)
    return


def fmin_helper(params, func=None, **kw_dict):
    return fmin(func, params, **kw_dict)

def fmin_helper2(all_args):
    if isinstance(all_args[-1], dict):
        ret = fmin(all_args[0], *all_args[1:-1], **all_args[-1])
    else:
        ret = fmin(all_args[0], *all_args[1:-1])
    return ret



def gfit(func, x0, fprime, args=(),  kwargs=dict(), maxiter=2000, ftol=0.001, factor=1., disp=False, bounds=None):
    """Perform gradient-based minimization of a user-specified function.

    :INPUTS:
      func : function
        Function that takes as input the parameters x0, optional
        additional arguments args, and optional keywords kwargs, and
        returns the metric to be minimized as a scalar.  For chi-squared
        minimization, a generalized option is :phasecurves:`errfunc`.

      x0 : sequence
        List or 1D NumPy array of initial-guess parameters, to be
        adjusted to minimize func(x0, *args, **kwargs).

      fprime : function
        Function that takes as input the parameters x0, optional
        additional arguments args, and optional keywords kwargs, and
        returns the partial derivatives of the metric to be minimized
        with regard to each element of x0. 

      args : list
        Optional arguments to func and fprime (see above)

      kwargs : dict
        Optional keywords to func and fprime (see above)

      maxiter : int
        Maximum number of iterations to run.

      ftol : scalar
        Desired tolerance on the metric to be minimized.  Iteration
        will continue until either iter>maxiter OR 
        (metric_i - metric_(i+1)) < ftol.

      factor : scalar
        Factor to scale gradient before applying each new
        iteration. Small values will lead to slower convergences;
        large values will lead to wild behavior. The code attempts to
        (crudely) tune the value of 'factor' depending on how the
        minimization process progresses.

      disp : bool
        If True, print some text to screen on each iteration.

      bounds : None, or list
        (min, max) pairs for each element in x0, defining the
        bounds on that parameter. Use None or +/-inf for one of
        min or max when there is no bound in that direction.


    :RETURNS:
      (params, metric, n_iter)

    :NOTES:
      The program attempts to be slightly clever: if the metric
      decreases by <ftol on one iteration, the code iterates one more
      time. If the termination criterion is once again met then
      minimization ends; if not, minimization continues as before.

      For quicker, smarter routines that do much the same thing, you
      may want to check out the functions in the scipy.optimize package.
    """
    # 2013-08-09 10:37 IJMC: Created
    # 2013-08-11 16:06 IJMC: Added a missing boolean flag
    
    if bounds is not None:
        bounds = np.array(bounds)

    def applyBounds(params):
        if bounds is not None:
            params = np.vstack((params, bounds[:,0])).max(0)
            params = np.vstack((params, bounds[:,1])).min(0)
        return params

    bestparams = applyBounds(x0)
    nx = bestparams.size

    metric = func(x0, *args, **kwargs)
    dmetric = 9e9
    keepFitting = True
    lastIterSaidToStop = False
    

    iter = 0
    recalcGrad = True
    if disp:
        fmtstr = '%7i   %1.'+str(np.abs(np.log(ftol)).astype(int)+2)+'f   %1.5e   %1.3e'
        print '  ITER       METRIC         FACTOR             DMETRIC'
    while iter<maxiter and keepFitting:
        iter += 1
        if recalcGrad: grad = fprime(bestparams, *args, **kwargs)
        newparam = applyBounds(bestparams - factor * grad)
        newmetric = func(newparam, *args, **kwargs)
        if newmetric < metric:
            bestparams = newparam.copy()
            dmetric = newmetric - metric
            metric = newmetric
            if recalcGrad is True: factor *= 1.5  # we updated twice in a row!
            recalcGrad = True
            if np.abs(dmetric) < ftol:
                if disp: print "Met termination criterion"
                if lastIterSaidToStop:
                    keepFitting = False
                else:
                    lastIterSaidToStop = True
        else:
            factor /= 2
            recalcGrad = False
            lastIterSaidToStop = False
            
        if disp: print fmtstr % (iter, metric, factor, dmetric)

    return bestparams, metric, iter