# Kiltispiikki

Kiltispiikki uses platform independent python package kivy for the GUI. Used sqlite3 databases are backed up on google drive

## Installation

Install kivy following the kivy installation guide (pick right platform) 

https://kivy.org/docs/installation/installation.html

install kivy dependencies on RasPi

```
$ sudo apt-get update
$ sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
      python-setuptools libgstreamer1.0-dev git-core \
	     gstreamer1.0-plugins-{bad,base,good,ugly} \
		    gstreamer1.0-{omx,alsa} python-dev cython
```

install kivy (RasPi only found old package versions of cython so had to rename the old version first)

```
$ sudo pip install git+https://github.com/kivy/kivy.git@master
```

Kiltispiikki uses google play api to make backups to google drive. Install google-api with

```
$ pip install --upgrade google-api-python-client
```

Before first run on a new user go to the folder piikki/drive_init/ and run 

```
$ python drive_auth_init.py
```

This starts the authentication flow for the google drive, it should direct the user to browser to login in to a google account. Kiltispiikki is currently configured for hupimestari account. A new account will require for the user to go to google developers console and create a new oauth2 token and download their own client_secret file to the folder drive_init/


## Setting up touchscreen

The touch screen used is waveshare 10.1" lcd touch screen 

https://www.waveshare.com/wiki/10.1inch_HDMI_LCD

Copy the driver "LCD-show" to the rasperry. Your home folder is fine. extract the archive with

```
$ tar xvf "filename"
```

the go to the folder and run the correct driver 

```
$ sudo ./LCD101-"something"
```
the touch screen should now start

