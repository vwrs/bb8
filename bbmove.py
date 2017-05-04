#!/usr/bin/env python

import pygame

from bb8 import BB8

pygame.display.set_mode((320, 240))
c = pygame.time.Clock()

bb = BB8('EE:D7:9A:A7:79:77')
bb.cmd(0x02, 0x20, [0x10, 0x10, 0x10, 0])
bb.cmd(0x02, 0x21, [0xff])

keys = [False] * 1024
h = 0

while True:
    c.tick(10)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False

    if keys[pygame.K_UP]:
        v = 100
    elif keys[pygame.K_DOWN]:
        v = 255
    else:
        v = 0

    if keys[pygame.K_LEFT]:
        h -= 15
    elif keys[pygame.K_RIGHT]:
        h += 15
    while h<0:
        h += 360
    while h>359:
        h -= 360
    print(h)

    bb.cmd(0x02, 0x30, [v, (h&0xff00)>>8, h&0xff, 1])
