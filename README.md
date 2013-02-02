Hobo Simulator 2013
===================

Watch your shit, son, we Hobo now! Gotta catch them all!... and tie RAZORBLADES to their claws an' shit!

Dogfighting adventure written in python, using pyGame and pyCairo.

Windows Development Setup
-------------------------
Library Dependencies for Windows:
- PyGame :  http://pygame.org/ftp/pygame-1.9.2a0.win32-py2.7.msi
- pyCairo : http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/pygtk-all-in-one-2.24.0.win32-py2.7.msi
- numPy : http://sourceforge.net/projects/numpy/files/NumPy/1.5.1/numpy-1.5.1-win32-superpack-python2.7.exe/download
- PIL : http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe


OSX Development Setup
---------------------
I setup everything using the Homebrew package manager, and pip with brew's python 2.x distribution.
Be sure that /usr/local/bin has presidence in your path.

###Install PyGame
```
brew install python
brew install hg
brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi 
pip install hg+http://bitbucket.org/pygame/pygame
```

###Install pyCairo
```
brew install ciaro pyCairo
```

###Install numPy
```
pip install numPy
```

###Install PIL
```
pip install PIL
```
