# Import necessary libraries
from astropy.io import fits
import numpy as np
import time 

def getcenter(file_path, group_rank=1):
    start_time = time.time()  # Record start time
    hdulist = fits.open(file_path)
    image_data = hdulist[0].data
    hdulist.close()

    # Step 2: Extract the image data (assuming it's a 2D array)
    data = image_data

    # Step 3: Find the coordinates of the brightest pixel(s)
    max_value = np.max(data)
    brightest_coords = np.argwhere(data == max_value)

    # Step 4: Identify groups of touching brightest pixels
    binary_image = (data == max_value).astype(int)

    # Label connected components manually
    def label_connected_components(binary_image):
        labeled_array = np.zeros_like(binary_image)
        label_count = 1
        for y in range(binary_image.shape[0]):
            for x in range(binary_image.shape[1]):
                if binary_image[y, x] == 1 and labeled_array[y, x] == 0:
                    stack = [(y, x)]
                    while stack:
                        vy, vx = stack.pop()
                        if (0 <= vy < binary_image.shape[0]) and (0 <= vx < binary_image.shape[1]) and binary_image[vy, vx] == 1 and labeled_array[vy, vx] == 0:
                            labeled_array[vy, vx] = label_count
                            stack.extend([(vy+1, vx), (vy-1, vx), (vy, vx+1), (vy, vx-1)])
                    label_count += 1
        return labeled_array, label_count - 1

    labeled_array, num_features = label_connected_components(binary_image)
    if num_features<group_rank:
        group_rank=num_features
    # Step 5: Determine the group based on rank
    bin_counts = np.bincount(labeled_array.flat)[1:]  # Exclude background label
    bin_counts_sorted = np.sort(bin_counts)[::-1]  # Sort in descending order
    if group_rank <= len(bin_counts_sorted):
        group_label = np.where(bin_counts == bin_counts_sorted[group_rank - 1])[0][0] + 1
    else:
        print(f"Group rank {group_rank} exceeds the number of groups.")
        return None

    # Step 6: Compute the center of the selected group
    if group_label > 0:
        group_coords = np.argwhere(labeled_array == group_label)
        center = np.mean(group_coords, axis=0)
    else:
        center = None

    x = center[1]
    y = center[0]
    print(f"Center of group {group_rank}: {x, y}")
    end_time = time.time()  # Record end time
    print(f"Execution time: {end_time - start_time} seconds")
    return x, y

 # Get center of the second largest group
