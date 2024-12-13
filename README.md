# Voice KKuTu

Voice KKuTu - Team Project for Embedded Software Lecture

## Getting Started

[`rye`](https://rye.astral.sh) is required for run this project easily.

```sh
# Fetch KKuTu Repository
git module init
git module update

# Install dependencies
rye sync

# Convert word database from KKuTu DB
rye run convert

# Install pre commit script for linting
rye run pre-commit
```

If below commands are not executed sucessfully, Try `rye sync` first.

**Commands**
```
rye run app
rye run convert
rye run clean
rye run black
rye run pre-commit
```

### Convert word data from KKuTu DB
This repository contains KKuTu repository as submodule.  

Word data for KKuTu server can be migrated for this project with converting script.

```sh
git submodule init
git submodule update
rye run convert
```

## Troubleshooting

### fatal error: 'portaudio.h' file not found

```
[stderr]
src/pyaudio/device_api.c:9:10: fatal error: 'portaudio.h' file not found
    9 | #include "portaudio.h"
      |          ^~~~~~~~~~~~~
1 error generated.
error: command '/usr/bin/clang' failed with exit code 1

hint: This error likely indicates that you need to install a library that provides "portaudio.h" for `pyaudio@0.2.14`
```

Install portaudio
```sh
sudo apt-get install portaudio19-dev  
```

### ModuleNotFoundError: No module name 'gi'
```sh
sudo apt update
sudo apt install -y build-essential libcairo2-dev libgirepository1.0-dev gir1.2-gtk-3.0 python3-dev
rye add PyGObject
```


## Raspberry Pi Setting

### Audio Activation
```
# Enable auido (loads snd_bcm2835)
dtparam=audio=on
```
remove comments from `boot/config.txt`

```sh
sudo /etc/init.d/alsa-utils reset
sudo reboot
```


### Audio Output
```sh
sudo raspi-config
```
System Options > Audio > [choose the audio output]

### Audio Output Test
Run TTS
```sh
sudo apt-get install espeak
espeak "hello"
```