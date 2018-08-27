"""Basic tools for browsing files, reading images and loading dicom data without too much understanding for python"""
import inspect
import os

import numpy as np
import pandas as pd
import pydicom
from IPython.display import display
from skimage.io import imread

from .utils import BASE_DIR, _rel_glob

_dicom_as_np = lambda x: pydicom.read_file(x).pixel_array
_img_as_np = lambda x: imread(x)


def show_workspace(in_vars=None, show_df=False):
    """
    Show the current workspace as a pandas dataframe
    :param in_vars:
    :return:
    >>> var_df = show_workspace()
    >>> var_df.columns.tolist()
    ['variable name', 'type', 'shape', 'preview']
    >>> var_df[var_df['variable name']=='bob'].shape[0]
    0
    >>> bob=5
    >>> var_df = show_workspace()
    >>> print(var_df[var_df['variable name']=='bob'].to_string(index=False))
    variable name           type shape preview
             bob  <class 'int'>             5
    """
    if in_vars is None:
        frame = inspect.currentframe()
        try:
            in_vars = frame.f_back.f_locals
        finally:
            del frame

    var_list = pd.DataFrame(
        [{'variable': v, 'variable name': k} for k, v in in_vars.items()])
    var_list['type'] = var_list['variable'].map(type)
    var_list['shape'] = var_list['variable'].map(
        lambda x: x.shape if isinstance(x, np.ndarray) else '')
    var_list['preview'] = var_list['variable'].map(lambda x: repr(x)[:80])
    var_list.drop('variable', inplace=True, axis=1)
    clean_var_list = var_list[~var_list['variable name'].str.startswith('_')]
    # remove imports
    clean_var_list = clean_var_list[clean_var_list['type'] != type(pd)]
    if show_df:
        display(clean_var_list)
    else:
        return clean_var_list


def file_type(in_path):
    _, ext = os.path.splitext(in_path.lower())
    if ext == '.dcm':
        return 'DICOM Image', _dicom_as_np
    if ext in ['.png', '.jpg', '.gif', '.tif']:
        return 'Image', _img_as_np
    else:
        return ext[1:].upper(), None


def find_files(path=None):
    """
    Show the currently available data files
    >>> find_files('').shape
    (2, 4)
    >>> find_files('dcm')['name'].values.tolist()
    ['test_ct.dcm', 'test_lung_ct.dcm']
    >>> find_files('*').columns.tolist()
    ['folder', 'name', 'file type', 'file size']
    """
    if (path is None) or not isinstance(path, str):
        raise ValueError('Please enter a path to search, a good start is *.*')
    if len(path) == 0:
        path = '*'
    if not '*' in path:
        path = '*{}*'.format(path)

    file_df = pd.DataFrame({'path': _rel_glob(path)})
    file_df['folder'] = file_df['path'].map(
        lambda x: os.path.basename(os.path.dirname(x)))
    file_df['name'] = file_df['path'].map(
        lambda path: os.path.relpath(path, BASE_DIR))

    file_df['_typeparser'] = file_df['path'].map(file_type)
    file_df['file type'] = file_df['_typeparser'].map(lambda x: x[0])

    file_df['file size'] = file_df['path'].map(lambda x: '%04.2f kb' %
                                                         (os.stat(
                                                             x).st_size / 1024))

    return file_df.drop(['path', '_typeparser'], axis=1)
