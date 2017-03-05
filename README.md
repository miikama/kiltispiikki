# Kiltispiikki

Kiltispiikki uses platform independent python package kivy for the GUI. Used sqlite3 databases are backed up on google drive

##Installation

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






