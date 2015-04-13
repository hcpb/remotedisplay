#!/usr/bin/python
# many dependencies are all brought in with this import...
from libslideshow import *
from random import randrange


#=============================================================================
# ==================================  MAIN  ==================================
#=============================================================================

size = (1024, 600)
pygame.init()
screen = pygame.display.set_mode(size)
#toggle_fullscreen()

#basefiles = '/root/share/for-display/'
basefiles = '/root/share/raw-images/'
files = os.listdir(basefiles)
for i in files:
	if i not in ['.', '..']:
		displayimage (screen, basefiles+i, (900,600) )
		time.sleep(3.0)

