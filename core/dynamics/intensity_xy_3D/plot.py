from numpy import append, meshgrid
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

from core.functions import r_to_xy, filter_and_log_arr, crop_rs


def plot_intensity_xy_3d(r_slice, r_max, r_right, res_path, idx, **params):
    x_ticks = params['x_ticks']
    y_ticks = params['y_ticks']
    language = params['language']
    cmap = params.get('cmap', 'jet')
    dpi = params.get('dpi', None)

    n_r = len(r_slice)
    h_r = r_max / n_r
    rs = [i * h_r for i in range(n_r)]
    rs_cropped, r_right_idx = crop_rs(rs, r_right)
    rs_reflected = append([-e for e in rs_cropped[::-1]], rs_cropped)

    arr = r_to_xy(r_slice[:r_right_idx])
    arr = filter_and_log_arr(arr)

    xx, yy = meshgrid(rs_reflected, rs_reflected)

    font_size = 40
    font_weight = 'bold'
    fig = plt.figure(figsize=(13, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.w_xaxis.set_pane_color(mcolors.to_rgba('white'))
    ax.w_yaxis.set_pane_color(mcolors.to_rgba('white'))
    ax.w_zaxis.set_pane_color(mcolors.to_rgba('white'))
    levels_plot = [-1. + i * 0.025 for i in range(130)]
    ax.plot_surface(xx, yy, arr, cmap=cmap, rstride=1, cstride=1, antialiased=False,
                    vmin=levels_plot[0], vmax=levels_plot[-1])

    offset_x = -(r_max / 2 - 0.025 * r_max)
    offset_y = (r_max / 2 - 0.025 * r_max)
    ax.contour(xx, yy, arr, 1, zdir='x', colors='black', linestyles='solid', linewidths=3, offset=offset_x, levels=0)
    ax.contour(xx, yy, arr, 1, zdir='y', colors='black', linestyles='solid', linewidths=3, offset=offset_y, levels=0)

    ax.view_init(elev=50, azim=345)
    ax.set_zlim([levels_plot[0], levels_plot[-1]])

    plt.xticks(x_ticks, fontsize=font_size - 5)
    plt.yticks(y_ticks, fontsize=font_size - 5)

    if language == 'english':
        xlabel = '\n\n\nx, $\mathbf{\mu}$m'
        ylabel = '\n\n\ny, $\mathbf{\mu}$m'
    else:
        xlabel = '\n\n\nx, мкм'
        ylabel = '\n\n\ny, мкм'
    plt.xlabel(xlabel, fontsize=font_size, fontweight=font_weight)
    plt.ylabel(ylabel, fontsize=font_size, fontweight=font_weight)

    zticks = [-1.0, 0.0, 1.0, 2.0]
    ax.set_zticks(zticks)

    plt.title("   lg I/I$\mathbf{_0}$(x, y)", fontsize=font_size, fontweight=font_weight)

    ax.tick_params(labelsize=font_size - 5)
    ax.xaxis.set_tick_params(pad=20)
    ax.yaxis.set_tick_params(pad=20)
    ax.zaxis.set_tick_params(pad=20)

    plt.tight_layout(rect=[-0.1, 0.1, 1.05, 1])

    if dpi is None:
        plt.savefig(res_path + '/%04d.png' % idx)
    else:
        plt.savefig(res_path + '/%04d.png' % idx, dpi=dpi)

    plt.close()
