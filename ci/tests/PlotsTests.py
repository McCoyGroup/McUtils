
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Plots import *
import sys, os, numpy as np

class PlotsTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        import matplotlib.pyplot as plt
        # plt.show()

    def result_file(self, fname):
        if not os.path.isdir(os.path.join(TestManager.test_dir, "test_results")):
            os.mkdir(os.path.join(TestManager.test_dir, "test_results"))
        return os.path.join(TestManager.test_dir, "test_results", fname)

    @validationTest
    def test_Plot(self):
        grid = np.linspace(0, 2*np.pi, 100)
        plot = Plot(grid, np.sin(grid))
        plot.show()

        # plot.savefig(self.result_file("test_Plot.png"))
        plot.close()
        # plot.show()

    @validationTest
    def test_Plot3D(self):
        import matplotlib.cm as colormaps

        f = lambda pt: np.sin(pt[0]) + np.cos(pt[1])
        plot = Plot3D(f, np.arange(0, 2 * np.pi, .1), np.arange(0, 2 * np.pi, .1),
                      plot_style={
                          "cmap": colormaps.get_cmap('viridis')
                      },
                      axes_labels=['dogs', 'cats',
                                   Styled('rats', color='red')
                                   ],
                      plot_label='my super cool 3D plot',
                      plot_range=[(-5, 5)] * 3,
                      plot_legend='i lik turtle',
                      colorbar=True
                      )
        plot.savefig(self.result_file("test_Plot3D.png"))
        plot.close()

    @validationTest
    def test_GraphicsGrid(self):

        main = GraphicsGrid(ncols=3, nrows=1)
        grid = np.linspace(0, 2 * np.pi, 100)
        grid_2D = np.meshgrid(grid, grid)
        main[0, 0] = ContourPlot(grid_2D[1], grid_2D[0], np.sin(grid_2D[0]), figure=main[0, 0])
        main[0, 1] = ContourPlot(grid_2D[1], grid_2D[0], np.sin(grid_2D[0]) * np.cos(grid_2D[1]), figure=main[0, 1])
        main[0, 2] = ContourPlot(grid_2D[1], grid_2D[0], np.cos(grid_2D[1]), figure=main[0, 2])
        # main.show()

        main.savefig(self.result_file("test_GraphicsGrid.png"))
        main.close()

    @validationTest
    def test_PlotStyling(self):
        grid = np.linspace(0, 2 * np.pi, 100)
        # file = '~/Desktop/y.png'
        plot = Plot(grid, np.sin(grid),
                    aspect_ratio=1.3,
                    theme='dark_background',
                    ticks_style={'color':'red', 'labelcolor':'red'},
                    plot_label='bleh',
                    padding=((30, 0), (20, 20))
                    )
        # plot.savefig(file)
        # plot = Image.from_file(file)
        plot.show()
        # plot.savefig(self.result_file("test_PlotStyling.png"))
        plot.close()

    @validationTest
    def test_PlotGridStyling(self):
        main = GraphicsGrid(ncols=3, nrows=1, theme='Solarize_Light2', figure_label='my beuatufil triptych',
                            padding=((50, 10), (50, 65)),
                            spacings=[50, 0])
        grid = np.linspace(0, 2 * np.pi, 100)
        grid_2D = np.meshgrid(grid, grid)
        x = grid_2D[1]; y = grid_2D[0]
        main[0, 0] = ContourPlot(x, y, np.sin(y), plot_label='$sin(x)$',
                                 axes_labels=[None, "cats (cc)"],
                                 figure=main[0, 0]
                                 )
        main[0, 1] = ContourPlot(x, y, np.sin(x) * np.cos(y),
                                 plot_label='$sin(x)cos(y)$',
                                 axes_labels=[Styled("dogs (arb.)", {'color': 'red'}), None],
                                 figure=main[0, 1])
        main[0, 2] = ContourPlot(x, y, np.cos(y), plot_label='$cos(y)$', figure=main[0, 2])
        main.colorbar = {"graphics": main[0, 1].graphics}

        main.show()
        # main.savefig(self.result_file("test_PlotGridStyling.png"))
        main.close()

    @validationTest
    def test_Scatter(self):
        pts = np.random.rand(50, 2)
        plot = ScatterPlot(*pts.T,
                           aspect_ratio=2,
                           image_size=250
                           )
        plot.show()
        # plot.savefig(self.result_file("test_Scatter.pdf"), format='pdf')
        plot.close()

    @validationTest
    def test_ListContourPlot(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListContourPlot(ptss)

        plot.savefig(self.result_file("test_ListContourPlot.png"))
        plot.close()

    @validationTest
    def test_ListTriPlot3D(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListTriPlot3D(ptss)

        plot.savefig(self.result_file("test_ListTriPlot3D.png"))
        plot.close()

    @validationTest
    def test_ListTriDensityPlot(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListTriDensityPlot(ptss)

        plot.savefig(self.result_file("test_ListTriDensityPlot.png"))
        plot.close()

    @validationTest
    def test_ListTriContourPlot(self):
        pts = np.pi*np.random.rand(150, 2)
        sins = np.sin(pts[:, 0])
        coses = np.cos(pts[:, 1])
        ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
        plot = ListTriContourPlot(ptss)
        plot.add_colorbar()

        plot.savefig(self.result_file("test_ListTriContourPlot.png"))
        plot.close()

    @inactiveTest
    def test_Animation(self):
        "Currently broken"
        def get_data(*args):
            pts = np.pi*np.random.normal(scale = .25, size=(10550, 2))
            sins = np.sin(pts[:, 0])
            coses = np.cos(pts[:, 1])
            ptss = np.concatenate((pts, np.reshape(sins*coses, sins.shape + (1,))), axis=1)
            return (ptss, )
        plot = ListTriContourPlot(*get_data(),
                                  animate = get_data,
                                  plot_range = [
                                      [-np.pi, np.pi],
                                      [-np.pi, np.pi]
                                  ]
                                  )

        plot.show()

        plot.savefig(self.result_file("test_ListTriContourPlot.gif"))
        plot.close()

    @validationTest
    def test_X3D(self):
        plot = Graphics3D(backend="x3d", image_size=[1500, 500], background='white')
        Sphere(color='red').plot(plot)
        plot.show()

    @debugTest
    def test_ColorPalettes(self):
        rgb_code = np.array([255, 255, 255])
        conv = ColorPalette.color_convert(rgb_code, 'rgb', 'hsl')
        inv = ColorPalette.color_convert(conv, 'hsl', 'rgb')
        self.assertTrue(
            np.allclose(inv, rgb_code)
        )

        rgb_code = [200, 10, 25]
        for space in [
            'rgb', 'hsv', 'hsl', 'xyz', 'lab'
        ]:
            conv = ColorPalette.color_convert(rgb_code, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(
                np.allclose(inv, rgb_code)
            )

        rgb_codes = np.array([
            [0, 0, 0],
            [255, 255, 255],
        ]).T
        for space in [
            'rgb', 'hsv', 'hsl', 'xyz', 'lab'
        ]:
            conv = ColorPalette.color_convert(rgb_codes, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(
                np.allclose(inv, rgb_codes),
                msg=f"bad conversion for {space}: {rgb_codes}, {inv}"
            )

        rgb_codes = np.random.rand(3, 10, 50) * 255
        for space in [
            'rgb', 'hsv', 'hsl', 'xyz', 'lab'
        ]:
            conv = ColorPalette.color_convert(rgb_codes, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(
                np.allclose(inv, rgb_codes)
            )

        rgb_codes = np.ones((3, 1000, 500)) * 255
        for space in [
            'rgb', 'hsv', 'hsl', 'xyz', 'lab'
        ]:
            conv = ColorPalette.color_convert(rgb_codes, 'rgb', space)
            inv = ColorPalette.color_convert(conv, space, 'rgb')
            self.assertTrue(
                np.allclose(inv, rgb_codes)
            )

        print(ColorPalette("pastel").blend(.2))
        # return

        grid = np.linspace(0, 2 * np.pi, 200)
        # base_fig = None
        # for i in range(6):
        #     base_fig = Plot(
        #         grid,
        #         i + np.sin((i + 1) * grid),
        #         figure=base_fig,
        #         style_list={'color': ColorPalette("pastel")}
        #     )

        palette_base = [
                    "#3a2652", "#dcca00", "#a15547",
                    "#009b5d", "#14013d",
                    "#8d0001", "#494947"
                ]
        lighter_palette = [
            ColorPalette.color_lighten(c, .2, shift=True)
            for c in palette_base
        ]
        lighter_palette_hsl = [
            ColorPalette.color_lighten(c, .2, modification_space='hsl', shift=True)
            for c in palette_base
        ]

        for n,p in {
            'starters':'starters',
            'base':palette_base,
            'lighter':lighter_palette,
            'lighter_hsl':lighter_palette_hsl,
        }.items():
            base_fig = None
            print(ColorPalette(p).get_colorblindness_test_url())
            for i in range(6):
                base_fig = Plot(
                    grid,
                    i + np.sin((i + 1) * grid),
                    figure=base_fig,
                    style_list={'color': ColorPalette(p)},
                    plot_label=n
                )
            # base_fig.savefig(os.path.expanduser(f"~/Desktop/palette_example_{n}.png"))
        # base_fig.show()

        # palette = ColorPalette("WarioColors")
        # base_fig = None
        # for i in range(10):
        #     base_fig = Plot(
        #         grid,
        #         i + np.sin((i + 1) * grid),
        #         figure=base_fig,
        #         color=palette.blend(i / 9)
        #     )

    @validationTest
    def test_ColorMaps(self):
        print(
            ColorPalette('pastel').blend([
                0, .2, .5, 1.1
            ])
        )

        print(
            ColorPalette('pastel')([0, .2, .5, 1.1])
        )

        grid_x = np.linspace(0, 2*np.pi, 100)
        grid_y = np.linspace(0, 2*np.pi, 100)
        mg = np.meshgrid(grid_x, grid_y)
        grid_z = np.sum(np.meshgrid(np.sin(grid_x), np.cos(grid_y)), axis=0)
        ContourPlot(
            *mg,
            grid_z,
            cmap=ColorPalette('starters').as_colormap(
                levels=np.linspace(0, 1, 20)**2,
                cmap_type='interpolated'
            ),
            levels=50,
            colorbar=True
        ).show()
    # @validationTest
    # def test_Plot3D_adaptive(self):
    #     f = lambda pt: np.sin(pt[0]) + np.cos(pt[1])
    #     plot = Plot3D(f, [0, 2*np.pi], [0, 2*np.pi])
    #     plot.show()

    @validationTest
    def test_PropertySetting(self):
        StickPlot(
            np.linspace(0, 2*np.pi, 35),
            np.sin(np.linspace(0, 2*np.pi, 35)),
            color='red',
            label='spec_1',
            plot_legend=True
        ).show()

    @validationTest
    def test_PlotDelayed(self):
        p = Plot(background = 'black')
        for i, c in enumerate(('red', 'white', 'blue')):
            p.plot(np.sin, [-2 + 4/3*i, -2 + 4/3*(i+1)], color = c)
        # p.show()

        p.savefig(self.result_file("test_PlotDelayed.gif"))
        p.close()

    @validationTest
    def test_Plot3DDelayed(self):
        p = Plot3D(background = 'black')
        for i, c in enumerate(('red', 'white', 'blue')):
            p.plot(
                lambda g: (
                    np.sin(g.T[0]) + np.cos(g.T[1])
                ),
                [-2 + 4/3*i, -2 + 4/3*(i+1)],
                [-2 + 4/3*i, -2 + 4/3*(i+1)],
                color = c)
        # p.show()

        p.savefig(self.result_file("test_Plot3DDelayed.gif"))
        p.close()