import os
import numpy as np
import sys
import matplotlib.pyplot as plt
from astropy.io import fits
from mpl_toolkits.mplot3d import Axes3D
import argparse
import time
from paths import TRAINING_DIR, OUTSIDE_DIR
from pathlib import Path



def analyze_poisson_noise(flats_file, chunk_size=15, plots=False, output_dir='plots'):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    

    
    # Load the FITS image
    with fits.open(flats_file) as hdul:
        data = hdul[0].data
    
    # Get image dimensions
    img_height, img_width = data.shape

    # Calculate the number of chunks
    num_chunks_height = img_height // chunk_size
    num_chunks_width = img_width // chunk_size
    
    means = np.zeros((num_chunks_height + 1, num_chunks_width + 1))
    medians = np.zeros((num_chunks_height + 1, num_chunks_width + 1))
    stds = np.zeros((num_chunks_height + 1, num_chunks_width + 1))
    
    # Iterate over the image in chunks of size chunk_size x chunk_size
    for i in range(num_chunks_height + 1):
        for j in range(num_chunks_width + 1):
            # Find the anchor corner
            start_i = i * chunk_size
            start_j = j * chunk_size

            # Define the chunk
            if i != num_chunks_height and j != num_chunks_width:
                chunk = data[start_i:start_i + chunk_size, start_j:start_j + chunk_size]
            elif i == num_chunks_height and j != num_chunks_width:
                chunk = data[start_i:img_height, start_j:start_j + chunk_size]
            elif j == num_chunks_width and i != num_chunks_height:
                chunk = data[start_i:start_i + chunk_size, start_j:img_width]
            else:
                chunk = data[start_i:img_height, start_j:img_width]
            
            median = np.median(chunk)
            mean = np.mean(chunk)
            std = np.std(chunk)
            medians[i, j] = median
            means[i, j] = mean
            stds[i, j] = std

    median = np.median(data)

    if plots:
        if 'left' in flats_file:
            L = len(flats_file)
            name = flats_file[L-37:L-10]
        elif 'right' in flats_file:
            L = len(flats_file)
            name = flats_file[L-38:L-10]
        elif 'telescope' in flats_file:
            L = len(flats_file)
            i = flats_file.find('telescope')
            name = flats_file[i + 12:L-5]
        plt.ion
        
        # Create a grid for plotting
        x = np.arange(num_chunks_width + 1)
        y = np.arange(num_chunks_height + 1)
        x, y = np.meshgrid(x, y)
        
        # Create a 3D plot of the medians
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(121, projection='3d')
        sc1 = ax1.scatter(x, y, medians, c=medians, cmap='viridis', marker='o')
        fig.colorbar(sc1, ax=ax1, shrink=.3, aspect=10)
        ax1.view_init(elev=elev, azim=azim)
        ax1.set_title('3D Plot of Medians')
        ax1.set_xlabel('Chunk Index X')
        ax1.set_ylabel('Chunk Index Y')
        ax1.set_zlabel('Median Value')
        
        # Create a 3D plot of the means
        ax2 = fig.add_subplot(122, projection='3d')
        sc2 = ax2.scatter(x, y, means, c=means, cmap='viridis', marker='o')
        fig.colorbar(sc2, ax=ax2, shrink=.3, aspect=10)
        ax2.view_init(elev=elev, azim=azim)
        ax2.set_title('3D Plot of Means')
        ax2.set_xlabel('Chunk Index X')
        ax2.set_ylabel('Chunk Index Y')
        ax2.set_zlabel('Mean Value')
        
        # Save the plot as a PNG
        output_path = os.path.join(output_dir, f'{name}_3d_info.png')
        plt.savefig(output_path, format='png')
        plt.show()
        plt.close()
        print(f"3D plot saved as {output_path}")

    # Plot means and medians vs. standard deviations on the same plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot for means vs. standard deviations
    ax.scatter(means.flatten(), stds.flatten(), s=10, alpha=0.7, color='blue', label='Means')

    # Scatter plot for medians vs. standard deviations
    ax.scatter(medians.flatten(), stds.flatten(), s=10, alpha=0.7, color='red', label='Medians')

    # Adding title and labels
    ax.set_title('Poisson Noise Statistics: Means and Medians vs Standard Deviations')
    ax.set_xlabel('Value')
    ax.set_ylabel('Standard Deviation')
    ax.grid(True)

    # Adding a legend
    ax.legend()

    # Save the plot as a PNG
    output_path = os.path.join(output_dir, f'{name}_ms_vs_stds_info.png')
    plt.savefig(output_path, format='png')
    plt.close()
    print(f"Plot saved as {output_path}")


    
    return means, stds, median

def get_all_directories(root_folder):
    root = Path(root_folder)
    return [str(path) for path in root.rglob('*') if path.is_dir()]
def get_all_files(root_folder):
    root = Path(root_folder)
    return [str(path) for path in root.rglob('*') if path.is_file()]

def get_files_in_directory(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


def filefinder(filename_chunk):
    files = get_all_files(TRAINING_DIR) # + get_files_in_directory(OUTSIDE_DIR)
    # print(files[-1][-5:-1])
    matches = []
    for file in files:
        if filename_chunk in file and file[-5:-1]=='.fit':
            matches.append(file)
            if len(matches) > 10:
                print("too many matches, narrow it down")
                return 
    return matches



def filetrier(inpath, outpath = None):

    if not outpath:
        try:
            analyze_poisson_noise(inpath,plots=True)
        except FileNotFoundError:
            subdirs = get_all_directories(TRAINING_DIR) + [OUTSIDE_DIR]
            for directory in subdirs:
                try:
                    analyze_poisson_noise(f'{directory}/{inpath}',plots=True)
                    exit()
                except:
                    pass
            print("The file was not found under that filepath, its parent path or any recursive directories from it")
            inpath = input("please provide another filepath or chunk of filename: ")
            if len(inpath)>4:
                if inpath[-5:-1] == '.fit'  and not inpath==None:
                    analyze_poisson_noise(inpath,plots=True)
            if len(inpath)<5 or not inpath[-5:-1] == '.fit' :
                matches = filefinder(inpath)
                if matches == None:
                    return
                if not len(matches) == 1 and not len(matches) == 0:
                    yorn =input(f"there are {len(matches)} matches, would you like to pick one? (Y/N): ")
                    if yorn == 'y' or yorn =='yes' or yorn=='Y' or yorn=="Yes" or yorn =="YES":
                        for i, match in enumerate(matches):
                            print(f'{i}: {match}')
                        choice =input("which number match do you want to try?: ")
                        try:
                            choice=int(choice)
                            analyze_poisson_noise(matches[choice])
                        except:
                            exit()
                if len(matches) == 1:
                    analyze_poisson_noise(matches[0], plots=True)

                
                    

        except Exception as e:
            # This will catch all other exceptions
            print(f"An error occurred: {e}")
        return None
    else:
        try:
            analyze_poisson_noise(inpath,plots=True)
        except FileNotFoundError:
            subdirs = get_all_directories(TRAINING_DIR) + [OUTSIDE_DIR]
            for directory in subdirs:
                try:
                    analyze_poisson_noise(f'{directory}/{inpath}',plots=True, output_dir=outpath)
                    exit()
                except:
                    pass
            print("The file was not found under that filepath, its parent path or any recursive directories from it")
            inpath = input("please provide another filepath or chunk of filename: ")
            if len(inpath)>4:
                if inpath[-5:-1] == '.fit'  and not inpath==None:
                    analyze_poisson_noise(inpath,plots=True, output_dir=outpath)
            if len(inpath)<5 or not inpath[-5:-1] == '.fit' :
                matches = filefinder(inpath)
                if matches == None:
                    print('no matches')
                    return
                if not len(matches) == 1 and not len(matches) == 0:
                    yorn =input(f"there are {len(matches)} matches, would you like to pick one? (Y/N): ")
                    if yorn == 'y' or yorn =='yes' or yorn=='Y' or yorn=="Yes" or yorn =="YES":
                        for i, match in enumerate(matches):
                            print(f'{i}: {match}')
                        choice =input("which number match do you want to try?: ")
                        try:
                            choice=int(choice)
                            analyze_poisson_noise(inpath,plots=True, output_dir=outpath)
                        except:
                            exit()
                if len(matches) == 1:
                    analyze_poisson_noise(inpath,plots=True, output_dir=outpath)


if __name__ == "__main__":
    elev = 40
    azim = 40
    if len(sys.argv) ==2:
        inpath = sys.argv[1]
        filetrier(inpath)

    elif len(sys.argv) == 3:
        outpath = sys.argv[2]
        inpath = sys.argv[1]
        filetrier(inpath,outpath)
    else:
        # inpath =input('please provide filepath: ')
        inpath = '/home/borderbenja/training_data/funpacked_fits/telescope_g_UGC_5900_2024_03_15_03_07_56.fits'
        if not len(inpath)==0 and not inpath==None:
            filetrier(inpath)
        else:
            exit()





