from tqdm import tqdm
from numpy import loadtxt

from core.functions import get_files, filter_files, a_to_i, find_r_slice_with_maximum
from .plot import plot_profiles_r


def process_dynamics_profiles_r(**params):
    path = params['path']
    res_path = params['res_path']
    rlim = params['rlim']
    language = params.get('language', '')

    files = filter_files(get_files(path), every=1)
    data = []
    for idx, file in enumerate(tqdm(files)):
        arr = a_to_i(loadtxt(file, skiprows=1))
        r_slice = find_r_slice_with_maximum(arr)
        lmbda = float((file.split('/')[-1]).split('_')[0])
        r_max = float((file.split('/')[-1]).split('_')[1])
        i_0 = float((file.split('/')[-1]).split('_')[2])
        data.append({'lmbda': lmbda,
                     'r_max': r_max,
                     'i_0': i_0,
                     'r_slice': r_slice})

    plot_profiles_r(data, res_path,
                    rlim=rlim,
                    language=language)
