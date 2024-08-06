import os
import time as t
import sys

def rename_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Rename .fits files to .fz
    for file in files:
        if file.endswith('.fits'):
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, file.replace('.fits', '.fz'))
            os.rename(old_path, new_path)
        # Execute funpack command for each .fz file
            os.system(f'funpack {new_path}')

    # Grab new list of files since we just changed it
    files = os.listdir(folder_path)
    # Delete .fz files
    for file in files:
        if file.endswith('.fz'):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)

    # Rename files without extension to .fits
    for file in files:
        if '.' not in file :
            try:
                old_path = os.path.join(folder_path, file)
                new_path = os.path.join(folder_path, file + '.fits')
                os.rename(old_path, new_path)
            except:
                None
    
def move_files(folder_path, outpath):    
    files = os.listdir(folder_path)
    for file in files:
        os.rename(os.path.join(folder_path, file),os.path.join(outpath,file) )
    

if __name__ == "__main__":
    if len(sys.argv) ==2:
        folder_path = sys.argv[1]
        rename_files(folder_path)
        # rename_files(folder_path)
        t.sleep(3)
        # rename_files(folder_path)
    elif len(sys.argv) == 3:
        folder_path = sys.argv[1]
        outpath = sys.argv[2]
        rename_files(folder_path)
        move_files(folder_path, outpath)
    else:
        folder_path =input('please provide folder path:')
        rename_files(folder_path)
        # rename_files(folder_path)
        # t.sleep(3)
        # rename_files(folder_path)