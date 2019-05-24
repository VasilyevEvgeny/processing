from numpy import zeros
from numpy import sqrt, exp, meshgrid
from numba import jit
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


@jit(nopython=True)
def fast_initialization(M, x, y, n, r_0):
    intensity = zeros((n, n))
    for i in range(n):
        for j in range(n):
            r = sqrt(x[j] ** 2 + y[i] ** 2)
            intensity[i, j] = (r / r_0) ** (2 * M) * exp(-(r / r_0) ** 2)

    return intensity


def plot_intensity_xy_3d_initial(**params):
    M = params['M']
    n = params['n']
    r_0 = params['r_0']
    x_ticks = params['x_ticks']
    y_ticks = params['y_ticks']
    z_ticks = params['z_ticks']
    z_lim = params['z_lim']
    language = params.get('language', '')

    x_max, y_max = sqrt(M) * 5 * r_0, sqrt(M) * 5 * r_0
    x, y = zeros(n), zeros(n)
    for i in range(n):
        x[i], y[i] = i * x_max / n - x_max / 2, i * y_max / n - y_max / 2

    intensity = fast_initialization(M, x, y, n, r_0)

    xx, yy = meshgrid(x, y)

    font_size = 40
    font_weight = 'bold'
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_subplot(111, projection='3d')

    plt.title('$\mathbf{I / I_0 (x,y)}$', fontsize=font_size, fontweight=font_weight)

    ax.plot_surface(xx, yy, intensity, cmap='jet', rstride=1, cstride=1, antialiased=False)
    ax.view_init(elev=75, azim=315)

    offset_x = -(x_max / 2 + 0.05 * x_max)
    offset_y = y_max / 2 + 0.05 * y_max
    ax.contour(xx, yy, intensity, 0, zdir='x', colors='black', linestyles='dashed', linewidths=5, offset=offset_x)
    ax.contour(xx, yy, intensity, 0, zdir='y', colors='black', linestyles='dashed', linewidths=5, offset=offset_y)

    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_zticks(z_ticks)
    ax.tick_params(labelsize=font_size - 5)
    plt.tight_layout()
    if language == 'english':
        xlabel = '\n\n\nx, $\mathbf{\mu}$m'
        ylabel = '\n\n\ny, $\mathbf{\mu}$m'
    else:
        xlabel = '\n\n\nx, мкм'
        ylabel = '\n\n\ny, мкм'
    plt.xlabel(xlabel, fontsize=font_size, fontweight=font_weight)
    plt.ylabel(ylabel, fontsize=font_size, fontweight=font_weight)

    ax.zaxis.label.set_rotation(56)
    ax.zaxis.label.set_size(font_size)
    ax.set_zlim(z_lim)
    ax.xaxis.set_tick_params(pad=15)
    ax.yaxis.set_tick_params(pad=15)
    ax.zaxis.set_tick_params(pad=15)

    fig.savefig('i(x,y)_M=%d.png' % M, transparent=False, bbox_inches='tight')

    plt.show()
    plt.close()
