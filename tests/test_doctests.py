import doctest
import sys
import types

from easyrad import browsing

if __name__=="__main__":
    import easyrad
    doctest.testmod(easyrad, verbose=True, report=True)
    for c_name in dir(easyrad):
        c_obj = getattr(easyrad, c_name)
        if isinstance(c_obj, types.ModuleType):
            print('Checking', 'easyrad.{}'.format(c_name))
            doctest.testmod(c_obj, verbose=True, report=True)
