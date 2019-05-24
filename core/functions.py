from glob import glob
from numba import jit
from numpy import max as maximum
from numpy import zeros, sqrt, log10, inf, float64, where
import os
import shutil
from time import sleep


def get_files(path, dir_name='pictures'):
    files = []
    for file in glob(path + '/*', recursive=True):
        if file.split('\\')[1] != dir_name:
            files.append(file)

    return files


def filter_files(files, every=6):
    files_new = []
    for i in range(len(files)):
        if not i % every:
            files_new.append(files[i])

    return files_new


@jit(nopython=True)
def a_to_i(arr):
    n_rows, n_cols = arr.shape[0], arr.shape[1]
    arr_i = zeros((n_rows, n_cols//2))
    for k in range(n_rows):
        idx = 0
        for s in range(0, n_cols, 2):
            arr_i[k, idx] = arr[k, s]**2 + arr[k, s+1]**2
            idx += 1
    return arr_i


@jit(nopython=True)
def find_t_slice_with_maximum(arr):
    max_val = maximum(arr)
    s_max = where(arr == max_val)[1][0]

    return arr[:, s_max]


@jit(nopython=True)
def linear_approximation_real(x, x1, y1, x2, y2):
    return (y1 - y2) / (x1 - x2) * x + (y2 * x1 - x2 * y1) / (x1 - x2)


@jit(nopython=True)
def r_to_xy(r_slice):
    n_r = len(r_slice)
    n_x, n_y = 2 * n_r, 2 * n_r
    arr = zeros(shape=(n_x, n_y))
    for i in range(n_x):
        for j in range(n_y):
            r = sqrt((i - n_x / 2.) ** 2 + (j - n_y / 2.) ** 2)
            if int(r) < n_r - 1:
                arr[i, j] = linear_approximation_real(r, int(r), r_slice[int(r)], int(r) + 1, r_slice[int(r) + 1])

    return arr


def filter_and_log_arr(arr, min_val=0.1):
    arr[where(arr < min_val)] = min_val
    return log10(arr)


def crop_rs(rs, r_right):
    idx = len(rs) - 1
    for i in range(len(rs)):
        if rs[i] > r_right:
            idx = i
            break
    return rs[:idx], idx


def create_dir(**kwargs):
    path = kwargs['path']
    dir_name = kwargs.get('dir_name', 'images')

    res_path = path + '/' + dir_name

    try:
        os.makedirs(res_path)
    except OSError:
        shutil.rmtree(res_path)
        sleep(1)
        os.makedirs(res_path)

    return res_path
