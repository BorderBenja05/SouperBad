from fim_scripts.image_analysis import analyze_poisson_noise
import argparse
import configparser
from fim_scripts.paths import *
from fim_scripts.filefinder import filetrier, filefinder, get_all_files, get_all_directories, get_files_in_directory

def main():

    # parses arguments 
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-ortho', action='store_true')
    parser.add_argument('-o','-outpath', dest='outpath', type=str)
    parser.add_argument('-f', dest='infile', type=str)
    parser.add_argument('-chunks', action='store_true')

    # assigns arguments to variables
    args = parser.parse_args()
    outpath = args.outpath
    inpath = args.infile
    chunks = args.chunks
    ortho = args.ortho

    if not inpath:
        default = configparser.ConfigParser()
        default.read(f'{FUTILITY_DIR}/default.cfg')
        inpath = default['DEFAULT']['inpath']
    
    


    # inpath =input('please provide filepath: ')

    if not outpath:
        filetrier(inpath, chunks, ortho)
    else:
        filetrier(inpath, outpath, chunks, ortho)

if __name__ == "__main__":
    main()