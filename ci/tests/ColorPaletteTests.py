"""Regression checks for color conversions and the palette quality dashboard."""
import contextlib
import io
import unittest
import numpy as np
import matplotlib.pyplot as plt
from McUtils.Plots import ColorPalette


class ColorPaletteTests(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def test_standard_xyz_primaries_and_lab_white(self):
        # Reference values, rather than a round trip that masks transposed matrices.
        np.testing.assert_allclose(ColorPalette.rgb_to_xyz(255, 0, 0),
                                   [41.2453, 21.2671, 1.9334], atol=1e-6)
        np.testing.assert_allclose(ColorPalette.rgb_to_xyz(0, 255, 0),
                                   [35.758, 71.516, 11.9193], atol=1e-6)
        np.testing.assert_allclose(ColorPalette.rgb_to_lab(255, 255, 255),
                                   [100, 0, 0], atol=0.02)

    def test_xyz_to_rgb_known_red(self):
        np.testing.assert_allclose(ColorPalette.xyz_to_rgb(41.2453, 21.2671, 1.9334),
                                   [255, 0, 0], atol=1e-5)

    def test_vectorized_color_roundtrips(self):
        rgb = np.random.default_rng(73).uniform(0, 255, (3, 8, 5))
        for space in ['xyz', 'lab', 'lch', 'hsl', 'hsv']:
            with self.subTest(space=space):
                converted = ColorPalette.color_convert(rgb, 'rgb', space)
                restored = ColorPalette.color_convert(converted, space, 'rgb')
                np.testing.assert_allclose(restored, rgb, atol=1e-7)

    def test_palette_lighten_changes_lightness(self):
        palette = ColorPalette(['#FFB257', '#85BADD', '#B985BD'])
        dark = palette.lighten(-0.2)
        np.testing.assert_allclose(dark.lab_colors[:, 0],
                                   0.8 * palette.lab_colors[:, 0], atol=1e-7)
        self.assertNotEqual(palette.color_strings, dark.color_strings)

    def test_modify_in_same_space(self):
        lab = np.array([[60., 50.], [10., 15.], [5., 8.]])
        changed = ColorPalette.color_modify(lab, lambda l, a, b: [l - 10, a, b],
                                            color_space='lab', modification_space='lab')
        np.testing.assert_allclose(changed[0], [50., 40.])
        np.testing.assert_allclose(changed[1:], lab[1:])

    def test_cvd_zero_severity_and_full_simulations(self):
        rgb = np.array([[12., 190., 252.], [200., 110., 70.], [49., 3., 230.]])
        for cvd in ColorPalette.DEFAULT_CVD_TYPES:
            with self.subTest(cvd=cvd):
                np.testing.assert_allclose(ColorPalette.simulate_cvd(*rgb, cvd, severity=0),
                                           rgb, atol=1e-7)
                full = ColorPalette.simulate_cvd(*rgb, cvd)
                self.assertEqual(full.shape, rgb.shape)
                self.assertTrue(np.isfinite(full).all())
                self.assertTrue(((0 <= full) & (full <= 255)).all())

    def test_luminance_and_contrast(self):
        self.assertAlmostEqual(ColorPalette.relative_luminance(255, 0, 0), .212671)
        self.assertAlmostEqual(ColorPalette.relative_luminance(0, 255, 0), .715160)
        self.assertAlmostEqual(ColorPalette.relative_luminance(0, 0, 255), .072169)
        self.assertAlmostEqual(ColorPalette.contrast_ratio([0]*3, [255]*3), 21.)
        self.assertAlmostEqual(ColorPalette.contrast_ratio([50]*3, [50]*3), 1.)

    def test_luminance_matches_xyz_y_for_batches(self):
        rgb = np.random.default_rng(84).uniform(0, 255, (3, 4, 7))
        np.testing.assert_allclose(ColorPalette.relative_luminance(*rgb),
                                   ColorPalette.rgb_to_xyz(*rgb)[1] / 100,
                                   atol=1e-15)

    def test_luminance_uses_subclass_matrix(self):
        class CalibratedPalette(ColorPalette):
            rgb_to_xyz_array = np.array(ColorPalette.rgb_to_xyz_array, copy=True)
            rgb_to_xyz_array[1] = [0.25, 0.65, 0.10]

        self.assertAlmostEqual(CalibratedPalette.relative_luminance(255, 0, 0), .25)
        self.assertAlmostEqual(CalibratedPalette.relative_luminance(0, 255, 0), .65)
        self.assertAlmostEqual(CalibratedPalette.relative_luminance(0, 0, 255), .10)
        self.assertAlmostEqual(CalibratedPalette.contrast_ratio([255, 0, 0], [0]*3), 6.)
        # Replacing a profile must leave the base class's profile untouched.
        self.assertAlmostEqual(ColorPalette.relative_luminance(255, 0, 0), .212671)

    def test_dashboard_renders_all_conditions(self):
        palette = ColorPalette(['#AD590C', '#2B5900', '#007CB5', '#AF333C', '#663166', '#887100'])
        with contextlib.redirect_stdout(io.StringIO()):
            figures = palette.run_palette_quality_dashboard()
        conditions = ['original', *ColorPalette.DEFAULT_CVD_TYPES]
        expected = {'swatches', 'contrast'} | {
            f'{kind}_{cond}' for kind in ['line', 'bar', 'delta_e'] for cond in conditions
        }
        self.assertEqual(set(figures), expected)
        for name, fig in figures.items():
            with self.subTest(figure=name):
                output = fig.to_png().getvalue()
                self.assertTrue(output.startswith(b'\x89PNG\r\n\x1a\n'))
                self.assertGreater(len(output), 1000)

    def test_dashboard_empty_cvd_list_and_singleton(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            figures = ColorPalette(['#663166']).run_palette_quality_dashboard(cvd_types=[])
        self.assertEqual(set(figures), {'swatches', 'contrast', 'line_original',
                                       'bar_original', 'delta_e_original'})
        self.assertIn('[N/A]', output.getvalue())
        self.assertEqual(figures['swatches'].shape, (1, 1))
        for fig in figures.values():
            fig.to_png()

    def test_dashboard_accepts_cvd_generator(self):
        with contextlib.redirect_stdout(io.StringIO()):
            figures = ColorPalette(['#AD590C', '#007CB5']).run_palette_quality_dashboard(
                cvd_types=(condition for condition in ['protanopia']))
        self.assertIn('line_protanopia', figures)
        self.assertIn('line_original', figures)

    def test_swatch_rows_remain_visible_after_layout(self):
        grid = ColorPalette(['#AD590C', '#2B5900', '#007CB5']).plot_swatch_grid()
        for _ in range(2):
            grid.prep_show()
            for row in range(4):
                axes = grid[row, 0].axes.obj
                self.assertGreater(axes.get_position().height, 0.1)
                self.assertEqual(len(axes.collections), 3)
                self.assertEqual(axes.texts[0].get_text(),
                                 ['original', *ColorPalette.DEFAULT_CVD_TYPES][row])

    def test_distance_matrix_properties(self):
        palette = ColorPalette(['#AD590C', '#2B5900', '#007CB5'])
        for cvd in [None, *ColorPalette.DEFAULT_CVD_TYPES]:
            distance = palette.delta_e_matrix(cvd)
            np.testing.assert_allclose(distance, distance.T)
            np.testing.assert_allclose(np.diag(distance), 0)
            self.assertGreater(distance[0, 1], 0)


if __name__ == '__main__':
    unittest.main()
