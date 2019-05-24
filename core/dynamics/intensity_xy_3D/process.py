from core.functions import get_files, filter_files, a_to_i, find_t_slice_with_maximum
from .plot import plot_intensity_xy_3d
from tqdm import tqdm
from numpy import loadtxt


def process_dynamics_intensity_xy_3d(**params):
    path = params['path']
    res_path = params['res_path']
    r_max = params['r_max']
    r_right = params['r_right']
    x_ticks = params['x_ticks']
    y_ticks = params['y_ticks']
    language = params.get('language', '')

    files = filter_files(get_files(path), every=1)
    for idx, file in enumerate(tqdm(files)):
        arr = a_to_i(loadtxt(file, skiprows=1))
        t_slice = find_t_slice_with_maximum(arr)
        plot_intensity_xy_3d(t_slice, r_max * 10**6, r_right * 10**6, res_path, idx,
                             x_ticks=x_ticks,
                             y_ticks=y_ticks,
                             language=language)
