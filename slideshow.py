#!/usr/bin/python
# many dependencies are all brought in with this import...
from libslideshow import *
from random import randrange


#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# indicate what display we are using...
disptype = 'LVDS'
#disptype = 'EEEpc'

#imgtype = 'D90' # D90 camera image
imgtype = 'disp' # horizontal 4-up composite image

# set up display and image sizes for screen
if disptype == 'LVDS':
   size = (1024, 768) # LVDS display screen size
   if imgtype == 'D90': imagesz = (1152, 768) # LVDS image size, D90
   if imgtype == 'disp': imagesz = (1024, 614) # LVDS image size, composite
if disptype == 'EEEpc':
   size = (1024, 600) # EEE pc screen size
   if imgtype == 'D90': imagesz = (900, 600) # EEE pc image size, D90
   if imgtype == 'disp': imagesz = (1000, 600) # EEE pc image size, composite

# determine the proper offset for a centered image, x and y...
imageloc = center_loc(size, imagesz) 

# initiate pygame and hide mouse..
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

# directory to pull image files from...
basefiles = '/root/share/for-display/'
#basefiles = '/root/share/raw-images/'

# repeate forever, or at least until a quit event...
while (1):
   files = os.listdir(basefiles)
   for i in files:
	if i not in ['.', '..']:
		displayimage (screen, basefiles+i, imagesz, imageloc )
		time.sleep(2.0)

		for event in pygame.event.get():
			if event.type == QUIT or event.key == K_q or event.key == K_ESCAPE:
				sys.exit()

