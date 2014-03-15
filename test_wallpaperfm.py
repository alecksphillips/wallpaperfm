#!/usr/bin/env python
"""
Integration tests for wallpaperfm.py
"""
import os
import unittest
# import wallpaperfm  # Don't import, test via command line

class TestSequenceFunctions(unittest.TestCase):

    def remove_file(self, file):
        if os.path.isfile(file):
            os.remove(file)

    def setUp(self):
        self.username = "hvk"  # TODO enter a test username
        self.cmd = "./wallpaperfm.py -l -u " + self.username + " "

    def test_help(self):
        """ Test tiled albums """
        # Arrange
        cmd = "./wallpaperfm.py"

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

    def test_collage_albums(self):
        """ Test collage albums """
        # Arrange
        outfile = "test_collage"
        cmd = self.cmd + " -m collage -f " + outfile
        self.remove_file(outfile + ".png")
        self.assertFalse(os.path.isfile(outfile + ".png"))

        # Act
        print(cmd)
        os.system(cmd)

        # Assert
        self.assertTrue(os.path.isfile(outfile + ".png"))
#         self.remove_file(outfile + "png")

if __name__ == '__main__':
    unittest.main()

# End of file
