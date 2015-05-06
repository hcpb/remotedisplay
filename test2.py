#!/usr/bin/python
# many dependencies are all brought in with this import...
from libslideshow import *
from random import randrange
import Image, select, v4l2capture
from time import sleep, time
from StringIO import StringIO

def startvid():			# open the video camera for use...
	global x, y, video
        video = v4l2capture.Video_device('/dev/video0')
        x, y = video.set_format(1280, 720, fourcc='MJPG')
	video.create_buffers(1)
        video.queue_all_buffers()
	video.start()

def grabframe_and_display(sv=False):	# grab a frame from cam and display t to screen
	buff = StringIO()	# create StringIO buffer for stashing image data
	#video.start()		# start the video cam
        select.select((video,), (), ())

	image_data = video.read_and_queue()	# grab image from camera
	buff.write(image_data)			# stash in buff
	buff.seek(0)				# reset file pointer to zero...
	im = Image.open(buff)			# read image from buff
	buff.seek(0)				# reset file pointer to zero again...
        mode = im.mode				# pull relevant info from image for pygame
        imsz = im.size
        data = im.tostring()
        image = pygame.image.fromstring(data, imsz, mode) # read image into pygame...
        imagerect = image.get_rect()			  # and display it...
        image = pygame.transform.scale(image, imagesz)
	sx, sy = size	# locate the image in the center of the screen...
	ix, iy = imagesz
	loc = ( int((sx-ix)/2.), int((sy-iy)/2.) )
        screen.blit(image, loc)
        pygame.display.flip()

	if sv: 
		im.save('/var/www/html/frame'+str(time())+'.jpg')
		print 'Saved image...'


# ==================================  MAIN  ==================================
#=============================================================================

# indicate what display we are using...
#disptype = 'LVDS'
#disptype = 'EEEpc'
#disptype = 'mx28'
disptype = 'fullhd' #hdmi TV

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
if disptype == 'fullhd':
   size = (1920, 1080)
   if imgtype == 'D90': imagesz  = (1620, 1080)
   if imgtype == 'disp': imagesz = (1920, 1080)
   if imgtype == 'hd720': imagesz = (1920, 1080) 


# determine the proper offset for a centered image, x and y...
imageloc = center_loc(size, imagesz) 

# initiate pygame and hide mouse..
pygame.init()
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(False)

# directory to pull image files from...
if imgtype=='disp': basefiles = '/root/share/for-display/'
if imgtype=='D90': basefiles = '/root/share/raw-images/'

startvid()

# repeate forever, or at least until a quit event...
count = 0
while (1):
	count += 1
	if count == 90:
		count = 0
		grabframe_and_display(sv=True)
	else: grabframe_and_display(sv=False)

	for event in pygame.event.get():
			if event.type == QUIT or event.key == K_q or event.key == K_ESCAPE:
				sys.exit()

