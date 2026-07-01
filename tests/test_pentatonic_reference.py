import unittest

from pentatonic_reference import get_pentatonic_reference


class PentatonicReferenceTests(unittest.TestCase):
    def test_set_77_gets_octatonic_parent_label(self):
        refs = get_pentatonic_reference([0, 1, 4, 7, 9])
        self.assertIn('OCT 0,1 Pentatonic Subset', refs)

    def test_non_octatonic_set_does_not_get_octatonic_label(self):
        refs = get_pentatonic_reference([0, 2, 4, 7, 9])
        self.assertNotIn('OCT 0,1 Pentatonic Subset', refs)


if __name__ == '__main__':
    unittest.main()
