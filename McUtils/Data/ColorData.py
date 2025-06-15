import numpy as np
from .CommonData import DataHandler, DataRecord

__all__ = [ "ColorData" ]
__reload_hook__ = [".CommonData"]

class ColorDataHandler(DataHandler):
    def __init__(self):
        super().__init__("ColorData", record_type=ColorDataRecord)

    def __getitem__(self, item):
        if isinstance(item, int):
            item = list(self.data['Palettes'].keys())[item]
            return super().__getitem__(('Palettes', item))
        elif isinstance(item, str) and item not in self.data:
            for k,v in self.data.items():
                if item in v:
                    return super().__getitem__((k, item))
            else:
                raise KeyError(f"couldn't find `ColorData` spec {item}")
        else:
            return super().__getitem__(item)

            # return super().__getitem__(('Gradients', item))

    @classmethod
    def rgb_code(cls, rgb, padding=2):
        if not isinstance(rgb[0], (int, float, np.floating, np.integer)):
            return [
                cls.rgb_code([r, g, b])
                for r, g, b in zip(*rgb)
            ]
        rgb = np.round(rgb).astype(int)
        return f"#{rgb[0]:0>{padding}x}{rgb[1]:0>{padding}x}{rgb[2]:0>{padding}x}"
    @classmethod
    def parse_rgb_code(cls, code, padding=2):
        if code[0] == "#":
            code = code[1:]
        return [
            int(code[(padding*i):(padding*(i+1))], 16)
            for i in range(3)
        ]

    converters = {}
    @classmethod
    def color_convert(self, color, original_space, target_space):
        if (original_space, target_space) in self.converters:
            conversion = self.converters[(original_space, target_space)]
        else:
            conversion = getattr(self, f"{original_space}_to_{target_space}") #TODO: register these better

        return conversion(*color)

    xyz_to_rbg_array = [
        [ 3.2406, -1.5372, -0.4986],
        [-0.9689,  1.8758,  0.0415],
        [ 0.0557, -0.2040,  1.0570],
    ]
    @classmethod
    def xyz_to_rgb(self, x, y, z):
        # converted from https://www.easyrgb.com/en/math.php
        if not isinstance(self.xyz_to_rbg_array, np.ndarray):
            self.xyz_to_rbg_array = np.array(self.xyz_to_rbg_array)

        xyz = np.array([x, y, z]) / 100
        rgb = np.dot(self.xyz_to_rbg_array, xyz)
        mask = rgb > 0.0031308
        rgb[mask] = 1.055*rgb[mask]**(1/2.4) - 0.055
        not_mask = np.logical_not(mask)
        rgb[not_mask] = rgb[not_mask] * 12.92
        return rgb * 255

    rgb_to_xyz_array = [ # just the inverse
        [0.4124, 0.3576, 0.1805],
        [0.2126, 0.7152, 0.0722],
        [0.0193, 0.1192, 0.9505],
    ]
    @classmethod
    def rgb_to_xyz(self, r, g, b):
        if not isinstance(self.rgb_to_xyz_array, np.ndarray):
            self.rgb_to_xyz_array = np.array(self.rgb_to_xyz_array)

        rgb = np.array([r, g, b]) / 255
        mask = rgb > 0.04045
        rgb[mask] = ((rgb[mask] + 0.055) / 1.055)**(2.4)
        not_mask = np.logical_not(mask)
        rgb[not_mask] = rgb[not_mask] / 12.92

        xyz = np.dot(self.rgb_to_xyz_array, rgb)
        return xyz * 100

    @classmethod
    def _rgb2hue(cls, rgb, diff, max_val):

        diff_r, diff_g, diff_b = [
            ((max_val - c) / 6 + (diff / 2)) / diff
            for c in rgb
        ]
        r_primary, g_primary, b_primary = [
            max_val == c
            for c in rgb
        ]

        h = np.zeros_like(diff)
        h[r_primary] = (diff_b - diff_g)
        h[g_primary] = (1 / 3 + diff_r - diff_b)
        h[b_primary] = (2 / 3 + diff_g - diff_r)

        h[h < 0] += 1
        h[h > 1] -= 1

        return h
    @classmethod
    def rgb_to_hsl(self, r, g, b):

        rgb = np.array([r, g, b]) / 255
        smol = rgb.ndim == 1
        if smol:
            rgb = rgb[:, np.newaxis]

        min_val = np.min(rgb, axis=0)
        max_val = np.max(rgb, axis=0)
        diff = max_val - min_val

        L = (max_val + min_val) / 2

        non_gray = diff > 0
        s = np.zeros_like(L)
        h = np.zeros_like(L)
        if non_gray.any():
            s[non_gray] = (diff / (2 - (max_val + min_val)))
            dim_mask = np.logical_and(non_gray, L < .5)
            s[dim_mask] = (diff / (max_val + min_val))[dim_mask]

            h_ = self._rgb2hue(rgb[:, non_gray], diff[non_gray], max_val[non_gray])
            h[non_gray] = h_

        hsl = np.array([h, s, L])
        if smol:
            hsl = hsl[:, 0]

        return hsl

    @classmethod
    def _hue2rgb(cls, v1, v2, h):

        h = np.array(h)
        v1 = np.array(v1)
        v2 = np.array(v2)
        h[h < 0] += 1
        h[h > 1] -= 1

        res = v1.copy()
        mask = 6*h < 1
        res[mask] = v1[mask] + (v2[mask] - v1[mask]) * 6*h[mask]
        rem = np.logical_not(mask)
        mask = np.logical_and(rem, 2*h < 1)
        res[mask] = v2[mask]
        rem = np.logical_and(rem, np.logical_not(mask))
        mask = np.logical_and(rem, 3*h < 2)
        res[mask] = v1[mask] + (v2[mask] - v1[mask]) * 6*(2/3 - h[mask])

        return res

    @classmethod
    def hsl_to_rgb(cls, h, s, l):

        hsl = np.array([h, s, l])
        smol = hsl.ndim == 1
        if smol:
            hsl = hsl[:, np.newaxis]
        non_gray = hsl[1] > 0
        dim = np.logical_and(non_gray, hsl[2] < .5)

        rgb = np.zeros_like(hsl)
        if non_gray.any():
            h, s, L = hsl
            v2 = np.zeros_like(h)
            v2[non_gray] = ((L + s) - (s * L))[non_gray]
            v2[dim] = (L * (1 + s))[dim]

            v1 = np.zeros_like(h)
            v1[non_gray] = 2 * L[non_gray] - v2[non_gray]

            for i,shift in enumerate([1/3, 0, -1/3]):
                rgb[i, non_gray] = cls._hue2rgb(v1[non_gray], v2[non_gray], h[non_gray] + shift)

        if smol:
            rgb = rgb[:, 0]

        return rgb * 255

    @classmethod
    def rgb_to_hsv(self, r, g, b):

        rgb = np.array([r, g, b]) / 255
        smol = rgb.ndim == 1
        if smol:
            rgb = rgb[:, np.newaxis]

        min_val = np.min(rgb, axis=0)
        max_val = np.max(rgb, axis=0)
        diff = max_val - min_val

        v = max_val

        non_gray = diff > 0
        s = np.zeros_like(v)
        h = np.zeros_like(v)
        if non_gray.any():
            s[non_gray] = (diff / max_val)[non_gray]
            h_ = self._rgb2hue(rgb[:, non_gray], diff[non_gray], max_val[non_gray])
            h[non_gray] = h_

        hsl = np.array([h, s, v])
        if smol:
            hsl = hsl[:, 0]

        return hsl

    @classmethod
    def hsv_to_hsl(cls, h, s, v):

        hsv = np.array([h, s, v])
        smol = hsv.ndim == 1
        if smol:
            hsv = hsv[:, np.newaxis]

        h, s, v = hsv
        max_val = np.array(v)
        diff = max_val * np.array(s)
        min_val = max_val - diff

        L = (max_val + min_val) / 2

        non_gray = diff > 0
        s = np.zeros_like(L)
        if non_gray.any():
            s[non_gray] = (diff / (2 - (max_val + min_val)))
            dim_mask = np.logical_and(non_gray, L < .5)
            s[dim_mask] = (diff / (max_val + min_val))[dim_mask]

        hsl = np.array([h, s, L])
        if smol:
            hsl = hsl[:, 0]

        return hsl

    @classmethod
    def hsv_to_rgb(cls, h, s, v):
        return cls.hsl_to_rgb(*cls.hsv_to_hsl(h, s, v))

    lab_scaling_reference = [95.0489, 100.0, 108.8840]
    @classmethod
    def xyz_to_lab(cls, x, y, z, scaling=None):

        xyz = np.array([x, y, z])
        smol = xyz.ndim == 1
        if smol:
            xyz = xyz[:, np.newaxis]

        if scaling is None:
            scaling = cls.lab_scaling_reference

        xyz /= np.array(scaling)[:, np.newaxis]

        mask = xyz > 0.008856
        xyz[mask] = xyz[mask] ** (1/3)
        not_max = np.logical_not(mask)
        xyz[not_max] = (7.787 * xyz[not_max]) + (16/116)

        L = 116 * xyz[1] - 16
        a = 500 * (xyz[0] - xyz[1])
        b = 200 * (xyz[1] - xyz[2])

        lab = np.array([L, a, b])
        if smol:
            lab = lab[:, 0]

        return lab

    @classmethod
    def lab_to_xyz(cls, l, a, b, scaling=None):

        lab = np.array([l, a, b])
        smol = lab.ndim == 1
        if smol:
            lab = lab[:, np.newaxis]

        if scaling is None:
            scaling = cls.lab_scaling_reference

        y = (lab[0] + 16) / 116
        x = lab[1] / 500 + y
        z = y - lab[2] / 200

        xyz = np.array([x, y, z])

        mask = xyz**3 > 0.008856
        xyz[mask] = xyz[mask] ** (3)
        not_max = np.logical_not(mask)
        xyz[not_max] = (xyz[not_max] - (16/116)) / 7.787

        xyz *= np.array(scaling)[:, np.newaxis]
        if smol:
            xyz = xyz[:, 0]

        return xyz

    @classmethod
    def rgb_to_lab(cls, r, g, b, xyz_scaling=None):
        return cls.xyz_to_lab(*cls.rgb_to_xyz(r, g, b), scaling=xyz_scaling)
    @classmethod
    def lab_to_rgb(cls, l, a, b, xyz_scaling=None):
        return cls.xyz_to_rgb(*cls.lab_to_xyz(l, a, b, scaling=xyz_scaling))

class ColorDataRecord(DataRecord):
    """
    Represents a simple callable wavefunction...
    """
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        # TODO: add more sophisticated blending
        self.abcissae = np.linspace(0, 1, len(self.data))
        self._lab_colors = None
        self.flipped = False

    def flip(self):
        new = type(self)(self.handler, self.key, self.data)
        new.abcissae = self.abcissae #TODO: make this flip properly...
        new.data = list(reversed(self.data))
        new.flipped = not self.flipped
        return new

    def __eq__(self, other):
        if not hasattr(other, 'handler'):
            return False
        if other.handler is not self.handler:
            return False
        if other.flipped != self.flipped:
            return False
        return self.key == other.key

    # def __len__(self):
    #     return len(self.data)
    # def __getitem__(self, item):
    #     return self.data[item]
    def blend(self, amount):
        insertion_index = np.searchsorted(self.abcissae, amount)
        if insertion_index == len(self.abcissae):
            return self.data[-1]
        elif insertion_index == 0:
            return self.data[0]

        x = self.abcissae[insertion_index-1]
        y = self.abcissae[insertion_index]
        d = (amount-x) / (y-x)

        if self._lab_colors is None:
            arr = np.array([ColorData.parse_rgb_code(d) for d in self.data])
            self._lab_colors = ColorData.color_convert(arr.T, "rgb", "lab").T

        new_lab = self._lab_colors[insertion_index-1] * (1 - d) + self._lab_colors[insertion_index] * d

        rgb = ColorData.color_convert(new_lab, 'lab', 'rgb')
        return ColorData.rgb_code(rgb)
    def index(self, i):
        return self.data[i%len(self.data)]
    def __call__(self, amount):
        return self.blend(amount)

ColorData=ColorDataHandler()
ColorData.__doc__ = """An instance of `ColorDataHandler` that can be used for looking up data on color palettes"""
ColorData.__name__ = "ColorData"