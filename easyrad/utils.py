import os
from glob import glob

BASE_DIR = os.environ.get('EASYRAD_DIR', '.')
_rel_glob = lambda x: sorted(glob(os.path.join(BASE_DIR, x)))
