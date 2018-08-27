import os, sys
os.environ['EASYRAD_DIR'] = os.path.join(os.path.expandvars('$HOME'), 'dicoms')
sys.path.append(os.path.expandvars('$HOME'))
from easyrad import *
