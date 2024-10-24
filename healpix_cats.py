#!/usr/bin/python


'''
This is a script to divide the combined optical/IR and radio catalogues up into
HEALPix areas to allow for the smaller sky areas to be passed through the next
stages of the pipeline.

Author: B. Barkus
Version: 0.001

Inputs:
1 - Data directory that the hp folder containing all the catalogues will be created in
2 - The optical input catalogue
3 - The radio input catalogue

'''

# Imports

import sys
import os
import numpy as np
from astropy.table import Table, vstack, unique
from astropy_healpix import HEALPix
import astropy.units as u


# Arguments
'''
These need to be the combined optical/IR and radio catalogues.
'''

dir = sys.argv[1]                               # Working directory to change to and run the code from 
optcat = sys.argv[2]                            # Path to combined optical/IR catalogue
radcat = sys.argv[3]                            # Path to radio catalogue
gauscat = sys.argv[4]                           # Path to radio gaussian catalogue

# Main Code

'''
This code is going to assign HEALPix values to the RA and DEC pairs and place these
in a new column in the tables.
New catalogues for the radio and combined optical/IR are generated by filtering on
the unique HEALPix numbers and saving the corresponding sources out.
There is also code included for filtering the radio catalogue down if needed at any
but is shouldn't as this is an initial step.
There is also code included which can detect the nearest neighbour areas for the
HEALPix in case this is helpful for the LR and LR threshold determination.
New directories can be created for the new catalogues, but I am not sure this is
necessary.
'''

# Set up

os.chdir(dir)                                   # Move to working/data directory (should be bound to container)

data_path = os.path.join(dir, "Data")

#try:
#    BASEPATH = os.path.dirname(os.path.realpath(__file__))
#    data_path = os.path.join(BASEPATH, "..", "..", "data")
#except NameError:
#    if os.path.exists("data"):
#        BASEPATH = "."
#        data_path = os.path.join(BASEPATH, "data")
#    else:
#        BASEPATH = os.getcwd()
#        data_path = os.path.join(BASEPATH, "..", "..", "data")

outroot= os.path.join(data_path, 'hp')          # Setting up the folder for outputting the hp catalogues
try:
    os.mkdir(outroot)
except:
    print("Directory "+outroot+" exists")

os.chdir(outroot)                               # Move to outroot to work in

hp = HEALPix(nside=16)                          # Setting the size of the HEALPix areas

# Reading in catalogues and filtering if necessary

print('Reading catalogues...')
rcat=Table.read(radcat)                         # Read in radio catalogue
ocat=Table.read(optcat)                         # Read in combined optical/IR catalogue
gcat=Table.read(gauscat)

# Converting the coordinates and creating the HEALPix id column for radio and optical/IR

#hpix=hp.lonlat_to_healpix(rscut['RA'].value*u.deg,rscut['DEC'].value*u.deg)    # If filtered need this line

rhpix=hp.lonlat_to_healpix(rcat['RA'].value*u.deg,rcat['DEC'].value*u.deg)       # Create HEALPix id column from RA and DEC in degs

ruhp=sorted(np.unique(rhpix))                                         # Sorted list of the unique hp values in hpix
print('There are',len(ruhp),'healpixes in the radio catalogue')       # How many of these are there?

ghpix=hp.lonlat_to_healpix(gcat['RA'].value*u.deg,gcat['DEC'].value*u.deg)       # Create HEALPix id column from RA and DEC in degs

guhp=sorted(np.unique(ghpix))                                         # Sorted list of the unique hp values in hpix
print('There are',len(guhp),'healpixes in the Gaussian catalogue')       # How many of these are there?

ohpix=hp.lonlat_to_healpix(ocat['RA'].value*u.deg,ocat['DEC'].value*u.deg)

ouhp=sorted(np.unique(ohpix))                                          # Sorted list of the unique hp values in hpix
print('There are',len(ouhp),'healpixes in the optical catalogue')      # How many of these are there?

# Loop through pairs to create the catalogues

for i,pix in enumerate(ruhp):                    # Create pairs of index and hp value from uhp to loop through
    print('Doing healpix',i,pix)
    #bdir=outroot+'_'+str(pix)                  # The bdir lines allow for splitting into separate directories
    rname = 'radio_'+str(pix)+'.fits'
    gname = 'gaussian_'+str(pix)+'.fits'
    oname = 'optical_'+str(pix)+'.fits'
    onname = 'optical_'+str(pix)+'_nn.fits'
    rnname = 'radio_'+str(pix)+'_nn.fits'
    gnname = 'gaussian_'+str(pix)+'_nn.fits'
    #newrcat=rscut[hpix==pix]
    newrcat = rcat[rhpix==pix]
    newgcat = gcat[ghpix==pix]
    newocat = ocat[ohpix==pix]
    #try:                                       # This section creates new directories for each HEALPix area
    #    os.mkdir(bdir)
    #except:
    #    print("Directory "+bdir+" exists")
    if len(newocat) > 0:
        if not os.path.exists(rname):          # Check if rname already exists
            newrcat.write(rname,overwrite=True)
            print(f'Created: {rname}')
        else:
            print(f'File already exists: {rname}')
        if not os.path.exists(gname):          # Check if gname already exists
            newrcat.write(gname,overwrite=True)
            print(f'Created: {gname}')
        else:
            print(f'File already exists: {gname}')
        if not os.path.exists(oname):          # Check if oname already exists
            newocat.write(oname,overwrite=True)
            print(f'Created: {oname}')
        else:
            print(f'File already exists: {oname}')            

    
# The following code takes the neighbours for each hp area and creates a catalogue 
# for all the nearby areas, kept in if it is needed for LR calculations can delete 
# if not required.
    
        neighbours=np.ndarray.flatten(hp.neighbours(pix))
        
        rmask=np.zeros_like(rhpix,dtype=bool)
        for npix in list(neighbours)+[pix]:
            rmask|=(rhpix==npix)
        if not os.path.exists(rnname):          # Check if rnname already exists
            rcat[rmask].write(rnname,overwrite=True)
            print(f'Created: {rnname}')
        else:
            print(f'File already exists: {rnname}') 
            
        gmask=np.zeros_like(ghpix,dtype=bool)
        for npix in list(neighbours)+[pix]:
            gmask|=(ghpix==npix)
        if not os.path.exists(gnname):          # Check if gnname already exists
            gcat[gmask].write(gnname,overwrite=True)
            print(f'Created: {gnname}')
        else:
            print(f'File already exists: {gnname}')
            
        omask=np.zeros_like(ohpix,dtype=bool)
        for npix in list(neighbours)+[pix]:
            omask|=(ohpix==npix)
        if not os.path.exists(onname):          # Check if onname already exists
            ocat[omask].write(onname,overwrite=True)
            print(f'Created: {onname}')
        else:
            print(f'File already exists: {onname}')


'''
The following is the filtering code incase it is needed at a later date otherwise 
it can be deleted.
'''
# Filter radio catalogue for flux and size

#rfcut=rcat[rcat['Total_flux']>10.0]
#rmcutf=rfcut['Maj']>15.0
#rlcutf=rfcut['LGZ_Size']>15.0
#rscut=rfcut[rmcutf | rlcutf]
#print("Length of rm, rl: ",np.sum(rmcutf),np.sum(rlcutf))

#lrad=len(rscut)
#print("Length of filtered radio catalogue is "+str(lrad))
#rscut.write("radio_filtered.fits",overwrite=True)      # Delete once confident not required

# Filter optical catalogue for WISE dets                # Delete once confident not required

#ocut=ocat[ocat['UNWISE_OBJID']!="N/A"]

#print("Length of filtered hosts catalogue is "+str(len(ocut)))
#ocut.write("optical_filtered.fits",overwrite=True)


