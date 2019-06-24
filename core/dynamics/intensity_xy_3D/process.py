from core.functions import get_files, filter_files, a_to_i, find_r_slice_with_maximum
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
    cmap = params.get('cmap', 'jet')
    dpi = params.get('dpi', None)

    files = filter_files(get_files(path), every=1)
    for idx, file in enumerate(tqdm(files)):
        arr = a_to_i(loadtxt(file, skiprows=1))
        r_slice = find_r_slice_with_maximum(arr)
        plot_intensity_xy_3d(r_slice, r_max * 10**6, r_right * 10**6, res_path, idx,
                             x_ticks=x_ticks,
                             y_ticks=y_ticks,
                             language=language,
                             cmap=cmap,
                             dpi=dpi)
