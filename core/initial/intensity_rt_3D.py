from numpy import zeros
from numpy import sqrt, exp, meshgrid
from numba import jit
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


@jit(nopython=True)
def fast_initialization(M, r, t, n, r_0, t_0):
    intensity = zeros((n, n))
    for i in range(n):
        for j in range(n):
            intensity[i, j] = (r[j] / r_0) ** (2 * M) * exp(-(r[j] / r_0) ** 2) * exp(-(t[i] / t_0) ** 2)

    return intensity


def plot_intensity_rt_3d_initial(**params):
    M = params['M']
    n = params['n']
    r_0 = params['r_0']
    t_0 = params['t_0']
    r_ticks = params['r_ticks']
    t_ticks = params['t_ticks']
    z_ticks = params['z_ticks']
    z_lim = params['z_lim']
    language = params.get('language', '')
    cmap = params.get('cmap', 'jet')
    dpi = params.get('dpi', None)

    r_max, t_max = sqrt(M) * 5 * r_0, sqrt(M) * 5 * t_0
    r, t = zeros(n), zeros(n)
    for i in range(n):
        r[i], t[i] = i * r_max / n - r_max / 2, i * t_max / n - t_max / 2

    intensity = fast_initialization(M, r, t, n, r_0, t_0)

    rr, tt = meshgrid(r, t)

    font_size = 40
    font_weight = 'bold'
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_subplot(111, projection='3d')

    plt.title('$\mathbf{I / I_0 (r,t)}$', fontsize=font_size, fontweight=font_weight)

    ax.plot_surface(rr, tt, intensity, cmap=cmap, rstride=1, cstride=1, antialiased=False)
    ax.view_init(elev=75, azim=315)

    offset_x = -(r_max / 2 + 0.05 * r_max)
    offset_y = t_max / 2 + 0.05 * t_max
    ax.contour(rr, tt, intensity, levels=[-sqrt(M) * r_0], zdir='x', colors='black', linestyles='dashed', linewidths=5, offset=offset_x)
    ax.contour(rr, tt, intensity, levels=[0], zdir='y', colors='black', linestyles='dashed', linewidths=5, offset=offset_y)

    ax.set_xticks(r_ticks)
    ax.set_yticks(t_ticks)
    ax.set_zticks(z_ticks)
    ax.tick_params(labelsize=font_size - 5)
    plt.tight_layout()

    if language == 'english':
        xlabel = '\n\n\nr, $\mathbf{\mu}$m'
        ylabel = '\n\n\nt, fs'
    else:
        xlabel = '\n\n\nr, мкм'
        ylabel = '\n\n\nt, фс'

    plt.xlabel(xlabel, fontsize=font_size, fontweight=font_weight)
    plt.ylabel(ylabel, fontsize=font_size, fontweight=font_weight)

    ax.zaxis.label.set_rotation(56)
    ax.zaxis.label.set_size(font_size)
    ax.set_zlim(z_lim)
    ax.xaxis.set_tick_params(pad=15)
    ax.yaxis.set_tick_params(pad=15)
    ax.zaxis.set_tick_params(pad=15)

    if dpi is None:
        fig.savefig('i(r,t)_M=%d.png' % M, transparent=False, bbox_inches='tight')
    else:
        fig.savefig('i(r,t)_M=%d.png' % M, transparent=False, bbox_inches='tight',
                    dpi=dpi)

    plt.show()
    plt.close()
