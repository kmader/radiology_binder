import doctest
import sys
sys.path.append('..')
import easyrad
from easyrad import io

def test_io():
    doctest.testmod(io)