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


if os.name == "nt":
    OS_CMD = ""
else:
    OS_CMD = " ./"


class TestSequenceFunctions(unittest.TestCase):

    def remove_file(self, file):
        if os.path.isfile(file):
            os.remove(file)

    def mkdir(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    def setUp(self):
        self.username = "RJ"
        self.mkdir("my_cache")
        self.cmd = (
            COVERAGE_CMD + OS_CMD +
            "wallpaperfm.py --Cache my_cache "
            "--Local -u " + self.username + " ")

    def helper_run(self, args):
        # Arrange
        cmd = COVERAGE_CMD + OS_CMD + "wallpaperfm.py " + args

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        # Should run with no exceptions
        # (Could run with subprocess.Popen() and check output)

    def test_help(self):
        """ Test usage with help option """
        # Arrange
        args = " --help"

        # Act/Assert
        self.helper_run(args)

    def test_no_options(self):
        """ Test usage with no options """
        # Arrange
        args = ""

        # Act/Assert
        self.helper_run(args)

    def test_unknown_option(self):
        """ Test usage with unknown options """
        # Arrange
        args = " --someunknownoption"

        # Act/Assert
        self.helper_run(args)

    def test_unknown_mode(self):
        """ Test usage with unknown mode """
        # Arrange
        args = " --Mode superduperanimated"

        # Act/Assert
        self.helper_run(args)

    def helper_run_and_assert_file(self, args, outfile, ext=".png"):
        # Arrange
        cmd = self.cmd + " " + args + " -f " + outfile
        self.remove_file(outfile + ext)
        self.assertFalse(os.path.isfile(outfile + ext))

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        self.assertTrue(os.path.isfile(outfile + ext))

    def test_tiled_albums(self):
        """ Test tiled albums """
        # Arrange
        outfile = "out_tiled"
        args = " -m tile --AlbumSize 120 --Interspace 4 --FinalOpacity 40"

        # Act/Assert
        self.helper_run_and_assert_file(args, outfile)

    def test_default_username(self):
        """ Test tiled albums """
        # Arrange
        cmd = self.cmd + " -m tile"  # no outfile given
        outfile = "RJ.png"
        self.remove_file(outfile)
        self.assertFalse(os.path.isfile(outfile))

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        self.assertTrue(os.path.isfile(outfile))

    def test_tiled_albums_jpg(self):
        """ Test tiled albums """
        # Arrange
        outfile = "out_tiled_jpg"
        args = " -m tile --ImageType jpg --BackgroundColor red --Radius 25"

        # Act/Assert
        self.helper_run_and_assert_file(args, outfile, ext=".jpg")

    def test_glass_albums(self):
        """ Test glassy albums """
        # Arrange
        outfile = "out_glass"
        args = (
            " -m glass --AlbumNumber 8 --EndPoint 80 --Offset 30 "
            " --ImageSize 1920x1080 --CanvasSize 1900x1900 --Past 12month "
            " -x http://images.amazon.com/images/P/B00001ZTYQ.01._SCMZZZZZ "
            )

        # Act/Assert
        self.helper_run_and_assert_file(args, outfile)

    def test_collage_albums(self):
        """ Test collage albums """
        # Arrange
        outfile = "out_collage"
        args = (
            " -m collage --AlbumSize 200 --AlbumOpacity 85 "
            " --AlbumNumber 60 --GradientSize 20 --Passes 3 ")

        # Act/Assert
        self.helper_run_and_assert_file(args, outfile)


if __name__ == '__main__':
    if len(COVERAGE_CMD):
        os.system("coverage erase")
    unittest.main()

# End of file
