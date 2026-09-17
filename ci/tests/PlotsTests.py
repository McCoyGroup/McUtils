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

    @validationTest
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

    @validationTest
    def test_PlotlyBackend(self):
        g = np.linspace(0, 2*np.pi, 25)
        Plot(g, np.sin(g),
             backend='plotly',
             # ticks=[[0, 1, 2], [0, 1, 2]],
             # plot_range=[[0, 2], [0, 2]],
             frame=True,
             aspect_ratio=1/1.16
             ).show()

    @validationTest
    def test_X3DMathText(self):
        fig = Graphics3D(backend='x3d', view_settings={'view_distance':5})
        # Cube([0, 0, 0], [(1 - 1 + 0) / np.sqrt(6), (1 + 1 + 0)/ np.sqrt(6), (0 + 0 + np.sqrt(2)) / np.sqrt(6)],
        #      normal=[1, 1, 0],
        #      # rotation=[1, 1, 0, 1],
        #      color='gray').plot(fig)
        Text("$\\sqrt{5}$", [1, 0, 0], color='red', billboard=False).plot(fig)
        # Text("$\\int_{x=10}^{100} \\sqrt{20} e^{(-x^2)}$", [-1, 0, 0], color='blue', font_size=20, billboard=False).plot(fig)
        # Text("s5", [-1, 0, 0], color='black', billboard=False, solid=False).plot(fig)
        # print(fig.to_widget().tostring(prettify=True))
        # fig.to_widget().write("/Users/Mark/Desktop/new_text2.html")
        fig.show()

    @validationTest
    def test_Plotly3D(self):
        fig = Graphics3D(backend='plotly3D', frame=False, subplot_kw={'include_save_buttons':True})
        Sphere([1, 0, 0], .1, color='red').plot(fig)
        # print(fig.to_widget().tostring(prettify=True))
        fig.show()

    @validationTest
    def test_BaseSVG(self):
        fig = SVGFigure(height=800)#, view_box=[[0, 100], [0, 100]])
        # fig.add_rect(x=0, y=0, width=100, height=100, fill='red',
        #              transform=[
        #                  ['rotate', [30]]
        #              ])
        # fig.add_rect(x=100, y=100, width=100, height=100, fill='blue')
        fig.add_path(d=[
            ["M", [0, 0]],
            ["L", [100, 100]],
            ["Q", [100, 0, 0, 0]],
            ["l", [100, 0, 0, 100]],
        ], stroke='green', fill='none')
        print(
            fig.to_svg().tostring(prettify=True)
        )
        fig.to_svg().display()

    @validationTest
    def test_SVGBackend2D(self):
        fig = Graphics(backend='svg')
        Rectangle(
            [[0, 0], [100, 100]],
            fill='red',
            transform=[
                ['rotate', [30]]
            ]
        ).plot(fig)
        Rectangle(
            [[100, 100], [200, 200]],
            fill='blue',
            # transform=[
            #     ['rotate', [30]]
            # ]
        ).plot(fig)
        # Path(
        #     [[100, 100], [200, 200]],
        #     fill='blue',
        #     # transform=[
        #     #     ['rotate', [30]]
        #     # ]
        # ).plot(fig)
        # print(
        #     fig.to_widget().tostring(prettify=True)
        # )
        fig.show()

    @validationTest
    def test_SVGBackend3D(self):

        fig = Graphics3D(backend='svg3D',
                         image_size=[500, 500],
                         padding=0,
                         plot_range=[[-100, 100], [-100, 100], [-100, 100]],
                         background='gray',
                         view_settings={
                             "view_vector":[0, 0, 1],
                             "up_vector":[0, 1, 0],
                             # "view_position":[0, 0, 1]
                         })
        # Rectangle(
        #     [[0, 0, 0], [100, 100, 0]],
        #     fill='red',
        #     # rotation=np.pi/6
        # ).plot(fig)
        # Rectangle(
        #     [[-100, -100, 0], [0, 0, 50]],
        #     fill='pink',
        #     # rotation=np.pi/6
        # ).plot(fig)
        Path([
            ["M", [0, 0]],
            ["L", [100, 100]],
            ["Q", [100, 0, 0, 0]],
            ["l", [100, 0, 0, 100]],
        ], stroke='green', fill='none', rotation=np.pi/6, normal=[0, 1, 1]).plot(fig)
        fig.show()

    def test_SVGFigure3DProjectsStrokeWidths(self):
        from McUtils.Plots.SVG import SVGCylinder, SVGSphere

        projection = np.eye(4)
        projection[0, 0] = projection[1, 1] = 2
        projection[2, 3] = -1
        projection[3, 3] = 10

        sphere = SVGSphere(
            center=[0, 0, 0], radius=.4, **{'stroke-width': '.01px'}
        )
        sphere_kwargs, _ = sphere.prep_kwargs(projection)
        self.assertAlmostEqual(
            float(sphere_kwargs['stroke-width'].removesuffix('px')),
            .002
        )

        cylinder = SVGCylinder(
            [0, 0, 0], [1, 0, 5], .1, **{'stroke-width': '.01px'}
        )
        cylinder_kwargs, _ = cylinder.prep_kwargs(projection)
        # Mean endpoint scale: 2 * mean(1/10, 1/5) == .3.
        self.assertAlmostEqual(
            float(cylinder_kwargs['stroke-width'].removesuffix('px')),
            .003
        )

    def test_SVGFigure3DViewScale(self):
        from McUtils.Plots.SVG import SVGFigure3D

        fig = SVGFigure3D(view_scale=2)
        fig.set_projection_kwargs(render_matrix=np.eye(4))
        fig.add_sphere(center=[0, 0, 0], radius=1, fill='red')

        root = fig.to_svg()
        _, _, width, height = root['viewBox']
        self.assertAlmostEqual(width, 4)
        self.assertAlmostEqual(height, 4)
        self.assertEqual(fig.get_projection_kwargs()['view_scale'], 2)

    def test_SVGFigure3DInteractiveRuntime(self):
        import tempfile
        from McUtils.Plots.SVG import SVGFigure3D

        fig = SVGFigure3D(
            id='interactive-svg-test',
            view_box=np.array([[-2, 2], [-2, 2], [-2, 2]])
        )
        fig.set_projection_kwargs(render_matrix=np.eye(4))
        fig.add_line(
            x1=0, y1=0, z1=0, x2=1, y2=1, z2=1, stroke='black'
        )
        fig.add_sphere(
            center=[0, 0, 0], radius=.2, fill='red',
            **{'stroke-width': '.01px'}
        )

        static_source = fig.to_svg().tostring()
        self.assertNotIn('McUtilsSVG3D.ready', static_source)

        interactive_source = fig.to_svg(interactive=True).tostring()
        self.assertIn('id="interactive-svg-test"', interactive_source)
        self.assertIn('McUtilsSVG3D.ready(event)', interactive_source)
        self.assertIn('api.figures["interactive-svg-test"]', interactive_source)
        self.assertIn('interactive-svg-test-primitive-0', interactive_source)
        self.assertIn('interactive-svg-test-primitive-1', interactive_source)
        self.assertIn('scaleStroke(primitive, projected)', interactive_source)
        self.assertIn('"strokeWidth"', interactive_source)

        with tempfile.TemporaryDirectory() as tmpdir:
            runtime_file = os.path.join(tmpdir, 'runtime.js')
            linked_source = fig.to_svg(
                interactive=True,
                runtime_file=runtime_file,
                runtime_src='assets/runtime.js'
            ).tostring()
            self.assertTrue(os.path.isfile(runtime_file))
            self.assertIn('assets/runtime.js', linked_source)
            with open(runtime_file) as runtime_stream:
                runtime_source = runtime_stream.read()
            self.assertIn('api.figures["interactive-svg-test"]', runtime_source)

    @validationTest
    def test_MPLPath(self):
        fig = Graphics(backend='svg')
        # Path([
        #     ["M", [0, 0]],
        #     ["L", [100, 100]],
        #     ["Q", [100, 0, 0, 0]],
        #     ["l", [100, 0, 0, 100]],
        # ], stroke='pink').plot(fig)

        Path([
            ["M", [0, 0]],
            ["L", [100, 100]],
            ["Q", [100, 0, 0, 0]],
            ["l", [100, 0, 0, 100]],
        ], stroke='pink', use_polyline=True).plot(fig)
        fig.show()

    @validationTest
    def test_MeshBackend(self):
        from Psience.Molecools import Molecule

        Molecule.from_string('').plot(backend='mesh3D').savefig("/Users/Mark/Desktop/water.glb")
        # fig = Graphics3D(backend='mesh3D',
        #                  # image_size=[500, 500],
        #                  # padding=0,
        #                  # plot_range=[[-100, 100], [-100, 100], [-100, 100]],
        #                  background='gray',
        #                  view_settings={
        #                      "view_vector": [0, 0, 1],
        #                      "up_vector": [0, 1, 0],
        #                      # "view_position":[0, 0, 1]
        #                  })
        # Sphere([1, 0, 0], .1, color='red', transparency=.2).plot(fig)
        # fig.show()

    @debugTest
    def test_InvertAxes(self):
        import matplotlib as mpl
        # ['gtk3agg', 'gtk3cairo', 'gtk4agg', 'gtk4cairo', 'macosx', 'nbagg', 'notebook', 'qtagg', 'qtcairo', 'qt5agg', 'qt5cairo', 'tkagg', 'tkcairo', 'webagg', 'wx', 'wxagg', 'wxcairo', 'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template', 'inline']
        mpl.use('macosx')

        HistogramPlot(np.random.normal(size=1000),
                      density=True,
                      invert=True,
                      normalize=True).show()