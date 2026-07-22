"""Extracted from SymmetryTests.test_Characters via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest SymmetryTests.test_Characters"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Symmetry import *
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):

    @validationTest
    def test_Characters(self):
        print()
        ct = CharacterTable.point_group('Dh', 4)
        print(ct.format())
        ct = CharacterTable.point_group('Oh')
        print(ct.format())
        ct = CharacterTable.point_group('Cv', 2)
        print(ct.format())
        ct = CharacterTable.point_group('Td')
        print(ct.format())
        ct = CharacterTable.point_group('S', 4)
        print(ct.format())
        ct = CharacterTable.point_group('C', 3)
        print(ct.format())
        elements, classes = point_group_data('Cv', 5, prop='classes')
        self.assertEquals(np.sort(np.concatenate(classes)).tolist(), np.arange(sum((len(l) for l in classes))).tolist())
        self.assertEquals(len(elements), sum((len(l) for l in classes)))
        return
        print(mfmt.TableFormatter('').format(symmetric_group_character_table(3)))
        print('=' * 50)
        print(mfmt.TableFormatter('').format(symmetric_group_character_table(4)))
        weights, ct = symmetric_group_character_table(4, return_weights=True)
        weights = weights
        w_vec = np.sqrt(weights[np.newaxis, :] / np.sum(weights))
        wct = w_vec * ct
        print(mfmt.TableFormatter('').format(wct))
        print(np.round(wct @ wct.T, 6))
        sel = (0, 2, 3, 4)
        b2 = wct[:, sel]
        w2 = np.sqrt(weights[np.newaxis, sel] / np.sum(weights[sel,]))
        q, r = np.linalg.qr(b2.T)
        print(q.T / w2)
