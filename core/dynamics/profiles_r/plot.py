from matplotlib import pyplot as plt


def plot_profiles_r(data, res_path, **params):
    rlim = params['rlim']
    language = params['language']

    if not data:
        raise Exception('Empty r_slices!')

    font_size = 40
    font_weight = 'bold'
    plt.figure(figsize=(10, 7))
    for idx in range(len(data)):
        lmbda, r_max, i_0, r_slice = data[idx]['lmbda'], \
                                     data[idx]['r_max'], \
                                     data[idx]['i_0'], \
                                     data[idx]['r_slice']
        n_r = len(r_slice)
        dr = r_max / n_r
        rs = [i * dr for i in range(n_r)]

        if lmbda == 1235:
            color = 'blue'
        elif lmbda == 1557:
            color = 'green'
        elif lmbda == 1800:
            color = 'red'
        else:
            raise Exception('Wrong color!')

        for i in range(len(r_slice)):
            r_slice[i] *= i_0 / 10**12

        if language == 'english':
            label = '$\lambda_0 = %d$ nm' % lmbda
        else:
            label = '$\lambda_0 = %d$ нм' % lmbda

        plt.plot(rs, r_slice, color=color, linewidth=5, alpha=0.8, label=label)

    plt.xlim(rlim)

    plt.xticks(fontsize=font_size-10, fontweight=font_weight)
    plt.yticks(fontsize=font_size-10, fontweight=font_weight)

    if language == 'english':
        xlabel = '$\mathbf{r}$, $\mathbf{\mu}$m'
        ylabel = '$\mathbf{I}$, TW/cm$\mathbf{^2}$'
    else:
        xlabel = '$\mathbf{r}$, мкм'
        ylabel = '$\mathbf{I}$, ТВт/см$\mathbf{^2}$'
    plt.xlabel(xlabel, fontsize=font_size, fontweight=font_weight)
    plt.ylabel(ylabel, fontsize=font_size, fontweight=font_weight)

    plt.grid(linewidth=2, linestyle='dotted', color='black', alpha=0.5)

    plt.legend(bbox_to_anchor=(0., 1.1, 1., .102), fontsize=font_size - 23, loc='center', ncol=3)

    plt.savefig(res_path + '/bullets_profiles.png', bbox_inches='tight')
    plt.show()
    plt.close()

