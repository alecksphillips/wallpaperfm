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
        cmd = COVERAGE_CMD + "./wallpaperfm.py --help"

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        # Should run with no exceptions
        # (Could check no image files exist)

    def helper_run_and_assert_file(self, outfile, args):
        # Arrange
        cmd = self.cmd + " " + args + " -f " + outfile
        self.remove_file(outfile + ".png")
        self.assertFalse(os.path.isfile(outfile + ".png"))

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        self.assertTrue(os.path.isfile(outfile + ".png"))

    def test_tiled_albums(self):
        """ Test tiled albums """
        # Arrange
        outfile = "out_tiled"
        args = " -m tile  --AlbumSize 120 --Interspace 4 "

        # Act/Assert
        self.helper_run_and_assert_file(outfile, args)

    def test_glass_albums(self):
        """ Test glassy albums """
        # Arrange
        outfile = "out_glass"
        args = " -m glass --AlbumNumber 8 --EndPoint 80 --Offset 30 "

        # Act/Assert
        self.helper_run_and_assert_file(outfile, args)

    def test_collage_albums(self):
        """ Test collage albums """
        # Arrange
        outfile = "out_collage"
        args = (
            " -m collage --AlbumSize 200 --AlbumOpacity 85 "
            " --AlbumNumber 60 --GradientSize 20 --Passes 3 ")

        # Act/Assert
        self.helper_run_and_assert_file(outfile, args)

if __name__ == '__main__':
    if len(COVERAGE_CMD):
        os.system("coverage erase")
    unittest.main()

# End of file
