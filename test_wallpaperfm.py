#!/usr/bin/env python
"""
Integration tests for wallpaperfm.py
"""
import os
import unittest

try:
    import coverage
    coverable = True
except ImportError:
    coverable = False


class TestSequenceFunctions(unittest.TestCase):

    def remove_file(self, file):
        if os.path.isfile(file):
            os.remove(file)

    def setUp(self):
        self.username = "RJ"
        self.cmd = "./wallpaperfm.py --Local -u " + self.username + " "
        if coverable:
            self.cmd = "coverage run -a " + self.cmd

    def test_help(self):
        """ Test tiled albums """
        # Arrange
        cmd = "./wallpaperfm.py"
        if coverable:
            cmd = "coverage run -a " + cmd

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        # Should run with no exceptions
        # (Could check no image files exist)

    def test_tiled_albums(self):
        """ Test tiled albums """
        # Arrange
        outfile = "test_tiled"
        cmd = self.cmd + " -m tile -f " + outfile
        self.remove_file(outfile + ".png")
        self.assertFalse(os.path.isfile(outfile + ".png"))

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        self.assertTrue(os.path.isfile(outfile + ".png"))

    def test_glass_albums(self):
        """ Test tiled albums """
        # Arrange
        outfile = "test_glass"
        cmd = self.cmd + " -m glass -f " + outfile
        self.remove_file(outfile + ".png")
        self.assertFalse(os.path.isfile(outfile + ".png"))

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        self.assertTrue(os.path.isfile(outfile + ".png"))

if __name__ == '__main__':
    if coverable:
        os.system("coverage erase")
    unittest.main()

# End of file
