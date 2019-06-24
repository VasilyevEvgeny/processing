import pandas as pd


def xlsx_to_df(path_to_xlsx, normalize_z_to=10**2, normalize_i_to=10**17):
    df = pd.read_excel(path_to_xlsx)

    df['z, m'] *= normalize_z_to
    df['dz, m'] *= normalize_z_to
    df['i_max, W / m^2'] /= normalize_i_to

    df = df.rename(index=str, columns={'z, m': 'z_normalized', 'dz, m': 'dz_normalized', 'i_max, W / m^2': 'i_max_normalized'})

    return df


def txt_to_df(path_to_txt, normalize_z_to=10**2, normalize_i_to=10**17, normalize_ne_rel_to=10**-3):
    df = pd.read_csv(path_to_txt, sep='\t')

    df['z[m]'] *= normalize_z_to
    df['dz[m]'] *= normalize_z_to
    df['I_max[W/m^2]'] /= normalize_i_to
    df['Ne_max/N0'] /= normalize_ne_rel_to

    df = df.rename(index=str,
                   columns={'z[m]': 'z_normalized', 'dz[m]': 'dz_normalized', 'I_max[W/m^2]': 'i_max_normalized',
                            'Ne_max/N0': 'ne_rel_normalized'})

    return df
