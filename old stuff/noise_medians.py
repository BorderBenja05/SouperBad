import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def analyze_poisson_noise(flats_file,chunk_size=15, plots = False, output_dir='plots'):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    
    # Load the FITS image
    with fits.open(flats_file) as hdul:
        data = hdul[0].data
    
    # Get image dimensions
    img_height, img_width = data.shape
    # print(f"Image dimensions: {img_height}x{img_width}")
    
    # Calculate the number of chunks
    num_chunks_height = img_height // chunk_size
    num_chunks_width = img_width // chunk_size
    
    medians = np.zeros((num_chunks_height, num_chunks_width))
    means = np.zeros((num_chunks_height, num_chunks_width))
    stds = np.zeros((num_chunks_height, num_chunks_width))
    
    # Iterate over the image in chunks of size chunk_size x chunk_size
    for i in range(num_chunks_height):
        for j in range(num_chunks_width):
            start_i = i * chunk_size
            start_j = j * chunk_size
            chunk = data[start_i:start_i + chunk_size, start_j:start_j + chunk_size]
            median = np.median(chunk)
            std = np.std(chunk)
            medians[i, j] = median
            stds[i, j] = std
            # print(f"Processed chunk ({start_i}:{start_i + chunk_size}, {start_j}:{start_j + chunk_size}) - mean: {mean}, std: {std}")
    

    
    median = np.median(medians)
    
    # print(f"medians array shape: {medians.shape}")
    # print(f"Number of stds: {len(stds)}")
    if plots ==True:
        if 'left' in flats_file:
            L = len(flats_file)
            name = flats_file[L-37:L-10]
        elif 'right' in flats_file:
            L = len(flats_file)
            name = flats_file[L-38:L-10]
        elif 'telescope' in flats_file:
            L = len(flats_file)
            i = flats_file.find('telescope')
            name = flats_file[i + 12:L-14]            
        # Create a grid for plotting
        x = np.arange(num_chunks_width)
        y = np.arange(num_chunks_height)
        x, y = np.meshgrid(x, y)
        z = medians
        plt.ion
        # Create a 3D plot of the medians
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        plt.colorbar()  
        ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')
        # plt.imshow(data, cmap='viridis', vmin=10, vmax=1900)
        # plt.colorbar()  
        ax.view_init(elev=0,azim=90)
        ax.set_title('3D Plot of Medians')
        ax.set_xlabel('Chunk Index X')
        ax.set_ylabel('Chunk Index Y')
        ax.set_zlabel('Median Value')
        # ax.set_proj_type('ortho')
        # z_min = 1350
        # z_max = 
        # ax.set_zlim(z_min, z_max)

        
        # Save the plot as a PDF
        output_path = os.path.join(output_dir, f'{name}_3d_plot_medians.png')
        # plt.savefig(output_path, format='png')
        plt.show()
        plt.close()
        print(f"3D plot saved as {output_path}")

        # Plot medians vs. standard deviations
        plt.figure(figsize=(10, 6))
        plt.scatter(medians.flatten(), stds.flatten(), s=10, alpha=0.7, color='blue')
        plt.title('Poisson Noise Statistics: Medians vs Standard Deviations')
        plt.xlabel('Median')
        plt.ylabel('Standard Deviation')
        plt.grid(True)
        
        # Save the plot as a PDF
        output_path = os.path.join(output_dir, f'{name}_noise_medians.png')
        plt.savefig(output_path, format='png')
        plt.close()
        print(f"Plot saved as {output_path}")
    
    return medians, stds, median

# # Example usage
# flats_file = '/mnt/14tb_turbo_disk/transfer_data/2024_04_12/telescope_r_UGC_5900_2024_04_13_02_47_40.fits'
# medians, stds, median = analyze_poisson_noise(flats_file, plots=True)
# print(np.median(stds), median,median/np.median(stds))
# print(np.std(stds))

# flats_file = '/home/borderbenja/training_data/funpacked_fits/telescope_g_S240413p_5954_2024_04_14_23_26_43.fits'
# medians, stds, median = analyze_poisson_noise(flats_file, plots=True)
# print(np.median(stds), median,median/np.median(stds))
# print(np.std(stds))

# flats_file = '/home/borderbenja/training_data/funpacked_fits/telescope_g_UGC_4132_2024_04_13_00_02_24.fits'
# medians, stds, median = analyze_poisson_noise(flats_file, plots=True)
# print(np.median(stds), median,median/np.median(stds))
# print(np.std(stds))

# flats_file = '/home/borderbenja/training_data/funpacked_fits/telescope_r_ArturusA_2024_04_12_23_22_07.fits'
# medians, stds, median = analyze_poisson_noise(flats_file, plots=True)
# print(np.median(stds), median,median/np.median(stds))
# print(np.std(stds))

# flats_file = '/home/borderbenja/training_data/funpacked_fits/telescope_r_S240413p_6504_2024_04_14_22_10_16.fits'
# medians, stds, median = analyze_poisson_noise(flats_file, plots=True)
# print(np.median(stds), median,median/np.median(stds))
# print(np.std(stds))