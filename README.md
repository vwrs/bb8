# bb8
control BB-8(Sphero) by [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

## Requirements
- python2.7
    - bluepy
    - pygame
- web camera
- Ubuntu 16.04 LTS(recommended)
    - worked on NVIDIA Jetson TX2

## Usage
1. install openpose at ~/openpose and `mkdir ~/output`
2. get Sphero's mac address & edit `bbmove.py`
```
$ sudo hcitool lescan
$ vim bbmove.py
```
3. run!
```
$ ./openpose.sh
$ python bbmove.py
```

ref(BB8 driver):
https://github.com/jchadwhite/SpheroBB8-python
