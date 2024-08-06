# MSSG, 12-22-2023
# Code to insert a star at a given location in a FITS file -- very fast

from astropy.io import fits
import sys
import numpy as np

if (len(sys.argv) >= 2):
    f_in=sys.argv[1]
else:
    print('************ Need input file my dude/tte!')
    exit()


# Open full filename given in cmd line, with abspath
print(f'********* Opening {f_in}')
f=fits.open(f_in)            

print(f'****************** f = {f}')

# Pull out just the name without the .fits extension
filename=f_in.split('/')[-1]  # Remove path and only get the file name
print(f"****** {filename}") 
fname=filename.replace('.fits','')    # Remove .fits
print(f'********* Working with {fname}')


fp = f['primary']


# Pull out the 2D array data from the primary header HDU into dat
dat=f['primary'].data  
print(type(dat))


############ M82 test file #'s
#star=dat[3205:3230,4890:4915]  # For the particular testfile telescope_r_M82_2023_11_19_03_25_42.fits, I found a large bright star in this location, so this is a 25x25 pixel cutout of it
#dat[3205:3230,4850:4875] = star  # Here I copy that star into a place 40 pixels to the left of it which initially was just random noise


########### #'s for # Sn2023tsz: telescope_g_SN_2023tsz_2024_02_13_20_13_26.fits 
# xmin = 2550 ; xmin = 2580
# ymin = 3380 ; ymax = 3420

#############  For telescope_g_S240413p_5769_2024_04_14_02_08_29.fits 
yc = 4540 ; xc = 3270  

############# For telescope_r_S240413p_6504_2024_04_14_22_10_16.fits
yc = 4780 ; xc = 3080
yc = 4800 ; xc = 3450

############### For telescope_g_S240413p_5954_2024_04_14_23_26_43.fits
yc = 5800 ; xc = 3375  # brighter star
yc = 5890 ; xc = 3400  # dimmer star

################ For telescope_g_UGC_4132_2024_04_13_00_02_24.fits
yc = 4597; xc = 2423
galy = 5992
galx = 3311

################# For telescope_r_UGC_5900_2024_04_13_04_34.fits
yc = 5088 ; xc = 3067
galy=5240
galx = 5424


################# For telescope_r_UGC_5900_2024_04_13_04_34.fits
yc = 5452 ; xc = 5313
galy=5240
galx = 5424

################# For telescope_r_Virgo_Cluster_2024_04_24_03_23_42.fits
yc = 7691; xc = 3936  # semi-dim
galy = 7825
galx =  3896
shift = 55
########### for telescope_g_UGC_4132_2024_04_13_00_02_24.fits(1)
yc= 6073; xc = 3222
galy = 5991
galx = 3309
#for the 2nd one:
yc =2260; xc= 1438
galy = 2396
galx = 1290

################# For telescope_r_UGC_5900_2024_03_15_03_07_56.fits
yc=4228 ;xc= 4038
galy=4298
galx = 3969

window = 30 # pixels from L to R and Top to Bottom
half_window = int(window/2)

xmin = xc-half_window ; xmax = xc+half_window
ymin = yc-half_window ; ymax = yc + half_window


########### To insert star
xshift = yshift = float(100)

star=dat[xmin:xmax, ymin:ymax ]   
median = np.median(star)
# dat[ xmin:xmax, ymin-yshift:ymax-yshift ] = star  # Here I copy that star into a place yshift pixels low 
# dat[ xmin:xmax,  ymin+yshift:ymax+yshift  ] = star  # Here I copy that star into a place 40 pixels high
# dat[ xmin-xshift:xmax-xshift, ymin:ymax ] = star  # Here I copy that star into a place 40 pixels to the left 
# dat[ xmin+xshift:xmax+xshift, ymin:ymax ] = star  # Here I copy that star into a place 40 pixels to the right

#### If you want at the corners of the square also, comment back in
# dat[ xmin-xshift:xmax-xshift, ymin-yshift:ymax-yshift ] = star  # Here I copy that star into a place yshift low, xshift left 
# dat[  xmin-xshift:xmax-xshift,  ymin+yshift:ymax+yshift  ] = star  # Here I copy that star into a place yshift high, xshift left
# dat[ xmin+xshift:xmax+xshift, ymin-yshift:ymax-yshift   ] = star  # Here I copy that star into a place xshift right, yshift low  
# dat[ xmin+xshift:xmax+xshift, ymin+yshift:ymax+yshift  ] = star  # Here I copy that star into a place xshift right, yshift high
shift = 35
print(star)
print(star-median)
star = np.round(star-median).astype('uint16')

# Up down twice as far
# Correct the slicing indices
# print(f'top left corner value before={dat[galx + shift -half_window,galy -half_window]}')
# print(f'top right corner before: {dat[galx + shift + half_window-1, galy + half_window-1]}')
# print(f'bottom left value before: {dat[galx - half_window, galy - shift - half_window]}')
#print(star)
# medianarray =np.ArrayLike(star,median)
dat[galx + shift - half_window : galx + shift + half_window, galy - half_window : galy + half_window] += star
dat[galx - shift - half_window : galx - shift + half_window, galy - half_window : galy + half_window] += star 
dat[galx - half_window : galx + half_window, galy - shift - half_window : galy - shift + half_window] += star
dat[galx - half_window : galx + half_window, galy + shift - half_window : galy + shift + half_window] += star
# print(f'top left value after={dat[galx + shift -half_window,galy -half_window]}')
# print(f'top right corner after: {dat[galx + shift + half_window-1, galy + half_window-1]}')
# print(f'bottom left value after: {dat[galx - half_window, galy - shift - half_window]}')

newhdu = fits.PrimaryHDU(dat)  # This creates a new HDU based on the old
newhdu.name='primary'  # And gives it the name 'primary'

# This copies each key from the old HDU to the new one
for key in f['primary'].header:
    try:
        newhdu.header[key] = f['primary'].header[key]
        print(f"************** {key}, {f['primary'].header[key]}")
    except: 
        print('failed')

# Create a name for the new file
newname=fname + '.with_inserted_star.fits'

# And write out the entire file to disk 
# (will just do this locally, where the script is called, for now)
newhdu.writeto(newname,overwrite=True, output_verify='ignore')

print(f'********* wrote out {newname}')
 
exit()

### This was extra code to figure out the maximum value of the pixels in that range
hival = 0  # Variable we will need to figure out what the highest pixel value is
for x in range(3210,3230):
    for y in range(4895,4915):
        val = star[x,y]
        if val>hival:
            hival = val
            xmax = x ; ymax = y
            print(f' newhival: {x} {y}  {val}')
        print(f' {x} {y}  {val}')

print(f' max: {xmax} {ymax}  {hival}')        
        


 
