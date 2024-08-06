# MSSG, 12-22-2023
# Code to insert a star at a given location in a FITS file -- very fast

from astropy.io import fits
import sys
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

def gaussian(x, y, mean_x, mean_y, sigma_x, sigma_y):
  """
  This function defines a 2D Gaussian distribution.

  Args:
      x: Array of x-coordinates.
      y: Array of y-coordinates.
      mean_x: Mean value for the x-axis.
      mean_y: Mean value for the y-axis.
      sigma_x: Standard deviation for the x-axis.
      sigma_y: Standard deviation for the y-axis.

  Returns:
      A 2D array representing the Gaussian distribution.
  """
  return np.exp(-(((x - mean_x) ** 2) / (2 * sigma_x**2) + ((y - mean_y) ** 2) / (2 * sigma_y**2)))


# # Define desired dimensions of the output array
# array_size = 200
# small_array_size = 150

# # Create meshgrid for x and y coordinates
# x, y = np.meshgrid(np.linspace(-5, 5, small_array_size), np.linspace(-5, 5, small_array_size))

# # Define Gaussian parameters
# mean_x = 0
# mean_y = 0
# sigma_x = 2
# sigma_y = 2  # Adjust sigma for different spread in y direction

# # Generate the 2D Gaussian array
# gaussian_array = gaussian(x, y, mean_x, mean_y, sigma_x, sigma_y)

# print(f'*********** g array = {gaussian_array}')

# # Assuming you have a 2D array named 'target_array'
# target_array = np.zeros((array_size, array_size))  # Example empty array

# # Select a location for the Gaussian (adjust row_start and col_start for placement)
# row_start = 50
# col_start = 50

# print(f'{gaussian_array.shape[0]}, {gaussian_array.shape[1]}')
# # Place the Gaussian on the target array
# target_array[row_start:row_start + gaussian_array.shape[0], col_start:col_start + gaussian_array.shape[1]] = gaussian_array

# # Now 'target_array' will have the Gaussian distribution placed at the specified location

# # Create the heatmap
# plt.imshow(target_array, cmap="viridis")  # Choose a colormap (e.g., "viridis", "plasma")

# # Add labels and title
# plt.xlabel("X-axis")
# plt.ylabel("Y-axis")
# plt.title("Heatmap of 2D Array")

# # Add colorbar
# plt.colorbar(label="Values")

# # Display the heatmap
# #plt.show()

# exit()

############

if (len(sys.argv) >= 2):
    f_in=sys.argv[1]
else:
    print('************ Need input file my dude/tte!')
    exit()


# Open full filename given in cmd line, with abspath
print(f'********* Opening {f_in}')
f=fits.open(f_in)            

# Pull out just the name without the .fits extension
filename=f_in.split('/')[-1]  # Remove path and only get the file name
print(f"****** {filename}") 
fname=filename.replace('.fits','')    # Remove .fits
print(f'********* Working with {fname}')


# Pull out the 2D array data from the primary header HDU into dat
dat=f['primary'].data  
print(type(dat))


############################################### Locations of stars to copy for some specific files
############ M82 test file #'s
#star=dat[3205:3230,4890:4915]  # For the particular testfile telescope_r_M82_2023_11_19_03_25_42.fits, I found a large bright star in this location, so this is a 25x25 pixel cutout of it
#dat[3205:3230,4850:4875] = star  #  copy that star into a place 40 pixels to the left of it which initially was just random noise

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

################# For telescope_r_ArturusA_2024_04_12_23_22_07.fits
yc = 2830 ; xc = 3320  # semi-dim
yc = 2850 ; xc = 3320 #bright

##############  telescope_r_Virgo_Cluster_2024_04_13_01_45_29.fits
yc= 5100 ; xc = 2700


############### Figure out the edges of the star window to cut out
window = 30 # pixels from L to R and Top to Bottom
half_window = int(window/2)

xmin = xc-half_window ; xmax = xc+half_window
ymin = yc-half_window ; ymax = yc + half_window

# ########### How far to go away from the start to insert it
xshift = yshift = 100


# star=dat[xmin:xmax, ymin:ymax ]     # Get the star 

################# Insert star into locations of the plus sign
# dat[ xmin:xmax, ymin-yshift:ymax-yshift ] = star    # copy that star into a place yshift pixels low 
# dat[ xmin:xmax,  ymin+yshift:ymax+yshift  ] = star  # copy that star into a place 40 pixels high
# dat[ xmin-xshift:xmax-xshift, ymin:ymax ] = star    # copy that star into a place 40 pixels to the left 
# dat[ xmin+xshift:xmax+xshift, ymin:ymax ] = star    # copy that star into a place 40 pixels to the right


#### If you want to add at the corners of the square also, comment back in
# dat[  xmin-xshift:xmax-xshift,  ymin+yshift:ymax+yshift  ] = star  #  copy that star into a place yshift high, xshift left
# dat[ xmin-xshift:xmax-xshift, ymin-yshift:ymax-yshift ] = star  #  copy that star into a place yshift low, xshift left 
# dat[ xmin+xshift:xmax+xshift, ymin-yshift:ymax-yshift   ] = star  #  copy that star into a place xshift right, yshift low  
# dat[ xmin+xshift:xmax+xshift, ymin+yshift:ymax+yshift  ] = star  #  copy that star into a place xshift right, yshift high

# To insert up and down twice as far
# dat[ xmin:xmax, ymin-2*yshift:ymax-2*yshift ] = star  #  copy that star into a place 2*yshift pixels low 
# dat[ xmin:xmax,  ymin+2*yshift:ymax+2*yshift  ] = star  #  copy that star into a place 2*yshift pixels high





#################################### For putting stars on top of galaxies

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

################# For telescope_g_UGC_5900_2024_03_15_03_07_56.fits
yc=4228 ;xc= 4038
galy=4300
galx = 3969

window = 30 # pixels from L to R and Top to Bottom
half_window = int(window/2)

xmin = xc-half_window ; xmax = xc+half_window
ymin = yc-half_window ; ymax = yc + half_window




##### Define desired dimensions of the output array
# array_size = 200
small_array_size = 30

# Create meshgrid for x and y coordinates
x, y = np.meshgrid(np.linspace(-5, 5, small_array_size), np.linspace(-5, 5, small_array_size))

# Define Gaussian parameters
mean_x = 0
mean_y = 0
sigma = 0.3
sigma_x = sigma
sigma_y = sigma  # Adjust sigma for different spread in y direction

amp = 1000
# Generate the 2D Gaussian array
gaussian_star = amp * gaussian(x, y, mean_x, mean_y, sigma_x, sigma_y)

gaussian_star= gaussian_star.astype(np.uint16)
print(gaussian_star)
print(f'*********** g array = {gaussian_star}')


print(type(gaussian_star[0,0]))
print(type(dat[0,0]))
# Place the Gaussian on the target array

rightshift= 10

half_window = int(small_array_size / 2)
dat[galx + shift - half_window : galx + shift + half_window, galy - half_window : galy + half_window] += gaussian_star
dat[galx - shift - half_window : galx - shift + half_window, galy - half_window : galy + half_window] += gaussian_star
# dat[galx - half_window : galx + half_window, galy - shift - half_window : galy - shift + half_window] += gaussian_star
# dat[galx - half_window : galx + half_window, galy + shift - half_window : galy + shift + half_window] += gaussian_star
# dat[galx - half_window + rightshift : galx + half_window + rightshift, galy - half_window : galy  + half_window] += gaussian_star

# Now 'target_array' will have the Gaussian distribution placed at the specified location

# star=dat[xmin:xmax, ymin:ymax ]   
# median = np.median(star)

# shift = 30
# #print(star)
# #print(star-median)
# star = np.round(star-median).astype('uint16')



# Correct the slicing indices
# dat[galx + shift - half_window : galx + shift + half_window, galy - half_window : galy + half_window] += gaussian_star
# dat[galx - shift - half_window : galx - shift + half_window, galy - half_window : galy + half_window] += gaussian_star
# dat[galx - half_window : galx + half_window, galy - shift - half_window : galy - shift + half_window] += gaussian_star
# dat[galx - half_window : galx + half_window, galy + shift - half_window : galy + shift + half_window] += gaussian_star
# dat[galx - half_window : galx + half_window, galy - half_window : galy + half_window] += gaussian_star # Center, really doesn't work for some reason


######## New fits
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
        



# ######### for Virgo
# galy = 3880
# galx =  290
# shift = 40
# # Up down twice as far
# dat[ galx + shift -half_window :galx + shift + half_window, galy -half_window:galy + half_window ] = star
# dat[ galx - shift -half_window :galx - shift + half_window, galy -half_window:galy + half_window ] = star
# dat[ galx  -half_window :galx  + half_window, galy -shift -half_window:galy - shift + half_window ] = star
# dat[ galx  -half_window :galx  + half_window, galy +shift -half_window:galy + shift+ half_window ] = star
 
