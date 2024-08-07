from fim_scripts.image_analysis import analyze_poisson_noise
import argparse
import configparser
from fim_scripts.paths import *
from fim_scripts.filefinder import filetrier, filefinder, get_all_files, get_all_directories, get_files_in_directory

def main():

    # parses arguments 
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-v', dest='view', nargs=2, type=int, help="specifies viewing angle(in alt/az)")
    parser.add_argument('-ortho', action='store_true', help='triggers orgthographic projection in plotting')
    parser.add_argument('-o','-outpath', dest='outpath', help='Specific outpath')
    parser.add_argument('-chunks', action='store_true', help='enables chunked averaging')
    parser.add_argument('infile', nargs='?', type=str, help="Input file")

    # assigns arguments to variables
    args = parser.parse_args()
    outpath = args.outpath
    inpath = args.infile
    chunks = args.chunks
    ortho = args.ortho
    elev = args.view[0]
    azim = args.view[1]
    


    default = configparser.ConfigParser()
    if not inpath:
        default.read(f'{FIM_SCRIPTS_DIR}/default.cfg')
        inpath = default['DEFAULT']['inpath']
    if not args.view:
        default.read(f'{FIM_SCRIPTS_DIR}/default.cfg')
        elev = int(default['DEFAULT']['elev'])
        azim = int(default['DEFAULT']['azim'])
    
    


    # inpath =input('please provide filepath: ')

    if not outpath:
        filetrier(inpath, elev, azim, chunks, ortho)
    else:
        filetrier(inpath, elev, azim, outpath, chunks, ortho)

if __name__ == "__main__":
    main()