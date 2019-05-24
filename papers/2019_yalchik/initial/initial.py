from core import plot_intensity_xy_3d, plot_intensity_rt_3d, plot_phase_3d


plot_intensity_xy_3d(M=1,
                     n=256,
                     r_0=92,
                     x_ticks=[-200, -100, 0, 100, 200],
                     y_ticks=[-200, -100, 0, 100, 200],
                     z_ticks=[0, 0.25, 0.5],
                     z_lim=[0, 0.6])

plot_intensity_rt_3d(M=2,
                     n=256,
                     r_0=92,
                     t_0=40,
                     r_ticks=[-200, -100, 0, 100, 200],
                     t_ticks=[-100, -50, 0, 50, 100],
                     z_ticks=[0, 0.25, 0.5],
                     z_lim=[0, 0.6])

plot_phase_3d(m=1,
              n=256,
              x_ticks=[-200, -100, 0, 100, 200],
              y_ticks=[-200, -100, 0, 100, 200])


