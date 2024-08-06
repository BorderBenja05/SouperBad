import numpy as np
import random
import os
from paths import TRAINING_DIR, FUNPACKED_FITS, INJECTED_FITS, CAT_DIR


def read_cat_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Skip the first 8 lines
        data_lines = lines[8:]
        
        # Process the remaining lines
        for line in data_lines:
            # Only process lines that are not empty or comments
            if line.strip() and (line[0].isdigit() or line[0] == ' '):
                # Split the line into elements and convert to appropriate types
                row = [float(x) if '.' in x or 'e' in x.lower() else int(x) for x in line.split()]
                data.append(row)
                
    return data

def get_indexes_above_threshold(data, threshold=0.02):
    indexes = []
    for i, row in enumerate(data):
        if row[1] > threshold:
            if row[2] >80 and row[2] < 9495:
                if row[3] > 80 and row[3] < 6307:
                    indexes.append(i)
    print(f'there are {len(indexes)} sources that pass the galaxy check')
    return indexes

def get_indexes_of_stars(data, threshold=.007, max_size = 20):
    indexes = []
    for i, row in enumerate(data):
        if row[1] < threshold and (row[4] + row[5]) < max_size: #max size is the max sum of the major and minor axis'
            if row[2] >80 and row[2] < 9495:
                if row[3] > 80 and row[3] < 6307:
                    indexes.append(i)
    print(f'there are {len(indexes)} sources that pass the star check for size and spread')
    return indexes

def getcenter(infile):
    fname = infile.replace('.fits', '.cat')
    fname= os.path.basename(fname)
    if not os.path.exists(f'{CAT_DIR}/{fname}'):
        os.system(f'sex {infile}     -c /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/default.sex     -FILTER_NAME /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/default.conv     -PARAMETERS_NAME /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/starfinder.param     -CATALOG_NAME {CAT_DIR}/{fname} -PSF_NAME /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/default.psf')
    print(f'using catalog {fname}')
    data = read_cat_file(f'{CAT_DIR}/{fname}')
    indexes = get_indexes_above_threshold(data)
    galdex = []
    gals = []
    try:
        for i in range(len(indexes)): 
            galdex.append(indexes[i])
            gals.append([data[galdex[i]][2], data[galdex[i]][3]])
    except:
        gals = None
    # print(gals)
    return gals

def getStars(infile):
    fname = infile.replace('.fits', '.cat')
    fname= os.path.basename(fname)
    if not os.path.exists(f'{CAT_DIR}/{fname}'):
        os.system(f'sex {infile}     -c /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/default.sex     -FILTER_NAME /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/default.conv     -PARAMETERS_NAME /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/starfinder.param     -CATALOG_NAME {CAT_DIR}/{fname} -PSF_NAME /home/borderbenja/anaconda3/envs/pipeline/share/sextractor/default.psf')
    print(f'using catalog {fname}')
    data = read_cat_file(f'{CAT_DIR}/{fname}')
    indexes = get_indexes_of_stars(data)
    stardex = []
    stars = []
    try:
        for i in range(len(indexes)): 
            stardex.append(indexes[i])
            stars.append([data[stardex[i]][2], data[stardex[i]][3]])
    except:
        stars = None
    # print(gals)

    return stars
        

# # Example usage
# file_path = 'funpacked_fits/test.cat'
# getcenter(file_path, 4)
# # print(indexes)
