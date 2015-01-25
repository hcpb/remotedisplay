#!/usr/bin/python
# many dependencies are all brought in with this import...
from libslideshow import *
from random import randrange
from string import split,join
import os
import urllib2

#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# indicate what display we are using...
#disptype = 'LVDS'
disptype = 'EEEpc'
disptype = 'mx28'

#imgtype = 'D90' # D90 camera image
imgtype = 'disp' # horizontal 4-up composite image

# set up display and image sizes for screen
if disptype == 'LVDS':
   size = (1024, 768) # LVDS display screen size
   if imgtype == 'D90': imagesz = (1152, 768) # LVDS image size, D90
   if imgtype == 'disp': imagesz = (1024, 698) # LVDS image size, composite
if disptype == 'EEEpc':
   size = (1024, 600) # EEE pc screen size
   if imgtype == 'D90': imagesz = (900, 600) # EEE pc image size, D90
   if imgtype == 'disp': imagesz = (880, 600) # EEE pc image size, composite
if disptype == 'mx28':
   size = (800, 480)
   if imgtype == 'D90': imagesz = (720, 480) # EEE pc image size, D90
   if imgtype == 'disp': imagesz = (704, 480) # EEE pc image size, composite

# determine the proper offset for a centered image, x and y...
imageloc = center_loc(size, imagesz) 

# initiate pygame and hide mouse..
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

# directory to pull image files from...
if imgtype=='disp': basefiles = '/root/share/for-display/'
if imgtype=='D90': basefiles = '/root/share/raw-images/'

lastone = ''
count = 0
cc = []
while(1):
	check = urllib2.urlopen('http://10.81.17.82/~r14793/lastone.txt').read()
	if check <> lastone:
		lastone = check
		print "New one!", check
		# generate new list...
		bb = urllib2.urlopen('http://10.81.17.82/~r14793/for-disp/').read()
		bb = split(bb, 'href="')[2:]
		for i in bb:
			if i not in cc: cc.append(split(i, '">')[0])
			if cc[-1] not in os.listdir(os.curdir):
				print 'Grabbing file...'
				open(cc[-1], 'wb').write(urllib2.urlopen('http://10.81.17.82/~r14793/for-disp/'+cc[-1]).read())
			if lastone in cc[-1]:
				print 'displaying lastone ... ', cc[-1]
				displayimage (screen, cc[-1], imagesz, imageloc )
				time.sleep(3)

	count += 1
	if count == len(cc): count = 0
	print count, cc[count]
        displayimage (screen, cc[count], imagesz, imageloc )

        for event in pygame.event.get():
                if event.type == QUIT or event.key == K_q or event.key == K_ESCAPE:
                       sys.exit()
	time.sleep(3)




# repeate forever, or at least until a quit event...
while (1):
   files = os.listdir(basefiles)
   for i in files:
	if i not in ['.', '..']:
		displayimage (screen, basefiles+i, imagesz, imageloc )
		time.sleep(1.5)

		for event in pygame.event.get():
			if event.type == QUIT or event.key == K_q or event.key == K_ESCAPE:
				sys.exit()

