# bb8
control BB-8(Sphero) by [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

## requirements
- python2.7
    - bluepy
    - pygame
- web camera
- Ubuntu 16.04 LTS(recommended)

## usage
1. install openpose at ~/openpose
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

ref:
https://github.com/jchadwhite/SpheroBB8-python
