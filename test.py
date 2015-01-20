#!/usr/bin/python
# many dependencies are all brought in with this import...
from libslideshow import *
from random import randrange


#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# indicate what display we are using...
#disptype = 'LVDS'
disptype = 'EEEpc'
disptype = 'mx28'

#imgtype = 'D90' # D90 camera image
#imgtype = 'disp' # horizontal 4-up composite image
imgtype = 'hd720' # 1280x720 image...

# set up display and image sizes for screen
if disptype == 'LVDS':
   size = (1024, 768) # LVDS display screen size
   if imgtype == 'D90': imagesz = (1152, 768) # LVDS image size, D90
   if imgtype == 'disp': imagesz = (1024, 698) # LVDS image size, composite
   if imgtype == 'hd720': imagesz = (1025, 576) # LVDS image size, hd720
if disptype == 'EEEpc':
   size = (1024, 600) # EEE pc screen size
   if imgtype == 'D90': imagesz = (900, 600) # EEE pc image size, D90
   if imgtype == 'disp': imagesz = (880, 600) # EEE pc image size, composite
   if imgtype == 'hd720': imagesz = (1025, 576) # LVDS image size, hd720
if disptype == 'mx28':
   size = (800, 480)
   if imgtype == 'D90': imagesz = (720, 480) # EEE pc image size, D90
   if imgtype == 'disp': imagesz = (704, 480) # EEE pc image size, composite
   if imgtype == 'hd720': imagesz = (800, 450) # LVDS image size, hd720

# determine the proper offset for a centered image, x and y...
imageloc = center_loc(size, imagesz) 

# initiate pygame and hide mouse..
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

# directory to pull image files from...
if imgtype=='disp': basefiles = '/root/share/for-display/'
if imgtype=='D90': basefiles = '/root/share/raw-images/'

# repeate forever, or at least until a quit event...
while (1):
		os.system('uvccapture -m -x1280 -y720 -obobo.jpg')
		displayimage (screen, 'bobo.jpg' , imagesz, imageloc )
		#time.sleep(.05)

		for event in pygame.event.get():
			if event.type == QUIT or event.key == K_q or event.key == K_ESCAPE:
				sys.exit()

