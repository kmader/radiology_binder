from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
import pydicom

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
