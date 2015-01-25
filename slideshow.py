#!/usr/bin/python
# many dependencies are all brought in with this import...
from libslideshow import *
from random import randrange, shuffle
from string import split,join
import os
import urllib2

#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

# indicate what display we are using...
#disptype = 'LVDS'  # FSL LVDS display 
#disptype = 'EEEpc' # EEE PC netbook 
disptype = 'mx28'  # i.MX28 LCD display

#imgtype = 'D90' # D90 camera image
imgtype = 'disp' # horizontal 4-up composite image

# set up display and image sizes for screen
if disptype == 'LVDS':
   size = (1024, 768) # LVDS display screen size
   if imgtype == 'D90': imagesz = (1152, 768) # LVDS image size, D90 aspect ratio
   if imgtype == 'disp': imagesz = (1024, 698) # LVDS image size, composite aspect ratio
if disptype == 'EEEpc':
   size = (1024, 600) # EEE pc screen size
   if imgtype == 'D90': imagesz = (900, 600) # EEE pc image size, D90 aspect ratio
   if imgtype == 'disp': imagesz = (880, 600) # EEE pc image size, composite aspect ratio
if disptype == 'mx28':
   size = (800, 480) # i.MX28 LCD screen size
   if imgtype == 'D90': imagesz = (720, 480) # MX28 image size, D90 aspect ratio
   if imgtype == 'disp': imagesz = (704, 480) # MX28 image size, composite aspect ratio

# determine the proper offset for a centered image on the display we're using...
imageloc = center_loc(size, imagesz) 

# initiate pygame and hide mouse...
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

baseurl = 'http://10.81.17.82/~r14793/'

lastone = '' # this is the beginning of the latest image set: DSCxxxx 
count = 0    # index counter for stepping through list of files to display
files = []   # list of images to display

while(1):
	# check to see if a new image set is ready...
	check = urllib2.urlopen(baseurl+'lastone.txt').read()

	# grab the directory index if there has been a change...
	if check <> lastone:
		lastone = check # the latest is the new 'lastone'
		print "New one!", check
		# grab the new list...
		indx = urllib2.urlopen(baseurl+'for-disp/').read()
		# split the text to extract th image names
		indx = split(indx, 'href="')[2:]
		# iterate over the list of file names
		for i in indx:
			# further split the list of name because incomplete above
			filename = split(i, '">')[0]
			# add to file list if it's not already there...
			if filename not in files: files.append(filename)
			# grab the file if we don't already have it locally...
			if filename not in os.listdir(os.curdir):
				print 'Grabbing file...'
				open(filename, 'wb').write(urllib2.urlopen(baseurl+'for-disp/'+filename).read())
			# if 'i' is actually the latest, then display it right now...
			# holding it a little longer so people can see it when they come out
			if lastone in filename:
				print 'displaying lastone ... ', filename 
				displayimage (screen, filename, imagesz, imageloc )
				time.sleep(5)

	count += 1 # increment counter for stepping through 'files' list
	# check for the end of the list, and if it is, shuffle the file list as well
	if count == len(files): 
		count = 0
		print 'Shuffling file list...'
		shuffle(files)
	print count, files[count]
	# display the next image in the file list...
        displayimage (screen, files[count], imagesz, imageloc )

	# check for a signal to quit...
        for event in pygame.event.get():
                if event.type == QUIT or event.key == K_q or event.key == K_ESCAPE:
                       sys.exit()

	# delay time for displaying the image...
	time.sleep(3)


