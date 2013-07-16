wallpaperfm
===========

Python script for generating wallpapers from last.fm data.

Copyright (C) 2013  Alex Phillips (Email: alecks.phillips@gmail.com)

./wallpaper.py will display the instructions.

Please try to use the local option '-l' when possible to be kind to last.fm's servers.
 
GPL
---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/> for more information


Changes to original script
--------------------------
  - Background Color (--BackgroundColor)
  - Image Type (--ImageType)
  - Use artist images instead of album covers (--Artist)
  - Rounding of image corners (--Radius)
  - Adapted for Python 3

Requirements:
---------------
* Python >3.0
* Python Imaging Library (Not available for Python 3; 'Pillow' is a drop-in replacement)
* a last.fm account and an active internet connection

v. 16 Jul 2013
---------------
- Consolidated [Roignac] [5] and [HelgeBS] [3]'s changes into one script
- Integer division no longer truncates as of Python 3.0, instead returning
  a float. Changed all instances of '/' used for integer division to '//',
  the floor division operator to better preserve functionality.
- Lots of formatting to try to conform to the Python Style Guide


Acknowledgements
----------------
Thanks to [Koant] [1] for his [original script] [2] and to
[HelgeBS] [3] for the addition of the background color and image type [options] [4],
and to [Roignac] [5] for the artist image and rounded corners [options] [6].

  [1]: http://www.lastfm.fr/user/Koant        "Koant"
  [2]: http://ledazibao.free.fr/wallpaperfm/index.php "original script"
  [3]: http://www.lastfm.fr/user/HelgeBS  "HelgeBS"
  [4]: https://content.wuala.com/contents/nanyouco/Images/last.fm/wallpaperfm.py?key=4DCLgHGLNI32 "options"
  [5]: http://www.lastfm.fr/user/Roignac    "Roignac"
  [6]: http://bazaar.launchpad.net/~roignac/+junk/wallpaperfm/files "options"
