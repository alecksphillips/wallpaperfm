#!/usr/bin/env python
#
# Wallpaperfm.py is a python script that generates desktop wallpapers from your
# last.fm music profile.
# Copyright (C) 2014  Alex Phillips
#

#########################
# GPL Information
#########################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <http://www.gnu.org/licenses/> for more information
#
#########################

#Original script by Koant, http://www.last.fm/user/Koant
#    http://ledazibao.free.fr/wallpaperfm/index.php
#
#Background color, image type by HelgeBS, http://www.last.fm/user/HelgeBS
#    https://content.wuala.com/contents/nanyouco/Images/last.fm/wallpaperfm.py?key=4DCLgHGLNI32
#
#Artist images, rounded corners by nick (xmpp:nick@jabbim.org.ru)
#    and Vadim Rutkovsky (roignac@gmail.com)
#    http://bazaar.launchpad.net/~roignac/+junk/wallpaperfm/files
#
#Adapted for Python 3 and last.fm api 2.0, consolidated into one
#script and general cleanup
#    by aleckphillips (http://www.last.fm/user/alecksphillips)
#
#Changes to original script:
#  - Background Color (--BackgroundColor)
#  - Image Type (--ImageType)
#  - Use artist images instead of album covers (--Artist)
#  - Rounding of image corners (--Radius)
#
# ./wallpaper.py will display the instructions
#
# Requirements:
# . Python Imaging Library (probably already installed, available through
#   synaptic for Ubuntu users)
# . for Python 3, use 'Pillow', a drop-in replacement for PIL
# . a last.fm account and an active internet connectionopengl python3
#
# v. 16 Jul 2013
#  - Integer division no longer truncates as of Python 3.0, instead returning
#    a float. Changed all instances of '/' used for integer division to '//',
#    the floor division operator to better preserve functionality.
#
# v. 19 Jul 2013
#  - Changed getAlbumCovers to match last.fm api 2.0 including use of api key
#    User is encouraged to user their own key if they wish which can be
#    obtained with an api account (http://www.last.fm/api/account/create).
#
# v. 08 Feb 2014
#  - Edited makeCollageMask to remove hard edges on left and right borders of
#    albums.

__author__ = 'Alex Phillips (alecks.phillips@gmail.com)'
__version__ = '$ 19 Jul 2013 $'
__date__ = '$ Date: 2013/07/19 $'
__copyright__ = 'Copyright (c) 2013 Alex Phillips'
__license__ = 'GPL'


#Key for last.fm api - change to your own personal key
api_key='8cf8b8f0778a606621666c2152df79db'


try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from xml.dom import minidom
import os.path
import sys
from getopt import getopt
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops

from PIL import ImageFilter
from PIL import ImageOps

def usage():
    print("Quick examples")
    print("--------------")
    print("./wallpaperfm.py -m tile -u your_lastfm_username")
    print("    will generate an image with your favourite albums tiled up in "
          "a random order.\n")
    print("./wallpaperfm.py -m glass -u your_lastfm_username")
    print("    will generate an image with a few random albums, with a glassy"
          " effect.\n")
    print("./wallpaperfm.py -m collage -u your_lastfm_username")
    print("    will generate a random collage of your favorite albums.\n")
    print("./wallpaperfm.py -m photo -u your_lastfm_username")
    print("    will generate a random scattering of your favorite albums.\n")
    print("--------------")

    print("\nGlobal switches:")
    print("-u, --Username: your last.fm username.")
    print("-f, --Filename: the filename where the image will be saved. "
          "Username by default.")
    print("-t, --Past: [overall] how far back should the profile go.")
    print("        One of 3month, 6month, 12month or overall.")
    print("-O, --FinalOpacity: [80] darkness of the final image. from 0 to 100")
    print("-C, --BackgroundColor: [#000000] background color ('#' must be "
                "escaped)")
    print("-T, --ImageType: [png] destination image format\n" +
          "        (if png alpha will be used instead of colored background)")
    print("-i, --ImageSize: [1280x1024] size of the final image. "
                "Format: numberxnumber")
    print("-c, --CanvasSize: size of the canvas. = image size by default.")
    print("-e, --Cache: [wpcache] path to the cache.")
    print("-x, --ExcludedList: ['http://cdn.last.fm/depth/catalogue"
                "/noimage/cover_med.gif']")
    print("        excluded urls, comma separated.")
    print("-l, --Local: use a local copy of the charts.")
    print("        Ideal for using it offline or being kind to the "
                "last.fm servers.")
    print("-A, --Artist: use artist images instead of album covers.")
    print("-R, --Radius: [20] radius of corner rounding for images, no "
                "rounding by default")

    print("\nSpecific switches for the 'tile' mode (-m tile):")
    print("-a, --AlbumSize: [130] size of the albums, in pixel.")
    print("-s, --Interspace: [5]  space between in tile, in pixel.")

    print("\nSpecific switches for the 'glass' mode (-m glass):")
    print("-n, --AlbumNumber: [7] number of albums to show.")
    print("-d, --EndPoint: [75] where the reflection ends, in percentage of "
                "the album size.")
    print("-r, --Offset: [40] starting value of opacity for the shadow.")

    print("\nSpecific switches for the 'collage' mode (-m collage):")
    print("-a, --AlbumSize: [300] size of the albums, in pixel.")
    print("-o, --AlbumOpacity: [90] maximum opacity of each album, from 0 to "
                "100.")
    print("-n, --AlbumNumber: [50] number of albums to show.")
    print("-g, --GradientSize: [15] portion of the album in the gradient, "
                "from 0 to 100")
    print("-p, --Passes: [4] number of iterations of the algorithms.")
    print("\nSpecific switches for the 'photo' mode (-m photo):")
    print("-a, --AlbumSize: [250] size of the albums, in pixel.")
    print("-n, --AlbumNumber: [20] number of albums to show.")
    sys.exit()

def getSize(s):
    """ Turns '300x400' to (300,400) """
    return tuple([int(item) for item in s.rsplit('x')])

def getParameters():
    """ Get Parameters from the command line or display usage in case of
        problem """
    # Common Default Parameters
    Filename=''
    mode='tile'

    Profile=dict()
    Profile['Username']='Koant'
    Profile['Past']='overall'
    Profile['cache']='wpcache'
    Profile['ExcludedList']=['http://cdn.last.fm/depth/catalogue/noimage/cover_med.gif',
                             'http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png',
                             'http://userserve-ak.last.fm/serve/174s/32868291.png']
    Profile['Limit']=50
    Profile['Local']='no'
    Profile['Artist']='no'

    Common=dict();
    Common['ImageSize']=(1280,1024)
    Common['CanvasSize']=''
    Common['FinalOpacity']=80
    Common['ImageType']='png'
    Common['BgColor']=0
    Common['Radius']=20

    ## Specific Default Parameters
    # Collage
    Collage=dict();
    Collage['Passes']=4
    Collage['AlbumOpacity']=90
    Collage['GradientSize']=15
    Collage['AlbumSize']=250

    # Tile
    Tile=dict()
    Tile['AlbumSize']=130
    Tile['Interspace']=5

    # Glass
    Glass=dict()
    Glass['AlbumNumber']=7
    Glass['Offset']=40
    Glass['EndPoint']=75

    # Photo
    Photo=dict()
    Photo['AlbumNumber']=10
    Photo['AlbumSize']=250

    try:
        optlist, args=getopt(sys.argv[1:], 'hu:t:n:c:f:a:o:g:O:i:m:p:s:e:d:r:x:lAT:C:R:',
                             ["help", "Mode=", "Username=", "Past=",
                              "Filename=","CanvasSize=", "ImageSize=",
                              "FinalOpacity=","AlbumSize=","AlbumOpacity=",
                              "GradientSize=","Passes=","AlbumNumber=",
                              "Interspace=","Cache=","Offset=","EndPoint=",
                              "ExcludedList=","Local","Artist","ImageType=",
                              "BackgroundColor=","Radius="])
    except Exception as err:
        print("#"*20)
        print(str(err))
        print("#"*20)
        usage()
        
    if len(optlist)==0:
        usage()
        
    for option, value in optlist:
        if option in ('-h','--help'):
            usage()
            
        elif option in ('-m','--Mode'):     # m: mode; Tile, Glass, Collage or Photo
            mode=value.lower()

        elif option in('-e','--Cache'):     # e: cache
            Profile['cache']=value

        elif option in('-l','--Local'):     # l: use a local copy of the charts
            Profile['Local']='yes'

        elif option in ('-A','--Artist'):   # A: use artist images
            Profile['Artist']='yes'

        elif option in ('-u','--Username'): # u: username (Common)
            Profile['Username']=value

        elif option in ('-t','--Past'):     # t: how far back (Common),
            Profile['Past']=value           #either 3month,6month or 12month

        elif option in ('-x','--ExcludedList'):            # x: excluded url
            Profile['ExcludedList'].extend(value.rsplit(','))

        elif option in ('-f', '--Filename'): # f: image filename (Common)
            Filename=value

        elif option in ('-c','--CanvasSize'):# c: canvas size (Common)
            Common['CanvasSize']=getSize(value)

        elif option in ('-i','--ImageSize'): # i: image size (Common)
            Common['ImageSize']=getSize(value)

        elif option in ('-T','--ImageType'): # T: image type (Common)
            Common['ImageType']=value

        elif option in ('-O', '--FinalOpacity'): # O: opacity of final image (Common)
            Common['FinalOpacity']=int(value)

        elif option in ('-C', '--BackgroundColor'): # C: inital image background color (Common)
            Common['BgColor']=value

        elif option in ('-R','--Radius'):    # R: images have rounded corners
            Common['Radius']=int(value)

        elif option in ('-a','--AlbumSize'): # a: album size (Collage, Tile, Photo)
            Collage['AlbumSize']=int(value)
            Tile['AlbumSize']=int(value)
            Photo['AlbumSize']=int(value)

        elif option in ('-o','--AlbumOpacity'):    # o: album opacity (Collage)
            Collage['AlbumOpacity']=int(value)

        elif option in ('-g','--GradientSize'):    # g: gradient size (Collage)
            Collage['GradientSize']=int(value)

        elif option in ('-p','--Passes'):    # p: number of passes (Collage)
            Collage['Passes']=int(value)

        elif option in ('-n','--AlbumNumber'): # n: number of albums (Glass, Collage, Photo)
            Glass['AlbumNumber']=int(value)
            Collage['AlbumNumber']=int(value)
            Photo['AlbumNumber']=int(value)

        elif option in ('-s','--Interspace'):  # s: interspace (Tile)
            Tile['Interspace']=int(value)

        elif option in ('-d','--EndPoint'):    # d: EndPoint (Glass)
            Glass['EndPoint']=int(value)

        elif option in ('-r','--Offset'):      # r: Offset (Glass)
            Glass['Offset']=int(value)


        else:
            print("I'm not using ", option)

    if Filename=='': # by default, Filename=Username
        Filename=Profile['Username']
    if Common['CanvasSize']=='':    # by default, CanvasSize=ImageName
        Common['CanvasSize']=Common['ImageSize']

    # Add the common parameters
    for k,v in Common.items():
        Collage[k]=v
        Tile[k]=v
        Glass[k]=v
        Photo[k]=v

    return {'Filename':Filename, 'Mode':mode, 'Profile':Profile, 'Tile':Tile,
            'Glass':Glass, 'Collage':Collage, 'Photo':Photo, 'ImageType':Common['ImageType']}

##############################
## Parse and download the files
##############################
def makeFilename(url):
    """ Turns the url into a filename by replacing possibly annoying
        characters by _ """
    url=url[7:] # remove 'http://'
    for c in ['/', ':', '?', '#', '&','%']:
        url=url.replace(c,'_')
    return url

def download(url,filename):
    """ download the binary file at url """
    instream=urlopen(url)
    outfile=open(filename,'wb')
    for chunk in instream:
        outfile.write(chunk)
    instream.close()
    outfile.close()

def IsImageFile(imfile):
    """ Make sure the file is an image, and not a 404. """
    flag=True
    try:
        i=Image.open(imfile)
    except Exception as err:
        flag=False
    return flag

def getAlbumCovers(Username='Koant',Past='overall',cache='wp_cache',
                   ExcludedList=['http://cdn.last.fm/depth/catalogue/noimage/cover_med.gif',
                                 'http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png'],
                   Limit=50,Local='no',Artist='no'):
    """ download album covers if necessary """
    ## Preparing the file list.
    if Past in ('3month','6month','12month'):
        tpe='&type='+Past
    else:
        tpe=''

    if Artist=="yes":
        url=('http://ws.audioscrobbler.com/2.0/?method=user.getTopArtists&user='+Username+
         '&api_key='+api_key+'&limit='+str(Limit)+tpe)
        tagname='artist'
    else:
        url=('http://ws.audioscrobbler.com/2.0/?method=user.getTopAlbums&user='+Username+
         '&api_key='+api_key+'&limit='+str(Limit)+tpe)
        tagname='album'

    # make cache if doesn't exist
    if not os.path.exists(cache):
        print("cache directory ("+cache+") doesn't exist. I'm creating it.")
        os.mkdir(cache)

    # Make a local copy of the charts
    local_copy = cache+os.sep+tagname+'_charts_'+Username+'.xml'
    if Local=='no' or (Local=='yes' and not os.path.isfile(local_copy)):
        try:
            print("Downloading from ",url)
            download(url, local_copy)
        except Exception as err:
            print("#"*20)
            print("I couldn't download the profile or make a local copy of it.")
            print("#"*20)
    else:
        print("Reading from local copy:  ",local_copy)

    # Parse image filenames
    print("Parsing...")
    try:
        data=open(local_copy,'rb')
        xmldoc=minidom.parse(data)
        data.close()

    except Exception as err:
        print('#'*20)
        print("Error while parsing your profile. Your username might be "
              "misspelt or your charts empty.")
        print('#'*20)
        sys.exit()

    filelist=[]
    for item in xmldoc.getElementsByTagName(tagname):
        file = item.getElementsByTagName('image')[3].firstChild
        if file is not None:
            filelist.append(file.nodeValue)

    # Exclude covers from the ExcludedList
    filelist=[item for item in filelist if not item in ExcludedList]

    # Stop if charts are empty
    if len(filelist)==0:
        print('#'*20)
        print("Your charts are empty. I can't proceed.")
        print('#'*20)
        sys.exit()

    # download covers only if not available in the cache
    for imfile in filelist[:]:
        url=imfile
        imfile=makeFilename(imfile)
        if not os.path.exists(cache+os.sep+imfile):
            print("    Downloading ",url)
            download(url,cache+os.sep+imfile)

    filelist=[cache+os.sep+makeFilename(imfile) for imfile in filelist]

    # Checks the file is indeed an image
    filelist=[imfile for imfile in filelist if IsImageFile(imfile)]

    filelist.reverse() # changed on 02Aug2010
    return filelist

##############################
## Common
##############################
CROSS                = 'Cross'
ROUNDED              = 'Rounded'
SQUARE               = 'Square'
CORNERS              = [ROUNDED,SQUARE,CROSS]
CORNER_ID            = 'rounded_corner_r%d_f%d'
CROSS_POS            = (CROSS,CROSS,CROSS,CROSS)
ROUNDED_POS          = (ROUNDED,ROUNDED,ROUNDED,ROUNDED)
ROUNDED_RECTANGLE_ID = 'rounded_rectangle_r%d_f%d_s1%d_s2%d_p1%s_p2%s_p3%s_p4%s'

def round_image(image,radius=100,back_colour='#FFFFFF'):
    fill = 255
    mask    = create_rounded_rectangle(image.size,radius,fill)
    image.paste(Image.new('RGB',image.size,back_colour),(0,0),
                ImageChops.invert(mask))
    image.putalpha(mask)
    return image

def create_corner(radius=100,fill=255,factor=2):
    corner  = Image.new('L',(factor*radius,factor*radius),0)
    draw    = ImageDraw.Draw(corner)
    draw.pieslice((0,0,2*factor*radius,2*factor*radius),180,270,fill=fill)
    corner  = corner.resize((radius,radius),Image.ANTIALIAS)
    return corner

def create_rounded_rectangle(size=(600,400),radius=100,fill=255):
    #rounded_rectangle
    im_x, im_y  = size
    cross = Image.new('L',size,0)
    draw    = ImageDraw.Draw(cross)
    draw.rectangle((radius,0,im_x-radius,im_y),fill=fill)
    draw.rectangle((0,radius,im_x,im_y-radius),fill=fill)

    corner  = create_corner(radius,fill)
    #rounded rectangle
    rectangle   = Image.new('L',(radius,radius),255)
    rounded_rectangle   = cross.copy()
    pos = ROUNDED_POS
    for index, angle in enumerate(pos):
        if angle == CROSS:
            break
        if angle == ROUNDED:
            element = corner
        else:
            element = rectangle
        if index%2:
            x       = im_x-radius
            element = element.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            x       = 0
        if index < 2:
            y       = 0
        else:
            y       = im_y-radius
            element = element.transpose(Image.FLIP_TOP_BOTTOM)
        rounded_rectangle.paste(element,(x,y))
    return rounded_rectangle

##############################
## Tile
##############################
def Tile(Profile,ImageSize=(1280,1024),CanvasSize=(1280,1024),AlbumSize=130,
         FinalOpacity=30,Interspace=5,ImageType='png',BgColor=0,Radius=20):
    """ produce a tiling of albums covers """

    imagex,imagey=ImageSize
    canvasx,canvasy=CanvasSize

    offsetx=(imagex-canvasx)//2
    offsety=(imagey-canvasy)//2

    #number of albums on rows and columns
    #using round() brings albums to edge of canvas
    nx=int(round((canvasx-Interspace)/(AlbumSize+Interspace)))
    ny=int(round((canvasy-Interspace)/(AlbumSize+Interspace)))

    # number of images to download
    # some extra in case of 404 , even though there shouldn't be any really.
    Profile['Limit']=ny*nx+len(Profile['ExcludedList'])+5

    # download images
    filelist=getAlbumCovers(**Profile)

    #background=Image.new('RGB',(imagex,imagey),0) #original code
    background=getBG(ImageSize,ImageType,BgColor) #colour modification

    filelist2=list()
    posy=-AlbumSize+(canvasy-ny*(AlbumSize+Interspace)-Interspace)//2
    for j in range(0,ny):
        posx,posy=(-AlbumSize+(canvasx-nx*(AlbumSize+Interspace)-Interspace)//2,
                   posy+Interspace+AlbumSize) # location of album in the canvas
        for i in range(0,nx):
            posx=posx+Interspace+AlbumSize
            if len(filelist2)==0: # better than random.choice()
                #(minimises risk of doubles and goes through the whole list)

                filelist2=list(filelist)
                random.shuffle(filelist2)
            imfile=filelist2.pop()
            try:
                im=Image.open(imfile).convert('RGB')
            except Exception as err:
                print("#"*20)
                print(err)
                print("I couln't read that file: "+imfile)
                print("You might want to exclude its corresponding URL with"
                      " -x because it probably\n doesn't point to an image.")
                print("#"*20)
                sys.exit()
            im=im.resize((AlbumSize,AlbumSize),2)

            #Round corners
            if Radius != 0:
                im = round_image(im,Radius,BgColor)
            background.paste(im,(posx+offsetx,posy+offsety))

    # darken the result

    #background=background.point(laopengl python3mbda i: FinalOpacity*i/100) #original
    if FinalOpacity<100:
        background=Image.blend(getBG(ImageSize,ImageType,BgColor), background,
                               FinalOpacity/100.0)

    return background

##############################
## Glassy wallpaper
##############################
def makeGlassMask(ImageSize,Offset=50,EndPoint=75):
    """ Make mask for the glassy wallpaper """
    mask=Image.new('L',ImageSize,0)
    di=ImageDraw.Draw(mask)
    sizex,sizey=ImageSize

    stop=min((EndPoint*sizey)//100,sizey)
    #E=EndPoint*sizey//100
    #O=255*Offset//100
    for i in range(0,stop):
        color=(255*Offset//100*-100*i)//(EndPoint*sizey)+255*Offset//100 #linear gradient
        #color=((i-E)*(i-E)*O)//(E*E) # quadratic gradient
        #color=(O*(E*E-i*i))//(E*E)
        di.line((0,i,sizex,i),color)
    return mask

def Glass(Profile, ImageSize=(1280,1024),CanvasSize=(1280,1024),AlbumNumber=7,
          FinalOpacity=100,Offset=50,EndPoint=75,ImageType='png',BgColor=0,
          Radius=20):
    """ Make a glassy wallpaper from album covers """

    if AlbumNumber>Profile['Limit']:
        Profile['Limit']=AlbumNumber+len(Profile['ExcludedList'])+5

    filelist=getAlbumCovers(**Profile)
    imagex,imagey=ImageSize

    canvasx,canvasy=CanvasSize

    offsetx=(imagex-canvasx)//2
    offsety=(imagey-canvasy)//2

    #background=Image.new('RGB',(imagex,imagey),0) # background original
    background=getBG(ImageSize,ImageType,BgColor) #colour modification

    albumsize=canvasx//AlbumNumber
    mask=makeGlassMask((albumsize,albumsize),Offset,EndPoint)

    posx=(canvasx-AlbumNumber*albumsize)//2-albumsize

    for i in range(0,AlbumNumber):
        imfile=filelist.pop() # assumes there are enough albums in the filelist
        tmpfile=Image.open(imfile).convert('RGB')
        tmpfile=tmpfile.resize((albumsize,albumsize),2) # make it square
        posx,posy=(posx+albumsize,canvasy//2-albumsize)

        #Round corners
        if Radius != 0:
                tmpfile = round_image(tmpfile,Radius,BgColor)

        background.paste(tmpfile,(posx+offsetx,posy+offsety)) #paste albm cover
        tmpfile=tmpfile.transpose(1)                #turn it upside down

        # apply mask and paste
        background.paste(tmpfile,(posx+offsetx,
                                  canvasy//2+offsety),mask)

    # darken the result
    if FinalOpacity<100:
        background=Image.blend(getBG(ImageSize,ImageType,BgColor), background,
                               FinalOpacity/100.0)


    return background

############################
## Collage
############################
def erfc(x):
    """ approximate erfc with a few splines """
    if x<-2:
        return 2;
    elif (-2<=x) and (x<-1):
        c=[ 0.9040,   -1.5927,   -0.7846,   -0.1305];
    elif (-1<=x) and (x<0):
        c=[1.0000, -1.1284,   -0.1438,    0.1419];
    elif (0<=x) and (x<1):
        c=[1.0000,   -1.1284 ,   0.1438,    0.1419];
    elif (1<=x) and (x<2):
        c=[1.0960,   -1.5927,    0.7846 ,  -0.1305];
    else:
        return 0;
    return c[0]+c[1]*x+c[2]*x*x+c[3]*x*x*x;

def makeCollageMask(size,transparency,gradientsize):
    mask=Image.new('L',size,0)
    sizex,sizey=size
    l=(gradientsize*sizex)//100
    c=(255*transparency)//100.0
    c=c/4.0 # 4=normalizing constant from convolution
    s2=1/(l*1.4142)
    for i in range(sizex):

        #edited to remove hard edges on left and right borders of each album
        foo1=(erfc(s2*(l-i))-erfc(s2*(sizey-l-i))) #saving computation

        for j in range(sizey):

            foo2=(erfc(s2*(l-j))-erfc(s2*(sizex-l-j))) #saving computation

            v=c*foo1*foo2

            mask.putpixel((i,j),int(v))

    return mask

def Collage(Profile,ImageSize=(1280,1024),CanvasSize=(1280,1024),
            AlbumNumber=50,AlbumSize=300,GradientSize=20,AlbumOpacity=70,
            Passes=4,FinalOpacity=70,ImageType='png',BgColor=0,Radius=0):

    """ make a collage of album covers """

    Profile['Limit']=min(200,max(AlbumNumber,Profile['Limit']))

    filelist=getAlbumCovers(**Profile)

    imagex,imagey=ImageSize
    canvasx,canvasy=CanvasSize

    colorbg=getBG(ImageSize,ImageType,BgColor)
    background=Image.new(colorbg.mode,(imagex,imagey),0) # background
    mask=makeCollageMask((AlbumSize,AlbumSize),AlbumOpacity,GradientSize)
    print("Computing the collage...")
    for p in range(0,Passes):
        print("Pass ",p+1," of ",Passes)
        for imfile in filelist:
                tmpfile=Image.open(imfile).convert('RGB')
                tmpfile=tmpfile.resize((AlbumSize,AlbumSize),1)
                posx=random.randint(0,canvasx-AlbumSize)
                posy=random.randint(0,canvasy-AlbumSize)

                #Round corners
                if Radius != 0:
                    tmpfile = round_image(tmpfile,Radius,BgColor)    

                background.paste(tmpfile,(posx+(imagex-canvasx)//2,
                                          posy+(imagey-canvasy)//2), mask)

    # darken the result
    if FinalOpacity<100:
        background=Image.blend(colorbg,background,FinalOpacity/100.0)

    return background

##############################
## Photo
##############################
def Photo(Profile,ImageSize=(1280,1024),CanvasSize=(1280,1024),AlbumSize=250,AlbumNumber=10,
         FinalOpacity=30,ImageType='png',BgColor=0,Radius=20):
    """ produce a random scattering of album covers """

    imagex,imagey=ImageSize
    canvasx,canvasy=CanvasSize

    offsetx=(imagex-canvasx)//2
    offsety=(imagey-canvasy)//2

    Profile['Limit']=AlbumNumber+len(Profile['ExcludedList'])+5

    # download images
    filelist=getAlbumCovers(**Profile)

    #background=Image.new('RGB',(imagex,imagey),0) #original code
    background=getBG(ImageSize,ImageType,BgColor) #colour modification
    
    #Load image resources
    mask = Image.open("resources/mask.png").convert('RGBA').resize((AlbumSize,AlbumSize),1)
    white = Image.open("resources/white.png").convert('RGBA').resize((AlbumSize,AlbumSize),1)
    black = Image.open("resources/black.png").convert('RGBA').resize((AlbumSize,AlbumSize),1)
    alpha = Image.open("resources/alpha.png").convert('RGBA').resize((AlbumSize+2,AlbumSize+2),1)
    
    shadowOffset = AlbumSize/100
    
    blackMask=getBG((AlbumSize,AlbumSize),'png',(128,128,128))
    
    #Round corners
    if Radius !=0:
        black = round_image(black,Radius,BgColor)
        blackMask = round_image(blackMask,Radius,BgColor)
        alpha = round_image(alpha,Radius+1,BgColor)

    #Include 1 pixel border of alpha to reduce jaggys when rotating
    alpha1 = alpha.copy()
    alpha2 = alpha.copy()
    alpha1.paste(black, (1,1), black)
    alpha2.paste(blackMask, (1,1), blackMask)

    for i in range(0,AlbumNumber-1):
        imfile=filelist.pop() # assumes there are enough albums in the filelist
        tmpfile=Image.open(imfile).convert('RGBA')
        tmpfile=tmpfile.resize((AlbumSize,AlbumSize),1)
        posx=random.randint(0,canvasx-AlbumSize)
        posy=random.randint(0,canvasy-AlbumSize)
        
        #Add highlight for depth
        tmpfile.paste(white,(0,0),mask)

        #Round corners
        if Radius != 0:
            tmpfile = round_image(tmpfile,Radius,BgColor)
        
        #Random rotation up to 45 degrees left or right
        angle = int(random.gauss(0,15))
        
        #Jaggy reduction again
        alpha3=alpha.copy()
        alpha3.paste(tmpfile, (1,1), tmpfile)
        
        #Rotate the album, the shadow and the mask for the shadow
        tmpfile = alpha3.rotate(angle,resample=Image.BICUBIC,expand=1)
        shadow = alpha1.rotate(angle,resample=Image.BICUBIC,expand=1)
        shadowMask = alpha2.rotate(angle,resample=Image.BICUBIC,expand=1)
        
        #Paste the shadow using mask, paste the album cover
        background.paste(shadow, (posx+offsetx-shadowOffset,posy+offsety+shadowOffset), shadowMask)
        background.paste(tmpfile,(posx+offsetx,posy+offsety),tmpfile)

    # darken the result

    #background=background.point(lambda i: FinalOpacity*i/100) #original
    if FinalOpacity<100:
        background=Image.blend(getBG(ImageSize,ImageType,BgColor), background,
                               FinalOpacity/100.0)

    return background

#########################
#background gen from wallpaperfm-colour
#########################
def getBG(ImageSize=(1280,1024),ImageType='png',BgColor=0):
    imagex,imagey=ImageSize
    if ImageType=='png':
        return Image.new('RGBA',(imagex,imagey),None)
    else:
        return Image.new('RGB',(imagex,imagey),BgColor)

########################
## main
########################
def main():
    print("")
    print("Wallpaperfm.py is a python script that generates desktop wallpapers"
          " from your\n    last.fm musical profile.")
    print(" Original script by Koant, http://www.last.fm/user/Koant")
    print(" This version by alecksphillips, "
            "http://www.last.fm/user/alecksphillips")
    print("")
    param=getParameters()


    print("Mode: "+param['Mode'])
    print(" Image will be saved as "+param['Filename']+"."+param['ImageType'])

    if param['Mode']=='tile':
        for k,v in param['Tile'].items():
            print("    "+k+": "+str(v))
        image=Tile(param['Profile'],**param['Tile'])
    elif param['Mode']=='glass':
        for k,v in param['Glass'].items():
            print("    "+k+": "+str(v))
        image=Glass(param['Profile'],**param['Glass'])
    elif param['Mode']=='collage':
        for k,v in param['Collage'].items():
            print("    "+k+": "+str(v))
        image=Collage(param['Profile'],**param['Collage'])
    elif param['Mode']=='photo':
        for k,v in param['Photo'].items():
            print("    "+k+": "+str(v))
        image=Photo(param['Profile'],**param['Photo'])
    else:
        print(" I don't know this mode: ", param['Mode'])
        sys.exit()

    image.save(param['Filename']+"."+param['ImageType'])
    print(" Image saved as "+param['Filename']+"."+param['ImageType'])

if __name__=="__main__":
    main()
