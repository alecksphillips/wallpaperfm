wallpaperfm
===========

[![Build Status](https://travis-ci.org/hugovk/wallpaperfm.png?branch=master)](https://travis-ci.org/hugovk/wallpaperfm) [![Coverage Status](https://coveralls.io/repos/hugovk/wallpaperfm/badge.png)](https://coveralls.io/r/hugovk/wallpaperfm)

Python script for generating wallpapers from Last.fm data.

Copyright (C) 2014  Alex Phillips (Email: alecks.phillips@gmail.com)

./wallpaper.py will display the instructions.

Please try to use the local option '-l' when possible to be kind to Last.fm's servers.
 
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
  - Updated for Last.fm API 2.0

Requirements:
---------------
* Tested on Python 2.6, 2.7, 3.2 or 3.3
* Python Imaging Library (not available for Python 3; 'Pillow' is a drop-in replacement)
* A Last.fm account and an active internet connection
* Last.fm API account (available for free [here] [7])

Install:
---------------
`pip install -r requirements.txt`

Album of Examples:
---------------
[Imgur] [8] - each captioned with the options required to generate that example.


v. 16 Jul 2013
---------------
- Consolidated [Roignac] [5] and [HelgeBS] [3]'s changes into one script
- Integer division no longer truncates as of Python 3.0, instead returning
  a float. Changed all instances of '/' used for integer division to '//',
  the floor division operator to better preserve functionality.
- Lots of formatting to try to conform to the Python Style Guide

v. 19 Jul 2013
--------------
- Updated for Last.fm API 2.0 (user can use their own API account)
- Fixed artist option


v. 08 Feb 2014
--------------
- Fixed gradient on albums in Collage not being applied on left and right borders.


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
  [7]: http://www.last.fm/api/account/create "here"
  [8]: http://imgur.com/a/Utr4W "Imgur"
