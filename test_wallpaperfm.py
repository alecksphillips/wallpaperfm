#!/usr/bin/env python
"""
Integration tests for wallpaperfm.py
"""
import os
import unittest

import imp
try:
    imp.find_module("coverage")
    COVERAGE_CMD = "coverage run --append --source wallpaperfm.py "
except ImportError:
    COVERAGE_CMD = ""


class TestSequenceFunctions(unittest.TestCase):

    def remove_file(self, file):
        if os.path.isfile(file):
            os.remove(file)

    def setUp(self):
        self.username = "RJ"
        self.cmd = (
            COVERAGE_CMD +
            "./wallpaperfm.py --Local -u " + self.username + " ")

    def test_help(self):
        """ Test usage with no options """
        # Arrange
        cmd = COVERAGE_CMD + "./wallpaperfm.py"

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
        """ Test glassy albums """
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
    if len(COVERAGE_CMD):
        os.system("coverage erase")
    unittest.main()

# End of file
