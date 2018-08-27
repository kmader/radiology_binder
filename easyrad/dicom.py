"""
Commands for making opening one or more dicoms very easy
"""
from collections import namedtuple
import pydicom
import pandas as pd
from .browsing import _rel_glob

type_info = namedtuple('type_info',
                       ['inferrable', 'realtype', 'has_nulltype', 'length',
                        'is_complex'])


def _remove_empty_columns(in_df):
    empty_cols = dict(filter(lambda kv: kv[1] > 0,
                             in_df.apply(_countmissingvalues,
                                         axis=0).to_dict().items()))
    # remove missing columns
    return in_df[
        [ccol for ccol in in_df.columns if empty_cols.get(ccol, 0) == 0]]


def safe_type_infer(x):
    return type_info(True, type(x), has_nulltype=False,
                     length=_tlen(x), is_complex=False)


def _identify_column_types(in_df_dict):
    return dict([(k, safe_type_infer(v)) for (k, v) in in_df_dict.items()])


def _dicoms_to_dict(dicom_list):
    fvr = lambda x: None if x.first_valid_index() is None else x[
        x.first_valid_index()]

    out_list = []

    for in_dicom in dicom_list:
        temp_dict = {a.name: a.value for a in in_dicom.iterall()}
        if in_dicom.__dict__.get('_pixel_array', None) is not None:
            temp_dict['Pixel Array'] = in_dicom.pixel_array.tolist()

        out_list += [temp_dict]
    df_dicom = pd.DataFrame(out_list)  # just for the type conversion
    fvi_series = df_dicom.apply(_findvalidvalues, axis=0).to_dict()
    valid_keys = _identify_column_types(fvi_series)
    do_keep = lambda key, ti: ti.inferrable & (
        not ti.has_nulltype)  # & (not ti.is_complex) & (ti.length>0)
    fvalid_keys = dict(
        [(k, do_keep(k, t_info)) for k, t_info in valid_keys.items()])
    good_columns = list(
        map(lambda x: x[0], filter(lambda x: x[1], fvalid_keys.items())))
    bad_columns = list(
        map(lambda x: x[0], filter(lambda x: not x[1], fvalid_keys.items())))
    sql_df = df_dicom[good_columns]
    return sql_df.dropna(axis=1)


def _apply_conv_dict(in_ele):
    _dicom_conv_dict = {}
    cnv_fcn = _dicom_conv_dict.get(type(in_ele[0]), None)
    if cnv_fcn is not None:
        return in_ele.map(cnv_fcn)
    else:
        return in_ele


def _conv_df(in_df):
    return in_df.apply(_apply_conv_dict)


def _dicom_paths_to_df(in_path_list):
    f_df = _dicoms_to_dict(
        [pydicom.read_file(in_path, stop_before_pixels=True) for in_path in
         in_path_list])
    f_df['file path'] = in_path_list
    rec_df = _remove_empty_columns(f_df)
    conv_df = _conv_df(rec_df)
    return conv_df


def _tnonempty(x):
    return _tlen(x) > 0


def _findvalidvalues(crow):
    nz_vals = list(filter(_tnonempty, crow))
    return None if len(nz_vals) < 1 else nz_vals[0]


def _countmissingvalues(crow):
    nz_vals = list(filter(lambda i: not _tnonempty(i), crow))
    return len(nz_vals)


def _tlen(x):
    # type: (Any) -> int
    """
    Try to calculate the length, otherwise return 1
    Examples:
    >>> _tlen([1,2,3])
    3
    >>> _tlen("Hi")
    2
    >>> _tlen(0)
    1
    >>> _tlen(np.NAN)
    0
    """
    try:
        return len(x)
    except:
        try:
            if np.isnan(x): return 0
        except:
            pass
        return 1

def load_dicom(in_path, load_images=True):
    """
    A function to load a dicom, list of dicoms, or data frame of dicoms
    >>> load_dicom('test_ct.dcm').shape
    (1, 188)
    >>> load_dicom('*dcm').shape
    (2, 71)
    """

    if isinstance(in_path, pd.DataFrame):
        if 'path' in in_path:
            files_to_load = in_path['path'].values.tolist()
        elif 'name' in in_path:
            files_to_load = [os.path.join(BASE_DIR, x) for x in in_path['name']]
        else:
            raise ValueError(
                'load_dicom expects a dataframe like the one created by find_files (it should have a column called name)')
    else:
        if isinstance(in_path, str):
            files_to_load = _rel_glob(in_path)
        if isinstance(in_path, list):
            files_to_load = [_rel_glob(x) for x in in_path]
        files_to_load = [x for x in files_to_load]

    out_df = _dicom_paths_to_df(files_to_load)
    if load_images:
        out_df['image'] = out_df['image']