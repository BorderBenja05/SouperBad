import numpy as np
import time
from getcenters import getcenter
import gaussian as ga
from os import listdir
from os.path import isfile, join

fits_path = 'funpacked_fits/'
out_path = 'injected_fits/'

files = [f for f in listdir(fits_path) if isfile(join(fits_path, f))]
print(files)

def make_trainer(infile,out_path):
    tstart =time.time()
    gal_num = np.random.randint(8,10)
    print(gal_num)
    x,y = getcenter(infile,gal_num)
    x = int(x); y = int(y)
    x, y, sigma, amp, small_array_size, outname = ga.insert_gaussian(infile,out_path, .13, 1.5, x, y)
    print(time.time()-tstart)
    print(x,y)
    outname = outname.replace('injected_fits/', '')
    with open('starcoords.csv', 'a') as f:
        f.write(f"{outname},{x},{y},{sigma},{amp},{small_array_size}\n")
# make_trainer(fits_path,out_path)
for file in files:
    make_trainer(f'{fits_path}{file}',out_path)