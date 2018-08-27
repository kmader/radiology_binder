from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import pydicom
import numpy as np

from IPython.display import display, HTML

def find_files(path=None):
  if (path is None) or not isinstance(path, str): 
    raise ValueError('Please enter a path to search, a good start is *.*')
  if len(path)==0:
    path='*'
  if not '*' in path:
    path = '*{}*'.format(path)
  file_df = pd.DataFrame({'file_path': glob(path)})
  return file_df

def load_dicom(in_path):
  return pydicom.read_file(in_path)

def show_dicom(in_file):
  if isinstance(in_path, str): 
    raise ValueError('Please load the dicom first')
  plt.imshow(in_file.pixel_array)
  

def show_workspace(in_vars):
    var_list = pd.DataFrame([{'variable': v, 'variable name': k} for k,v in  in_vars.items()])
    var_list['type'] = var_list['variable'].map(type)
    var_list['shape'] = var_list['variable'].map(lambda x: x.shape if isinstance(x, np.ndarray) else '')
    var_list['preview'] = var_list['variable'].map(lambda x: repr(x)[:80])
    var_list.drop('variable', inplace=True, axis=1)
    clean_var_list = var_list[~var_list['variable name'].str.startswith('_')]
    # remove imports
    clean_var_list = clean_var_list[clean_var_list['type']!=type(pd)]
    display(clean_var_list)
