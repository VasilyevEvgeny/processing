from numpy import zeros
from numba import jit
from numpy import pi, arctan2, meshgrid
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


@jit(nopython=True)
def calc_phase(arg):
    while arg >= 2 * pi:
        arg -= 2 * pi

    return arg


@jit(nopython=True)
def fast_initialization(phase, x, y, m, n):
    for i in range(n):
        for j in range(n):
            phase[i, j] = calc_phase(m * arctan2(y[i], x[j]) + m * pi)

    return phase


def plot_phase_3d(**params):
    m = params['m']
    n = params['n']
    language = params.get('language', '')

    r_0 = 100
    x_max, y_max = 5 * r_0, 5 * r_0
    x, y = zeros(n), zeros(n)
    for i in range(n):
        x[i], y[i] = i * x_max / n - x_max / 2, i * y_max / n - y_max / 2

    x_ticks, y_ticks = [-200, -100, 0, 100, 200], [-200, -100, 0, 100, 200]

    phase = zeros((n, n))
    phase = fast_initialization(phase, x, y, m, n)

    xx, yy = meshgrid(x, y)

    font_size = 40
    font_weight = 'bold'
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_subplot(111, projection='3d')
    if language == 'english':
        title = '$\mathbf{\\theta(x,y)}$, rad'
    else:
        title = '$\mathbf{\\theta(x,y)}$, рад'
    plt.title(title, fontsize=font_size, fontweight=font_weight)
    ax.plot_surface(xx, yy, phase, cmap='gray', rstride=1, cstride=1, linewidth=0, antialiased=False)

    offset_x = -(x_max / 2 + 0.05 * x_max)
    ax.contour(xx, yy, phase, levels=[-249], zdir='x', colors='black', linestyles='dashed', linewidths=5, offset=offset_x)
    ax.view_init(elev=75, azim=315)

    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_zticks([0, pi, 2 * pi])
    ax.set_zticklabels(['0', '$\pi$', '$2\pi$'])

    ax.zaxis.label.set_size(font_size)
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

    ax.set_zlim([0, 2 * pi + 1])
    ax.xaxis.set_tick_params(pad=15)
    ax.yaxis.set_tick_params(pad=15)
    ax.zaxis.set_tick_params(pad=15)

    plt.show()
    fig.savefig('phase(x,y)_ring_m=%d.png' % m, transparent=False, bbox_inches="tight")
    plt.close()