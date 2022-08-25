# RSS Tube

A simple desktop application for Youtube, based on RSS feeds.


## Download

[Download the latest release.](https://github.com/seird/rsstube/releases/latest)

or, install via pip:
```
$ pip install rsstube
```


## Features

- Subscribe to youtube (and soundcloud) channels via RSS without needing a google account.
- Launch mpv (or other external video players) directly from the gui.
- Rule based filters to automatically delete new entries or mark them as viewed.


Dark theme                                                            |  Light theme
:--------------------------------------------------------------------:|:---------------------------------------------------------------------:
![](https://raw.githubusercontent.com/seird/rsstube/master/images/dark.png)  |  ![](https://raw.githubusercontent.com/seird/rsstube/master/images/light.png)


## Manual Installation

Get the source and install the requirements:

```
$ git clone https://github.com/seird/rsstube
$ cd rsstube
$ pip install -r requirements.txt
```

### Run from source

```
$ python -m rss_tube
```

### Create a pyinstaller executable

```
$ pip install pyinstaller
$ pyinstaller rss-tube.spec
```
An executable is created at `dist/rsstube/rsstube`.

### Create a deb package

```
$ make build

# or install

$ sudo make install
```

### (Inno setup (Windows))

Create an installer for windows with inno setup:

```
$ iscc rss-tube.iss
```


## Requirements

- Python >= 3.8
- lxml
- PyQt6
- requests
- schedule
- packaging
- (pysocks to connect to a socks5 proxy)
- (mpv + yt-dlp/youtube-dl or vlc, to directly play videos)
