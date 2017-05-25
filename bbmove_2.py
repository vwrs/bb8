#!/usr/bin/env python

import os
import glob
import json
import pygame
from pygame.locals import *
import sys

from bb8_2 import BB8

def get_values():
    filetmp=glob.glob('out2/*.json')
    if len(filetmp)!=0:
        try:
            filetmp.sort()
            with open(filetmp[-1],'r') as f:
                tmp=json.load(f)
            data=tmp["people"][0]["body_parts"]
            #残りのファイルを削除する
            for this in filetmp:
                os.remove(this)
            return data
        except:
            print 'read_nexttime'
            return 1

#向井追加分
data2=[]
READ_RATE=1000
SCREEN_SIZE = (640, 480)
framerate=100
COUNTA=READ_RATE/framerate
clock = pygame.time.Clock()
myfont = pygame.font.Font("ipag.ttf", 30)

i=0
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"値を読むだけだよ".encode('utf-8'))
#描画（毎回やる）
pose=get_values()
texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
textb=str(pose[12])+' '+str(pose[13])+' '+str(pose[14])
texta=unicode(texta.decode('utf-8'))
textb=unicode(textb.decode('utf-8'))
# テキストを描画したSurfaceを作成
hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
hello2 = myfont.render(u'右腕'+textb,True, (0,0,0))
hello3=myfont.render(str(i), True, (0,0,0))
counta=0





# pygame.display.set_mode((320, 240))
c = pygame.time.Clock()

bb = BB8('EE:D7:9A:A7:79:77')
bb.cmd(0x02, 0x20, [0x10, 0x10, 0x10, 0])
bb.cmd(0x02, 0x21, [0xff])

keys = [False] * 1024
h = 0

while True:
    #向井追加分
    if counta==COUNTA:
        pose=get_values()
        try:
            a=pose[10]
            texta=str(pose[6])+' '+str(pose[7])+' '+str(pose[8])
            textb=str(pose[12])+' '+str(pose[13])+' '+str(pose[14])
            texta=unicode(texta.decode('utf-8'))
            textb=unicode(textb.decode('utf-8'))

            # テキストを描画したSurfaceを作成
            hello1 = myfont.render(u'右肩'+texta, False, (0,0,0))
            hello2 = myfont.render(u'右腕'+textb,True, (0,0,0))
            hello3=myfont.render(str(i), True, (0,0,0))
        except:
            print 'read_next'
        counta=0
    screen.fill((255,255,255))
    counta+=1
    # テキストを描画する
    screen.blit(hello1, (90,50))
    screen.blit(hello2, (90,150))
    screen.blit(hello3, (90,250))
    pygame.display.update()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False
    if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(framerate)




    if pose[13]-pose[7]>0:
        v = 255
    else:
        v=100



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
    print h

    bb.cmd(0x02, 0x30, [v, (h&0xff00)>>8, h&0xff, 1])
