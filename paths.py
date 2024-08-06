from pathlib import Path
import os



TRAINING_DIR = Path(__file__).parent.absolute()
OUTSIDE_DIR = TRAINING_DIR.parent.absolute()
FUNPACKED_FITS = TRAINING_DIR.joinpath('funpacked_fits')
INJECTED_FITS = TRAINING_DIR.joinpath('injected_fits')
CAT_DIR = FUNPACKED_FITS.joinpath('catalogs')

if not os.path.exists(CAT_DIR):
    os.mkdir(CAT_DIR)
if not os.path.exists(INJECTED_FITS):
    os.mkdir(INJECTED_FITS)


